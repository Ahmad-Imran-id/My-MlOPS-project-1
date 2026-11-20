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

#all filepaths where transformed data is saved trainsfomed (train,test,object)
@dataclass
class DataTransformationArifacts:
    train_transformed_file_path:str
    test_transformed_file_path:str 
    obj_transformed_file_path:str #obj stands for object

@dataclass
class ClassificationMetricArtifact:
    accuracy_score:float
    f1_score:float
    precision_score:float
    recall_score:float
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str 
    metric_artifact:ClassificationMetricArtifact


