from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QTransform


class Animation:
    def __init__(
        self,
        path,
        frame_width=None,
        frame_height=None,
        size=160,
        columns=None,
        rows=None
    ):
        self.frames = []
        self.flipped_frames = []

        path = Path(path)

        if path.is_dir():
            files = sorted(path.glob("*.png"))
            for file in files:
                self.frames.append(self.prepare_frame(QPixmap(str(file)), size))
        else:
            sheet = QPixmap(str(path))
            if columns is not None and rows is not None:
                self.frames.extend(
                    self.load_spritesheet_grid(sheet, columns, rows, size)
                )
            elif frame_width is None or frame_height is None:
                self.frames.append(self.prepare_frame(sheet, size))
            else:
                self.frames.extend(
                    self.load_spritesheet(sheet, frame_width, frame_height, size)
                )

        if not self.frames:
            raise ValueError(f"No animation frames found in {path}")

        self.flipped_frames = [
            frame.transformed(
                QTransform().scale(-1, 1),
                Qt.SmoothTransformation
            )
            for frame in self.frames
        ]
        self.index = 0

    def load_spritesheet(self, sheet, frame_width, frame_height, size):
        frames = []
        columns = sheet.width() // frame_width
        rows = sheet.height() // frame_height

        for row in range(rows):
            for column in range(columns):
                frame = sheet.copy(
                    column * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )

                if not frame.isNull() and not self.is_empty_frame(frame):
                    frames.append(self.prepare_frame(frame, size))

        return frames

    def load_spritesheet_grid(self, sheet, columns, rows, size):
        frames = []

        for row in range(rows):
            top = round(row * sheet.height() / rows)
            bottom = round((row + 1) * sheet.height() / rows)

            for column in range(columns):
                left = round(column * sheet.width() / columns)
                right = round((column + 1) * sheet.width() / columns)
                frame = sheet.copy(
                    left,
                    top,
                    right - left,
                    bottom - top
                )

                if not frame.isNull() and not self.is_empty_frame(frame):
                    frames.append(self.prepare_frame(frame, size))

        return frames

    def is_empty_frame(self, frame):
        image = frame.toImage()

        for y in range(image.height()):
            for x in range(image.width()):
                if image.pixelColor(x, y).alpha() > 0:
                    return False

        return True

    def prepare_frame(self, frame, size):
        scaled = frame.scaled(
            size,
            size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        canvas = QPixmap(size, size)
        canvas.fill(Qt.transparent)

        painter = QPainter(canvas)
        painter.drawPixmap(
            (size - scaled.width()) // 2,
            size - scaled.height(),
            scaled
        )
        painter.end()

        return canvas

    def next_frame(self, mirrored=False):
        frames = self.flipped_frames if mirrored else self.frames
        frame = frames[self.index]

        self.index = (self.index + 1) % len(self.frames)

        return frame
