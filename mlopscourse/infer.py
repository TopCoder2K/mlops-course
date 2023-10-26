import os
import pickle

import fire

from .data.prepare_dataset import load_dataset


class Inferencer:
    """
    Runs the chosen model on the test set of the dataset and calculates the R^2 metric.

    Attributes
    ----------
    model_type : str
        The type of model that was used for training. Should be "rf" for RandomForest
        and "cb" for CatBoost.
    ckpt : str
        The filename inside 'checkpoint/' to load the model from. Should also contain the
        the filename extension.
    """

    def __init__(self, model_type: str, ckpt: str) -> None:
        self.model_type = model_type
        self.ckpt = ckpt

    def infer(self) -> None:
        (
            X_test,
            y_test,
            _,
            _,
        ) = load_dataset(split="test")

        with open(f"checkpoints/{self.ckpt}", "rb") as f:
            model = pickle.load(f)
        print(f"Evaluating the {self.model_type} model...")
        y_preds = model.eval(X_test, y_test)

        os.makedirs("predictions", exist_ok=True)
        preds_name = self.ckpt.split(".")[0]
        y_preds.to_csv(f"predictions/{preds_name}_preds.csv")


if __name__ == "__main__":
    fire.Fire(Inferencer)
