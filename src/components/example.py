models = {
                "Random Forest": 1,
                "Decision Tree": 2,
                "Gradient Boosting": 3,
                "Linear Regression": 4,
                "XGBRegressor": 5,
                "CatBoosting Regressor": 6,
                "AdaBoost Regressor": 7,
            }

print(max(zip(models.values(), models.keys())))