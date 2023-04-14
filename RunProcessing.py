import numpy as np
import os
from Processing import processing
from mat4py import loadmat
import matplotlib.pyplot as plt
import imageio.v2 as imageio

def run_processing(patient_data, gif_path, thresh, pat_num):
    # Initiate variables and static values
    ecg = loadmat(patient_data)
    array_data = np.array(ecg['array_data'])
    array_gain = np.zeros(112)
    array_data_nogain = np.zeros(array_data.shape)
    fs = 1000
    start_range = 0
    end_range = 112
    x_coord = np.zeros(112)
    y_coord = np.zeros(112)

    # Put send_to_mc into variables
    for n in range(start_range, end_range):
        x_coord[n] = np.array(ecg['elec_array']['chan'][n]['x'])
        y_coord[n] = np.array(ecg['elec_array']['chan'][n]['y'])
        array_gain[n] = np.array(ecg['elec_array']['chan'][n]['gain'])
        array_data_nogain[:, n] = np.array(array_data[:, n] / array_gain[n])

    # Run processing function
    temp = []
    for n in range(start_range, end_range):
        send_to_mc = processing(array_data_nogain[:, n], fs, thresh, n, pat_num)
        temp.append(send_to_mc)

    # Remove unwanted empty columns
    send_to_mc = np.array(temp)
    send_to_mc_2 = send_to_mc[:, ~np.all(send_to_mc == 0, axis=0)]

    # Create empty matrix
    send_to_mc_shape = send_to_mc_2.shape
    downsample = np.zeros((send_to_mc_shape[0], (send_to_mc_shape[1] // 8) + 1))

    # Combine every 8 ms
    ms = 8
    for i in range(0, len(send_to_mc_2[0]), ms):
        for j in range(112):
            if np.any(send_to_mc_2[j, i:i + ms]):
                downsample[j, i // ms] = 1
            else:
                downsample[j, i // ms] = 0

    # Convert matrix to array of strings to be sent to microcontroller
    array_of_strings = []
    transposed_downsample = zip(*downsample)
    for row in transposed_downsample:
        row_string = ''.join([str(elem) for elem in row])
        array_of_strings.append(row_string[:len(downsample[0])])


    # Plotting
    fig, ax = plt.subplots()
    for num in range(downsample.shape[1]):
        ax.clear()
        for m in range(112):
            if downsample[m, num] == 1:
                ax.scatter(x_coord[m], y_coord[m], color='r')
            else:
                ax.scatter(x_coord[m], y_coord[m], color='b')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.xlim([-100, 100])
        plt.ylim([-100, 100])
        ax.set_title('Local Activation')
        plt.savefig('frame_{0:03d}.png'.format(num))

    # Saving the frames as a gif
    images = []
    for i in range(downsample.shape[1]):
        images.append(imageio.imread('frame_{0:03d}.png'.format(i)))
        os.remove(f'frame_{i:03d}.png')

    imageio.mimsave(gif_path, images, fps=10)

    return array_of_strings

