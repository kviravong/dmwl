import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime

def create_dmwl():
    # Create a DMWL dataset
    ds = Dataset()

    # Patient information
    ds.PatientID = "123456"
    ds.PatientName = "DOE^JOHN"
    ds.PatientBirthDate = "20000101"
    ds.PatientSex = "M"

    # Study information
    ds.StudyInstanceUID = "1.3.6.1.4.1.5962.99.1.1761388472.1291962045.1616669124536.2592.0"
    ds.StudyDate = "20250328"
    ds.StudyTime = "010434.000"

    # Scheduled procedure step
    ds.ScheduledStationAETitle = "CT_STATION_01"
    ds.ScheduledProcedureStepStartDate = "20250328"
    ds.ScheduledProcedureStepStartTime = "010434.000"
    ds.Modality = "CT"

    # Create a FileDataset (DMWL file)
    file_meta = pydicom.dataset.Dataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.31"  # Correct UID for Modality Worklist Information Model - FIND
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    filename_dcm = "dmwl_ct.dcm"
    
    ds = FileDataset(filename_dcm, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # Add the dataset attributes to the FileDataset
    ds.update({
        'PatientID': "123456",
        'PatientName': "DOE^JOHN",
        'PatientBirthDate': "20000101",
        'PatientSex': "M",
        'StudyInstanceUID': "1.3.6.1.4.1.5962.99.1.1761388472.1291962045.1616669124536.2592.0",
        'StudyDate': "20250328",
        'StudyTime': "010434.000",
        'ScheduledStationAETitle': "CT_STATION_01",
        'ScheduledProcedureStepStartDate': "20250328",
        'ScheduledProcedureStepStartTime': "010434.000",
        'Modality': "CT"
    })

    # Save the DMWL file
    ds.save_as(filename_dcm)
    
    print(f"DMWL file '{filename_dcm}' created successfully.")

if __name__ == "__main__":
    create_dmwl()
