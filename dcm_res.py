import pydicom
import os

def list_dicom_data(dicomdir_path, dicom_folder_path, report_filename):
    # Read the DICOMDIR file
    dicomdir = pydicom.dcmread(dicomdir_path)

    # Open the report file for writing
    with open(report_filename, 'w') as report_file:
        # List the DICOM data
        for patient_record in dicomdir.patient_records:
            patient_id = patient_record.PatientID if 'PatientID' in patient_record else 'Unknown'
            patient_name = patient_record.PatientName if 'PatientName' in patient_record else 'Unknown'
            patient_birth_date = patient_record.PatientBirthDate if 'PatientBirthDate' in patient_record else '2000-01-01'
            patient_sex = patient_record.PatientSex if 'PatientSex' in patient_record else 'Unknown'

            report_file.write(f"Patient ID: {patient_id}\n")
            report_file.write(f"Patient Name: {patient_name}\n")
            report_file.write(f"Patient Birth Date: {patient_birth_date}\n")
            report_file.write(f"Patient Sex: {patient_sex}\n")

            for study_record in patient_record.children:
                study_instance_uid = study_record.StudyInstanceUID if 'StudyInstanceUID' in study_record else 'Unknown'
                study_date = study_record.StudyDate if 'StudyDate' in study_record else 'Unknown'
                study_time = study_record.StudyTime if 'StudyTime' in study_record else 'Unknown'
                study_description = study_record.StudyDescription if 'StudyDescription' in study_record else 'Unknown'

                report_file.write(f"  Study Instance UID: {study_instance_uid}\n")
                report_file.write(f"  Study Date: {study_date}\n")
                report_file.write(f"  Study Time: {study_time}\n")
                report_file.write(f"  Study Description: {study_description}\n")

                for series_record in study_record.children:
                    series_instance_uid = series_record.SeriesInstanceUID if 'SeriesInstanceUID' in series_record else 'Unknown'
                    series_number = series_record.SeriesNumber if 'SeriesNumber' in series_record else 'Unknown'
                    series_description = series_record.SeriesDescription if 'SeriesDescription' in series_record else 'Unknown'

                    report_file.write(f"    Series Instance UID: {series_instance_uid}\n")
                    report_file.write(f"    Series Number: {series_number}\n")
                    report_file.write(f"    Series Description: {series_description}\n")

                    for image_record in series_record.children:
                        sop_instance_uid = image_record.SOPInstanceUID if 'SOPInstanceUID' in image_record else 'Unknown'
                        instance_number = image_record.InstanceNumber if 'InstanceNumber' in image_record else 'Unknown'

                        report_file.write(f"      SOP Instance UID: {sop_instance_uid}\n")
                        report_file.write(f"      Instance Number: {instance_number}\n")

                        # Convert MultiValue to string
                        referenced_file_id = "\\".join(image_record.ReferencedFileID) if 'ReferencedFileID' in image_record else 'Unknown'
                        
                        # Read the associated DICOM file
                        dicom_filename = os.path.join(dicom_folder_path, referenced_file_id)
                        if os.path.exists(dicom_filename):
                            dicom_data = pydicom.dcmread(dicom_filename)

                            # Write the DICOM data to the report file
                            for element in dicom_data:
                                report_file.write(f"        {element.tag}: {element.value}\n")
                        else:
                            report_file.write(f"        File not found: {dicom_filename}\n")

if __name__ == "__main__":
    dicomdir_path = "DICOMDIR"
    dicom_folder_path = ""
    report_filename = "radiological_report.txt"
    list_dicom_data(dicomdir_path, dicom_folder_path, report_filename)
