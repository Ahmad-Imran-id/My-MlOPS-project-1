from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_file_path:str
    test_file_path:str

#artifacts used for creating data_validation report
@dataclass
class DataValidationArtifacts:
    validation_status:bool
    error_message:str
    report_file_path:str

