'''
This file is for data cleaning and feature engineering
'''

import sys
import os
import numpy as np
import pandas as pd 
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object 

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str = os.path.join("../../artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transfomer_object(self):
        try:
            numerical_columns = ['math_score', 'reading_score']
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline = Pipeline(
                steps = [
                    ("Imputer", SimpleImputer(strategy="median")),
                    ("Scaler", StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ("Imputer", SimpleImputer(strategy="most_frequent")),
                    ("OneHotEncoder", OneHotEncoder()),
                    ("Scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Handled missing values for both numerical and categorical features")
            logging.info("Numerical features are scaled")
            logging.info("Categorical features are encoded using OneHotEncoder")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Loaded train and test dataset")
            logging.info("Obtaining preprocessor object")

            preprocessing_obj = self.get_data_transfomer_object()

            target_column_name = 'writing_score'

            input_features_train = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train = train_df[target_column_name]

            input_features_test = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test = test_df[target_column_name]

            logging.info("Applying preprocessor object on training and testing dataframe")

            train_features = preprocessing_obj.fit_transform(input_features_train)
            test_features = preprocessing_obj.transform(input_features_test)

            train_data = np.c_[train_features, np.array(target_feature_train)]
            test_data = np.c_[test_features, np.array(target_feature_test)]

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            logging.info("Saved Preprocessing object successfully")

            return (
                train_data,
                test_data,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
        except Exception as e:
            raise CustomException(e)
