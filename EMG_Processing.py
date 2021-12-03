#!/usr/bin/env python
# coding: utf-8



# In[15]:


import scipy.signal as ssig
import math
import numpy as np

class EMG_data:
    
    def __init__(self,name):
        self.name=name
    
    def load_data(self):
        file=open(self.name,'r')
        lines=file.readlines()
        time,emg=[],[]
        for i in lines:
            time.append(float(i.split("\t")[0]))
            emg.append(float(i.split("\t")[-1]))
        return time, emg
    
    def high_Freq_response(self,data,fs): # Highpass_filter + freq_response
        b,a= ssig.butter(6,10,btype='high',fs=fs)
        w,h=ssig.freqz(b,a,fs)
        w_hz=w*fs/(2*math.pi)
        high_data=ssig.filtfilt(b,a,data)
        return w_hz, abs(h), high_data
    
    def low_Freq_response(self,data,fs): # Lowpass_filter + freq_response
        b,a=ssig.butter(5,20,btype='low', fs=fs)
        w,h=ssig.freqz(b,a,fs)
        w_hz=w*fs/(2*math.pi)
        low_data=ssig.filtfilt(b,a,data)
        return w_hz, abs(h), low_data
    
    def RMS_processing(self,data): # rms processing 
        rms_data=[]
        part_sum,count=0,0
        for i in range(0,len(data)):
            slist=[x**2 for x in data[i:i+int(0.07/0.0005)]]
            s2_list=math.sqrt(sum(slist)/len(slist))
            rms_data.extend([s2_list])
        return rms_data
    
    def show_result(self):
        time,emg=EMG_data.load_data(self)
        fs=int(1/(time[1]-time[0]))
        w_hz,h_fr,high_emg=EMG_data.high_Freq_response(self,emg,fs)
        l_hz,l_fr,low_emg=EMG_data.low_Freq_response(self,abs(high_emg),fs)
        rms_data=EMG_data.RMS_processing(self,high_emg)
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,8))
        plt.subplot(3,3,1);plt.plot(time,emg,'black');plt.title("Original EMG data"); plt.xlabel('time(s)'); plt.ylabel('amplitude(mV)');
        plt.subplot(3,3,2);plt.plot(w_hz,h_fr,'black');plt.title("Frequency response"); plt.xlabel('frequency(Hz)'); plt.ylabel('|H|');plt.xlim([0,50])
        plt.subplot(3,3,3);plt.plot(time,high_emg,'black');plt.title("High-pass filtered EMG data"); plt.xlabel('time(s)'); plt.ylabel('amplitude(mV)');
        plt.subplot(3,3,4);plt.plot(time,abs(high_emg),'black');plt.title("rectified EMG data"); plt.xlabel('time(s)'); plt.ylabel('amplitude(mV)');
        plt.subplot(3,3,5);plt.plot(l_hz,l_fr,'black');plt.title("Frequency response"); plt.xlabel('frequency(Hz)'); plt.ylabel('|H|');plt.xlim([0,50])
        plt.subplot(3,3,6);plt.plot(time,high_emg,'black',label='Original data');plt.plot(time,low_emg,'red', label='Envelope');plt.title("Low-pass filtered EMG data"); plt.xlabel('time(s)'); plt.ylabel('amplitude(mV)');
        plt.legend()
        plt.subplot(3,1,3);plt.plot(time,high_emg,'black',label='Original data');plt.plot(time,rms_data,'red',label='RMS');plt.title("RMS of EMG data"); plt.xlabel('time(s)'); plt.ylabel('amplitude(mV)');
        plt.legend();plt.tight_layout();plt.show()

    
if __name__=="__main__":
    EMG_data('EMG_data.txt').show_result()
    
    


# In[ ]:





# In[ ]:




