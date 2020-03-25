# chb-mit

Functions for reading the CHB-MIT scalp EEG database. Update on the work developed by @dougkoch. Adaptation to use in the reproduction of an article.

Modifications made:

* Removal of functions not used or already implemented in my application (__e.g.__: download);

* Conversion from python 2 to python 3;

* Changing library to read the file:
    * pyedflib -> mne.

* Adaptation of functions to allow interoperability;