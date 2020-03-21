import numpy as np
from patient import Patient
import random

# Generates splits within one patient (defaults to 80%/10%/10% train/val/test)
def intra_patient_split(patient_id, train_frac=0.8, val_frac=0.1):
    p = Patient(patient_id)
    seizures = p.get_seizures()
    clips = p.get_seizure_clips()

    test_frac = 1.0 - train_frac - val_frac

    n_val_seizures = max(1, int(round(val_frac * len(seizures))))
    n_test_seizures = max(1, int(round(test_frac * len(seizures))))
    n_train_seizures = len(seizures) - n_val_seizures - n_test_seizures

    return (
        # Training clips
        clips[:n_train_seizures],

        # Validation clips
        clips[n_train_seizures : n_train_seizures + n_val_seizures],
        
        # Test clips
        clips[n_train_seizures + n_val_seizures:]
    )

# Generates splits across patients
def inter_patient_split():
    patient_ids = [id for id in range(1, 11)]

    x = np.zeros((0, 23))
    y = np.array([])

    for id_ in patient_ids:
        patient = Patient(id_)    
        
        x = np.vstack((x, patient.get_eeg_data()))
        y = np.vstack((y, patient.get_seizure_labels()))

    return x, y
