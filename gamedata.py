import os
import random

import ujson
from validator import DataValidator


class GameData:
    def __init__(self, path2riddles: str):
        self.path2riddles = path2riddles
        self.riddles = self._load_riddles()

    def _load_riddles(self):
        riddles = [
            os.path.join(self.path2riddles, riddle)
            for riddle in os.listdir(self.path2riddles)
            if os.path.isdir(os.path.join(self.path2riddles, riddle))
        ]
        if not riddles:
            raise ValueError("Папка с загадками пуста или структура неправильная.")
        return riddles

    def next(self):
        riddle_path = random.choice(self.riddles)
        image_path, json_path = DataValidator.validate_files(riddle_path)

        with open(json_path, "r", encoding="utf-8") as json_file:
            riddle_data = ujson.load(json_file)

        DataValidator.validate_json(riddle_data, riddle_path)

        return {
            "image_path": image_path,
            "hints": riddle_data["hints"],
            "crops": riddle_data["crops"],
            "answer": riddle_data["answer"],
        }
