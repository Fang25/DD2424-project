import threading

import pyaudio
import wave

import csv
import os

import time
path = os.getcwd()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = path + "\\" + "long\\LONG_SEGMENT1.wav"


PRESSED_KEY_FILE =  path + "\\" + "long\\Key_ACTION1.csv"


class RecordThread2(threading.Thread):

    
    def __init__(self):
    
        self.action = []
        self.time_List = []
        self.key_list = []
        
        self.stop = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
                
        self.frames = []
        self.i = 0
        self.t = []
        
        threading.Thread.__init__(self)
        
    def addToList(self, key, action):
        self.t.append(time.clock())
        self.action.append(action)
        self.time_List.append(self.i)
        self.key_list.append(key)

        
    def saveToFolder(self):
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        with open(PRESSED_KEY_FILE, 'wt') as writeFile:
            writer = csv.writer(writeFile)
            line = [0, 0, 0, self.t[0]]
            writer.writerow(line)
            for i in range(len(self.action)):
                line = [self.time_List[i], self.key_list[i], self.action[i], self.t[i + 1]]
                writer.writerow(line)
            line = [self.i, 'Exit', 'E', self.t[-1]]
            writer.writerow(line)
        writeFile.close()
        
    def run(self):
        
        print("* recording")
        self.t.append(time.clock())
        while not self.stop:
            
            data = self.stream.read(CHUNK)
            self.frames.append(data)
            self.i += 1
        self.t.append(time.clock())
        print("* done recording")
        
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self.saveToFolder()
        
    def change_condition(self):
        self.stop = True

    def get_output_name(self):
        return(WAVE_OUTPUT_FILENAME)
    
    def get_key_name(self):
        return(PRESSED_KEY_FILE)
        
        