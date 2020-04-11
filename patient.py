from os.path import join
from glob import glob
from warnings import filterwarnings
from numpy import around, array, concatenate
from mne.io import read_raw_edf

from chb_label_wrapper import ChbLabelWrapper


filterwarnings("ignore", category=RuntimeWarning)


class Patient:

    def __init__(self, id, path_dataset):
        self._id = id
        self._path_dataset = path_dataset
        self._list_files = glob(join(self._path_dataset,
                                     "chb{0:0=2d}/*.edf".format(self._id)))

        self._edf_files = list(map(lambda x: read_raw_edf(x, verbose=0),
                                   self._list_files))
        self._cumulative_duration = [0]

        self._cumulative_duration = [len(file.times)
                                     for file in self._edf_files]

        self._duration = sum(self._cumulative_duration)

        name_path = "chb{0:0=2d}/chb{0:0=2d}-summary.txt".format(self._id, self._id)
        
        self._seizure_list = ChbLabelWrapper(join(self._path_dataset,
                                                  name_path)).get_seizure_list()

    def get_channel_names(self):
        return self._edf_files[0].get_channel_names()

    def get_eeg_data(self):

        all_data = [file.get_data() for file in self._edf_files]

        return concatenate(all_data)

    def get_non_seizures(self, name_channel="FT9-FT10"):

        clips = []
        for input_, file in zip(self._seizure_list, self._edf_files):

            data_frame = file.to_data_frame()
            range_times = around(file.times, 2)

            if input_ == []:

                clips.append(data_frame[name_channel].to_numpy())

            else:
                acc_not_seizure = array([])

                for range_ in input_:

                    begin = range_[0]

                    end = range_[1]

                    range_not_seizure = array([(range_times >= begin) &
                                               (range_times <= end)]).reshape(-1)

                    acc_not_seizure = (range_not_seizure | range_not_seizure)

                clips.append(data_frame[name_channel].to_numpy()[(~ acc_not_seizure)])

        return clips

    def get_seizure_clips(self, name_channel="FT9-FT10"):

        clips = []
        for input_, file in zip(self._seizure_list, self._edf_files):

            range_times = around(file.times, 2)

            data_frame = file.to_data_frame()

            if input_ == []:

                clips.append([])

            else:

                for range_ in input_:

                    begin = range_[0]

                    end = range_[1]

                    range_seizure = [(range_times >= begin)
                                     & (range_times < end)]

                    clips_ = data_frame[name_channel].to_numpy()[
                        tuple(range_seizure)]

                    clips.append(clips_)

        return clips
