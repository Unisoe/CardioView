import os
import Config
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as Line2D
from HandlerEllipse import HandlerEllipse
import seaborn as sns

sns.set()
sns.set_theme(style="whitegrid", palette="pastel")


def processing(ecg, fs, user_thresh, electrode_num, pat_num):
    let_c = []
    let_i = []
    sig_lvl = 0
    delay = 0
    skip = 0
    not_noise = 0
    noise_c = []
    noise_i = []
    let_i_raw = []
    let_amp_raw = []
    m_selected_p = 0
    mean_p = 0
    ser_back = 0
    text_m = 0
    sigl_buf = []
    noisl_buf = []
    thresh_buf = []
    sigl_buf1 = []
    noisl_buf1 = []
    thresh_buf1 = []
    pl = 1

    '''user input thresh'''
    if user_thresh:
        thresh = user_thresh
    else:
        thresh = 1

    '''bandpass filter'''
    f1 = 5
    f2 = 15
    n = 3
    t = np.arange(0, 4472, 1)
    nyq = 0.5 * fs
    low = f1 / nyq
    high = f2 / nyq
    b, a = sc.signal.butter(n, [low, high], 'bandpass')
    ecg_butt = sc.signal.filtfilt(b, a, ecg)
    ecg_butt = ecg_butt / max(np.absolute(ecg_butt))

    '''derivative filter'''
    h_d = np.array([-1, -2, 0, 2, 1]) * (fs / 8)
    ecg_der = np.convolve(ecg_butt, h_d)
    ecg_der = ecg_der / max(ecg_der)
    delay = delay + 2

    '''squaring non-linearly to enhance dominant peaks'''
    ecg_squared = np.square(ecg_der)

    '''moving average'''
    len_ones = round(0.150 * fs)
    array_ones = np.ones(len_ones) / len_ones

    ecg_moving_avg = np.convolve(ecg_squared, array_ones)
    delay = delay + 15

    '''take the derivative'''
    ecg_moving_avg = np.diff(ecg_moving_avg)

    '''fiducial mark'''
    locs, properties = sc.signal.find_peaks(ecg_moving_avg, distance=round(0.2 * fs))

    '''training phase'''
    sig_thresh = (max(ecg_moving_avg[0:fs])) / 3
    noise_thresh = (np.mean(ecg_moving_avg[0:fs])) / 2
    sig_lvl = sig_thresh
    noise_lvl = noise_thresh

    '''bandpass filter threshold'''
    sig_thresh1 = (max(ecg_butt[0:(2 * fs)])) / 3
    noise_thresh1 = (np.mean(ecg_butt[0:(2 * fs)])) / 2
    sig_lvl1 = sig_thresh1
    noise_lvl1 = noise_thresh1

    '''thresholding and online decision rule'''
    for i in range(len(locs)):
        '''locate corresponding peak in filtered sig'''
        if (locs[i] - round(0.15 * fs) >= 0) and (locs[i] <= len(ecg_butt)):
            y_i = max(ecg_butt[(locs[i] - round(0.150 * fs)):locs[i]])
            x_i = i
        else:
            if i == 0:
                y_i = max(ecg_butt[0:locs[i]])
                x_i = i
                ser_back = 1
            elif locs[i] >= len(ecg_butt):
                y_i = max(ecg_butt[locs[i] - round(0.150 * fs):])
                x_i = i
        # update activation rate (two means most recent and the other selected)
        if len(let_c) >= 9:
            diff_p = np.diff(let_i[-8:])  # calc interval
            mean_p = np.mean(diff_p)  # calc mean of 8 previous wave intervals
            comp = let_i[-1] - let_i[-2]  # latest set of peaks
            if 1.16 * mean_p <= comp or comp <= 0.92 * mean_p:
                sig_thresh = 0.5 * sig_thresh * thresh  # lower thresh to detect better in MVI
                sig_thresh1 = 0.5 * sig_thresh1 * thresh  # lower thresh to detect better in bandpass filt
            else:
                m_selected_p = mean_p  # latest regular beats mean

        if m_selected_p:
            test_m = m_selected_p  # if reg pulse interval is available use it
        elif mean_p and m_selected_p == 0:
            test_m = mean_p
        else:
            test_m = 0

        if test_m:
            if (locs[i] - let_i[-1]) >= round(1.66 * test_m):  # shows a peak is missed
                pks_temp = max(ecg_moving_avg[(let_i[-1] + round(0.2 * fs)):(locs[i] - round(0.2 * fs))])
                locs_temp = let_i[-1] + round(0.2 * fs) + locs_temp - 1
                if pks_temp > noise_thresh:
                    let_c = np.append(let_c, pks_temp)
                    let_i = np.append(let_i, locs_temp)
                    if locs_temp <= len(ecg_butt):  # find loc in filtered sig
                        y_i_t = max(ecg_butt[locs_temp - round(0.15 * fs):locs_temp])
                        x_i_t = i
                    else:
                        y_i_t = max(ecg_butt[locs_temp - round(0.15 * fs):])
                        x_i_t = i

                    if y_i_t > noise_thresh:  # bandpass thresh
                        let_i_raw = np.append(let_i_raw,
                                              locs_temp - round(0.15 * fs) + (x_i_t - 1))  # save index of bandpass
                        let_amp_raw = np.append(let_amp_raw, y_i_t)  # amp of bandpass
                        sig_lvl1 = 0.25 * y_i_t + 0.75 * sig_lvl1  # when found with second thresh
                    not_noise = 1
                    sig_lvl = 0.25 * pks_temp + 0.75 * sig_lvl  # when found with second thresh
                else:
                    not_noise = 0
        # find peaks and noise
        if ecg_moving_avg[locs[i]] >= sig_thresh:
            if len(let_c) >= 3:  # if peak candidate occurs within 360ms of previous peak
                if (locs[i] - let_i[-1]) <= round(0.36 * fs):
                    slope1 = np.mean(np.diff(ecg_moving_avg[(int(locs[i] - round(0.075 * fs))):int(locs[i])]))
                    slope2 = np.mean(np.diff(ecg_moving_avg[(int(let_i[-1] - round(0.075 * fs))):int(let_i[-1])]))
                    if np.abs(slope1) <= np.abs(0.5 * slope2):
                        noise_c = np.append(noise_c, ecg_moving_avg[locs[i]])
                        noise_i = np.append(noise_i, locs[i])
                        skip = 1  # false peak detection, adjust noise in filtered and MVI
                        noise_lvl1 = 0.125 * y_i + 0.875 * noise_lvl1
                        noise_lvl = 0.125 * locs[i] + 0.875 * noise_lvl
                    else:
                        skip = 0  # skip is 1 when false peak detected
            if skip == 0:
                let_c = np.append(let_c, ecg_moving_avg[locs[i]])
                let_i = np.append(let_i, locs[i])
                if y_i >= sig_thresh1:  # bandpass filter check thresh
                    if ser_back:
                        let_i_raw = np.append(let_i_raw, x_i)  # save bandpass index
                    else:
                        let_i_raw = np.append(let_i_raw,
                                              locs[i] - round(0.150 * fs) + (x_i - 1))  # save index of bandpass
                    let_amp_raw = np.append(let_amp_raw, y_i)  # save amplitude of bandpass
                sig_lvl = 0.125 * ecg_moving_avg[locs[i]] + 0.875 * sig_lvl  # adjust sig lvl
        elif (noise_thresh <= ecg_moving_avg[locs[i]]) and (ecg_moving_avg[locs[i]] < sig_thresh):
            noise_lvl1 = 0.125 * y_i + 0.875 * noise_lvl1  # adjust noise lvl in filt sig
            noise_lvl = 0.125 * ecg_moving_avg[locs[i]] + 0.875 * noise_lvl
        elif ecg_moving_avg[locs[i]] < noise_thresh:
            noise_c = np.append(noise_c, ecg_moving_avg[locs[i]])
            noise_i = np.append(noise_i, locs[i])
            noise_lvl1 = 0.125 * y_i + 0.875 * noise_lvl1  # adjust noise in filt sig
            noise_lvl = 0.125 * ecg_moving_avg[locs[i]] + 0.875 * noise_lvl  # adjuse noise in MVI
        if (noise_lvl != 0) or (sig_lvl != 0):
            sig_thresh = noise_lvl + 0.4 * (np.abs(sig_lvl - noise_lvl))
            noise_thresh = 0.5 * sig_thresh
        if (noise_lvl1 != 0) or (sig_lvl1 != 0):
            sig_thresh1 = noise_lvl1 + 0.25 * np.abs(sig_lvl1 - noise_lvl1)
            noise_thresh1 = 0.5 * sig_thresh1

        sigl_buf = np.append(sigl_buf, sig_lvl)
        noisl_buf = np.append(noisl_buf, noise_lvl)
        thresh_buf = np.append(thresh_buf, sig_thresh)
        sigl_buf1 = np.append(sigl_buf1, sig_lvl1)
        noisl_buf1 = np.append(noisl_buf1, noise_lvl1)
        thresh_buf1 = np.append(thresh_buf1, sig_thresh1)

        skip = 0
        not_noise = 0
        ser_back = 0

    if electrode_num == 16 or electrode_num == 50 or electrode_num == 107:
        # plotting
        plt.figure(figsize=(10,3))
        plt.ylim(ymax = 1.27, ymin = -1)
        r_label = Line2D.Line2D([0], [0], color='r', label='Noise Level', linestyle='--')
        m_label = Line2D.Line2D([0], [0], color='m', label='Signal Level', linestyle='-.')
        g_label = Line2D.Line2D([0], [0], color='g', label='Adaptive Threshold', linestyle='-.')
        k_vert = mpatches.Circle((0.5, 0.5), radius=0.3, color='k', label='Local Activation', linewidth=0.5)

        # plot filtered signal
        plt.plot(ecg_butt)
        for i in range(len(locs) - 1):
            x_vals = [locs[i], locs[i + 1]]
            y_vals_n = [noisl_buf1[i], noisl_buf1[i + 1]]
            y_vals_s = [sigl_buf1[i], sigl_buf1[i + 1]]
            y_vals_t = [thresh_buf1[i], thresh_buf1[i + 1]]
            plt.plot(x_vals, y_vals_n, linewidth=2, color='r', linestyle='--')
            plt.plot(x_vals, y_vals_s, linewidth=2, color='m', linestyle='-.')
            plt.plot(x_vals, y_vals_t, linewidth=2, color='g', linestyle='-.')
        plt.scatter(let_i.astype(int), let_c, c='k', s=20)

        # add legend
        plt.legend(handles=[r_label, m_label, g_label, k_vert],
                      loc='upper left', ncol=4, mode="expand", borderaxespad=0.,
                      handler_map={mpatches.Circle: HandlerEllipse()})

        # Save fig
        png_path = os.path.join(Config.patient_file_path, f'{pat_num}{electrode_num}.png')
        plt.savefig(png_path)

    # create binary array
    send_to_mc = np.zeros(len(ecg))
    for n in range(len(let_i)):
        for t in range(len(ecg)):
            if t == let_i[n]:
                send_to_mc[t] = 1

    return send_to_mc



    '''update activation rate'''