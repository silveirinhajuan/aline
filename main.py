import random
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication, QLabel, QWidget

from animation import Animation


class Pet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)

        self.animations = {
            "walk": Animation("assets/walk/Aline-walk.png", 256, 256),
            "jump": Animation("assets/jump/Aline-jump.png", 256, 256),
            "idle": Animation("assets/idle/aline_idle.png", columns=4, rows=6),
        }
        self.state_durations = {
            "idle": (2, 6),
            "walk": (4, 10),
        }
        self.state = "idle"
        self.state_ticks_remaining = 0
        self.animation = self.animations[self.state]
        self.frame_interval = 6
        self.frame_tick = 0

        pixmap = self.animation.next_frame()
        self.current_pixmap = None
        self.set_pet_pixmap(pixmap)

        screen = QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()

        self.screen_width = geometry.width()
        self.screen_height = geometry.height()

        self.direction = 1
        self.speed = 2

        self.ground_y = (
            self.screen_height
            - self.height()
        )

        self.move(
            0,
            self.ground_y
        )
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)
        self.drag_position = None
        self.set_state(self.state)
    
    def animate(self):
        if self.drag_position is not None:
            self.update_animation_frame("jump")
            return

        self.state_ticks_remaining -= 1
        if self.state_ticks_remaining <= 0:
            self.choose_next_state()

        self.update_animation_frame(self.state)

        if self.state != "walk":
            return

        x = self.x()

        x += self.direction * self.speed

        if x <= 0:
            x = 0
            self.direction = 1

        elif x >= self.screen_width - self.width():
            x = self.screen_width - self.width()
            self.direction = -1

        self.move(
            x,
            self.ground_y
        )

    def choose_next_state(self):
        states = list(self.state_durations)
        states.remove(self.state)
        self.set_state(random.choice(states))

    def set_state(self, name):
        self.state = name
        min_seconds, max_seconds = self.state_durations[name]
        duration = random.uniform(min_seconds, max_seconds)
        self.state_ticks_remaining = round(duration * 1000 / self.timer.interval())
        self.update_animation_frame(name, force=True)

    def update_animation_frame(self, name, force=False):
        if self.animation is not self.animations[name]:
            self.animation = self.animations[name]
            self.animation.index = 0
            self.frame_tick = 0

        self.frame_tick += 1
        if not force and self.frame_tick < self.frame_interval:
            return

        self.frame_tick = 0
        self.set_pet_pixmap(
            self.animation.next_frame(mirrored=self.direction < 0)
        )

    def set_pet_pixmap(self, pixmap):
        if pixmap is self.current_pixmap:
            return

        bottom = self.y() + self.height()
        self.current_pixmap = pixmap
        self.label.setPixmap(pixmap)
        self.resize(
            pixmap.width(),
            pixmap.height()
        )
        self.label.resize(
            pixmap.width(),
            pixmap.height()
        )
        self.setMask(pixmap.mask())

        if hasattr(self, "screen_width") and hasattr(self, "screen_height"):
            max_x = self.screen_width - self.width()
            self.move(min(max(self.x(), 0), max_x), self.y())

            if self.drag_position is None:
                max_y = self.screen_height - self.height()
                self.ground_y = min(max(bottom - self.height(), 0), max_y)
                self.move(self.x(), self.ground_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if self.drag_position:
            pos = (
                event.globalPosition().toPoint()
                - self.drag_position
            )

            max_x = self.screen_width - self.width()
            max_y = self.screen_height - self.height()
            x = min(max(pos.x(), 0), max_x)
            y = min(max(pos.y(), 0), max_y)

            self.move(x, y)
            self.ground_y = y

    def mouseReleaseEvent(self, event):
        self.drag_position = None


app = QApplication(sys.argv)

pet = Pet()
pet.show()

sys.exit(app.exec())
