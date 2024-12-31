import os

from exceptions import RiddleError


class DataValidator:

    @staticmethod
    def validate_files(riddle_path):
        image_path, json_path = None, None
        for file_name in os.listdir(riddle_path):
            file_path = os.path.join(riddle_path, file_name)
            if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = file_path
            elif file_name.lower() == "data.json":
                json_path = file_path

        if not image_path or not json_path:
            raise RiddleError(
                f"Ошибка при обработки загадки {riddle_path}. {'Изображение не найдено' if not image_path else 'JSON файл не найден'}"
            )

        return image_path, json_path

    @staticmethod
    def validate_json(json_data, riddle_path):
        assert isinstance(json_data, dict), "Некорректная структура JSON файла"
        assert riddle_path and isinstance(riddle_path, str), "Некорректный путь"
        required_keys = ["hints", "crops", "answer"]
        for key in required_keys:
            assert key in json_data, f"Нехватает '{key}' ключа в JSON файле"
            if key == "answer":
                assert isinstance(json_data[key], str), "Ответ должен быть строковым"
            else:
                assert isinstance(json_data[key], list), f"'{key}' должен быть списком"
