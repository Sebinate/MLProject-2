from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_test_file_path: str
    invalid_train_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessor_obj_file_path: str

@dataclass
class ClassificationMetricsArtifact:
    f1_score: str
    accuracy: str
    recall: str
    precession: str

@dataclass
class ModelTrainingArtifact:
    model_saved_file_path: str
    train_metric_artifact: ClassificationMetricsArtifact
    test_metric_artifact: ClassificationMetricsArtifact
