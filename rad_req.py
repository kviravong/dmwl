import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime

def create_dmwl():
    # Create a DMWL dataset
    ds = Dataset()

    # Patient information
    ds.PatientName = "John Doe"
    ds.PatientID = "123456"
    ds.PatientBirthDate = "19700101"
    ds.PatientSex = "M"
    ds.PatientComments = "No known allergies"

    # Study information
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.StudyDate = datetime.datetime.now().strftime("%Y%m%d")
    ds.StudyTime = datetime.datetime.now().strftime("%H%M%S")
    ds.AccessionNumber = "987654"
    ds.RequestedProcedureDescription = "MRI of knees - Suspected meniscus damage"

    # Scheduled procedure step
    ds.ScheduledProcedureStepStartDate = datetime.datetime.now().strftime("%Y%m%d")
    ds.ScheduledProcedureStepStartTime = datetime.datetime.now().strftime("%H%M%S")
    ds.Modality = "MR"
    ds.ScheduledStationAETitle = "NAT_HOSP_RAD"  # Shortened to fit within 16 characters
    ds.ScheduledProcedureStepDescription = "MRI of knees"
    ds.ScheduledProcedureStepID = "MRI_KNEES_001"
    ds.ScheduledStationName = "Radiology Ward"
    ds.ScheduledPerformingPhysicianName = "Dr. Smith"

    # Create a FileDataset (DMWL file)
    file_meta = pydicom.dataset.Dataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.31"  # Correct UID for Modality Worklist Information Model - FIND
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    filename_dcm = "dmwl.dcm"
    filename_txt = "dmwl.txt"
    
    ds = FileDataset(filename_dcm, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # Add the dataset attributes to the FileDataset
    ds.update({
        'PatientName': "John Doe",
        'PatientID': "123456",
        'PatientBirthDate': "19700101",
        'PatientSex': "M",
        'PatientComments': "No known allergies",
        'StudyInstanceUID': pydicom.uid.generate_uid(),
        'StudyDate': datetime.datetime.now().strftime("%Y%m%d"),
        'StudyTime': datetime.datetime.now().strftime("%H%M%S"),
        'AccessionNumber': "987654",
        'RequestedProcedureDescription': "MRI of knees - Suspected meniscus damage",
        'ScheduledProcedureStepStartDate': datetime.datetime.now().strftime("%Y%m%d"),
        'ScheduledProcedureStepStartTime': datetime.datetime.now().strftime("%H%M%S"),
        'Modality': "MR",
        'ScheduledStationAETitle': "NAT_HOSP_RAD",
        'ScheduledProcedureStepDescription': "MRI of knees",
        'ScheduledProcedureStepID': "MRI_KNEES_001",
        'ScheduledStationName': "Radiology Ward",
        'ScheduledPerformingPhysicianName': "Dr. Smith"
    })

    # Save the DMWL file
    ds.save_as(filename_dcm)
    
    # Save the text values of the DMWL to a text file
    with open(filename_txt, 'w') as f:
        f.write(f"Patient Name: {ds.PatientName}\n")
        f.write(f"Patient ID: {ds.PatientID}\n")
        f.write(f"Patient Birth Date: {ds.PatientBirthDate}\n")
        f.write(f"Patient Sex: {ds.PatientSex}\n")
        f.write(f"Patient Comments: {ds.PatientComments}\n")
        f.write(f"Study Instance UID: {ds.StudyInstanceUID}\n")
        f.write(f"Study Date: {ds.StudyDate}\n")
        f.write(f"Study Time: {ds.StudyTime}\n")
        f.write(f"Accession Number: {ds.AccessionNumber}\n")
        f.write(f"Requested Procedure Description: {ds.RequestedProcedureDescription}\n")
        f.write(f"Scheduled Procedure Step Start Date: {ds.ScheduledProcedureStepStartDate}\n")
        f.write(f"Scheduled Procedure Step Start Time: {ds.ScheduledProcedureStepStartTime}\n")
        f.write(f"Modality: {ds.Modality}\n")
        f.write(f"Scheduled Station AE Title: {ds.ScheduledStationAETitle}\n")
        f.write(f"Scheduled Procedure Step Description: {ds.ScheduledProcedureStepDescription}\n")
        f.write(f"Scheduled Procedure Step ID: {ds.ScheduledProcedureStepID}\n")
        f.write(f"Scheduled Station Name: {ds.ScheduledStationName}\n")
        f.write(f"Scheduled Performing Physician Name: {ds.ScheduledPerformingPhysicianName}\n")

    print(f"DMWL file '{filename_dcm}' and text file '{filename_txt}' created successfully.")

if __name__ == "__main__":
    create_dmwl()
