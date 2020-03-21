
import numpy as np
from glob import glob
from numpy import around, array
from os.path import join
from chb_edf_file import ChbEdfFile
from chb_label_wrapper import ChbLabelWrapper
from mne.io import read_raw_edf

class Patient:
    def __init__(self, id, path_dataset):
        self._id = id
        self._path_dataset = path_dataset
        self._list_files = glob(join(self._path_dataset, 
                                     "chb{0:0=2d}/*.edf".format(self._id)) )

        self._edf_files = list(map(lambda x : read_raw_edf(x, verbose=0), 
                                   self._list_files))
        self._cumulative_duration = [0]

        self._cumulative_duration = [len(file.times) 
                                     for file in self._edf_files]

        self._duration = sum(self._cumulative_duration)

        self._seizure_list = ChbLabelWrapper(
                                    "../data/chbmit/chb{0:0=2d}/chb{0:0=2d}-summary.txt".format(
                                        self._id, 
                                        self._id)).get_seizure_list()


    def get_channel_names(self):
        return self._edf_files[0].get_channel_names()

    def get_eeg_data(self):
    
        all_data = [file.get_data().T for file in self._edf_files]
        
        return np.concatenate(all_data)

    def get_non_seizures(self):
        
        clips = []
        for input_, file in zip(self._seizure_list, self._edf_files):

            range_times = around(file.times, 2)

            if input_ == []:

                clips.append(file.get_data().T)

            else:
                acc_not_seizure = array([])
                
                for range_ in input_:

                    begin = range_[0]

                    end = range_[1]

                    range_not_seizure = array([(range_times >= begin) & 
                                               (range_times <= end)]).reshape(-1) 

                    acc_not_seizure = (range_not_seizure | range_not_seizure)

                clips.append(file.get_data().T[(~ acc_not_seizure)])

        return clips

    def get_seizure_clips(self):
        
        clips = []
        for input_, file in zip(self._seizure_list, self._edf_files):

            range_times = around(file.times, 2)

            if input_ == []:

                clips.append([])

            else:

                for range_ in input_:

                    begin = range_[0]

                    end = range_[1]

                    clips_ = file.get_data().T[(range_times >= begin) & (range_times < end)]

                    clips.append(clips_)

        return clips