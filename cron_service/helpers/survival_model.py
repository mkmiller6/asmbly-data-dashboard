import pickle

with open("./helpers/transform_pipeline.pkl", "rb") as f:
    transform_pipeline = pickle.load(f)

with open("./helpers/gbm_model.pkl", "rb") as f:
    survival_model = pickle.load(f)
