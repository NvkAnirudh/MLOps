import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import Trainer, TrainerConfig

from sklearn.model_selection import train_test_split
from dataclasses import dataclass



@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Started data ingestion component")
        try:
            df = pd.read_csv("notebook/data/StudentsPerformance.csv")  
            df.rename(columns={'race/ethnicity':'race_ethnicity', 'parental level of education':'parental_level_of_education', 'test preparation course':'test_preparation_course','math score':'math_score',
                   'reading score':'reading_score', 'writing score':'writing_score'}, inplace=True)          
            logging.info("Read the required data as pandas dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Initiating train test split")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data Ingestion is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    di = DataIngestion()
    train_path, test_path = di.initiate_data_ingestion()

    # Performing DataTransformation
    dt = DataTransformation()
    train_arr, test_arr, _ = dt.initiate_data_transformation(train_path, test_path)

    # Model Training
    model_trainer = Trainer()
    r2_score = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(r2_score)

