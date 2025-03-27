import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime

# Define available modalities
modalities = [
    {"Modality": "MR", "StationName": "MRI_1", "AvailableTimes": ["08:00", "09:00", "10:00"]},
    {"Modality": "MR", "StationName": "MRI_2", "AvailableTimes": ["08:30", "09:30", "10:30"]},
    {"Modality": "PET", "StationName": "PET_CT_1", "AvailableTimes": ["08:00", "09:00", "10:00"]},
    {"Modality": "SCINT", "StationName": "SCINT_1", "AvailableTimes": ["08:00", "09:00", "10:00"]},
    {"Modality": "US", "StationName": "ULTRASOUND_1", "AvailableTimes": ["08:00", "09:00", "10:00"]},
    {"Modality": "DX", "StationName": "XRAY_1", "AvailableTimes": ["08:00", "09:00", "10:00"]}
]

# Define available staff
staff = [
    {"Name": "Dr. Smith", "Role": "Radiologist"},
    {"Name": "Dr. Johnson", "Role": "Radiologist"},
    {"Name": "Dr. Brown", "Role": "Radiologist"},
    {"Name": "Dr. Taylor", "Role": "Radiograph"},
    {"Name": "Dr. Anderson", "Role": "Radiograph"},
    {"Name": "Dr. Thomas", "Role": "Medical Physicist"},
    {"Name": "Dr. Jackson", "Role": "Medical Physicist"}
]

def read_dmwl(filename):
    # Read the DMWL file
    ds = pydicom.dcmread(filename)
    return ds

def get_modality_for_study(requested_procedure_description):
    # Determine the modality based on the requested procedure description
    if "MRI" in requested_procedure_description:
        return "MR"
    elif "PET" in requested_procedure_description:
        return "PET"
    elif "SCINT" in requested_procedure_description:
        return "SCINT"
    elif "ULTRASOUND" in requested_procedure_description:
        return "US"
    elif "XRAY" in requested_procedure_description:
        return "DX"
    else:
        raise ValueError("No suitable modality found for the requested procedure.")

def schedule_examination(ds):
    # Ensure Modality attribute is present
    if not hasattr(ds, 'Modality'):
        ds.Modality = get_modality_for_study(ds.RequestedProcedureDescription)

    # Find the first available modality and time
    for modality in modalities:
        if modality["Modality"] == ds.Modality:
            for time in modality["AvailableTimes"]:
                # Schedule the examination
                ds.ScheduledProcedureStepStartDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")
                ds.ScheduledProcedureStepStartTime = time.replace(":", "")
                ds.ScheduledStationName = modality["StationName"]
                modality["AvailableTimes"].remove(time)
                break
            break

    # Assign the first available staff
    for person in staff:
        if person["Role"] in ["Radiologist", "Radiograph", "Medical Physicist"]:
            ds.ScheduledPerformingPhysicianName = person["Name"]
            staff.remove(person)
            break

    return ds

def save_dmwl(ds, filename):
    # Save the altered DMWL file
    ds.save_as(filename)
    print(f"Altered DMWL file '{filename}' saved successfully.")

if __name__ == "__main__":
    # Read the original DMWL file
    original_filename = "dmwl.dcm"
    ds = read_dmwl(original_filename)

    # Schedule the examination
    ds = schedule_examination(ds)

    # Save the altered DMWL file
    altered_filename = "altered_dmwl.dcm"
    save_dmwl(ds, altered_filename)
