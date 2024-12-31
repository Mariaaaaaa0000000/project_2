from difflib import SequenceMatcher

from gamedata import GameData
from PIL import Image, ImageQt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget
from ui import Ui_WhoAmI


class WhoAmIApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WhoAmI()
        self.ui.setupUi(self)

        self.gamedata = GameData("ktoya/ridlles")
        self.currnet_game_data: dict = None
        self.current_image = None
        self.current_hints = None
        self.correct_answer = None
        self.current_hint_index = 0

        self.next_game()

        self.ui.checkButton.clicked.connect(self.check_answer)
        self.ui.giveUpButton.clicked.connect(self.give_up)

    def next_game(self):
        """Запускает следующую игру"""
        self.currnet_game_data = self.gamedata.next()
        if not self.currnet_game_data:
            self.ui.hintLabel.setText("Игра завершена! Больше вопросов нет")
            self.ui.imageLabel.clear()
            self.ui.checkButton.setEnabled(False)
            self.ui.giveUpButton.setEnabled(False)
            return

        self.current_image = self.currnet_game_data["image_path"]
        self.current_hints = self.currnet_game_data["hints"]
        self.currnet_crop = self.currnet_game_data["crops"]
        self.correct_answer = self.currnet_game_data["answer"]
        self.current_hint_index = 0
        self.attempts = 0

        self.update_image()
        self.update_hint()
        self.update_attempts()

    def update_image(self):
        """Обновляет изображение на экране"""
        self.ui.imageLabel.setPixmap(
            QPixmap.fromImage(
                ImageQt.ImageQt(
                    Image.open(self.current_image).crop(self.get_image_crop())
                )
            )
        )

    def get_image_crop(self):
        """Возвращает текущую область кропа изображения"""
        return self.currnet_crop[self.current_hint_index]

    def update_hint(self):
        """Обновляет текущий хинт"""
        self.ui.hintLabel.setText(
            f"Подсказка: {self.current_hints[self.current_hint_index]}"
            if self.current_hint_index < len(self.current_hints)
            else "Больше подсказок нет"
        )

    def update_attempts(self):
        """Обновляет количество попыток"""
        self.ui.attemptsLabel.setText(f"Попытки: {self.attempts}")

    def check_answer(self):
        """Проверяет ответ пользователя"""
        user_answer = self.ui.answerInput.text().strip().lower()
        similarity = SequenceMatcher(
            None, user_answer, self.correct_answer.lower()
        ).ratio()
        if similarity > 0.8:
            QMessageBox.information(
                self,
                "Победа!",
                f"Вы угадали!\nПравильный ответ: {self.correct_answer}\nКоличество попыток: {self.attempts}",
            )
            self.next_game()
        else:
            self.attempts += 1
            self.current_hint_index += 1
            if self.current_hint_index < len(self.current_hints):
                self.update_image()
                self.update_hint()
            else:
                self.ui.hintLabel.setText("Больше подсказок нет")
            self.update_attempts()

    def give_up(self):
        """Показывает правильный ответ и начинает следующую игру"""
        QMessageBox.information(
            self, "Ответ", f"Правильный ответ: {self.correct_answer}"
        )
        self.next_game()


def run():
    import sys

    app = QApplication(sys.argv)
    window = WhoAmIApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
