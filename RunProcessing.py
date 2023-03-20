import numpy as np
import os
from processing import processing
from mat4py import loadmat
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from patient_data_sqlite import get_gif_path


def run_processing(patient_data, thresh, pat_num):
    # Initiate variables and static values
    patient_data = patient_data.decode()
    ecg = loadmat(patient_data) #need to take the
    array_data = np.array(ecg['array_data'])
    array_gain = np.zeros(112)
    array_data_nogain = np.zeros(array_data.shape)
    fs = 1000
    start_range = 0
    end_range = 112
    x_coord = np.zeros(112)
    y_coord = np.zeros(112)


    # Put data into variables
    for n in range(start_range, end_range):
        x_coord[n] = np.array(ecg['elec_array']['chan'][n]['x'])
        y_coord[n] = np.array(ecg['elec_array']['chan'][n]['y'])
        array_gain[n] = np.array(ecg['elec_array']['chan'][n]['gain'])
        array_data_nogain[:, n] = np.array(array_data[:, n] / array_gain[n])

    # Run processing function
    temp = []
    for n in range(start_range, end_range):
        send_to_mc = processing(array_data_nogain[:, n], fs, thresh)
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
                downsample[j, i // ms] = 1.0
            else:
                downsample[j, i // ms] = 0.0

    # Convert matrix to array to be sent to microcontroller
    flattened_data = downsample.flatten(order='C')

    # Send array to csv
    downsample.tofile('vt_sample_test.csv', sep=',', format='%10.5f')

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
        ax.set_title('positions')
        plt.savefig('frame_{0:03d}.png'.format(num))

    # Saving the frames as a gif
    images = []
    for i in range(downsample.shape[1]):
        images.append(imageio.imread('frame_{0:03d}.png'.format(i)))
        os.remove(f'frame_{i:03d}.png')

    # Get gif path and make it only accessible by user
    gif_path = get_gif_path(pat_num)
    os.chmod(gif_path, 0o700)

    imageio.mimsave(gif_path, #need to send it to application save location
                    images, fps=10) # edithere update so that .gif is deleted upon closure of application

    return flattened_data

# call function to run
# run_processing("C:/Users/krist/PycharmProjects/capscone_sigprocessing_v1/vt1_sample.mat", 1, 123456789)
