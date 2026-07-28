import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


class VideoComposer:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.fps = 30

    def create_background(self, title: str):
        """
        Creates a background PNG with the episode title.
        """

        img = Image.new(
            "RGB",
            (self.width, self.height),
            (20, 20, 20),
        )

        draw = ImageDraw.Draw(img)

        font_path = r"C:\Windows\Fonts\arial.ttf"

        try:
            font = ImageFont.truetype(font_path, 72)
        except Exception:
            font = ImageFont.load_default()

        # Wrap title if it's too long
        words = title.split()
        lines = []
        current = ""

        for word in words:
            test = current + (" " if current else "") + word

            if draw.textlength(test, font=font) < self.width - 120:
                current = test
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

        line_height = 90
        start_y = 120

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]

            x = (self.width - text_width) // 2

            draw.text(
                (x, start_y),
                line,
                fill="white",
                font=font,
            )

            start_y += line_height

        background_path = tempfile.mktemp(suffix=".png")
        img.save(background_path)

        return background_path

    def compose(
        self,
        audio_path,
        output_path,
        title="AI Generated Podcast",
    ):

        background = self.create_background(title)

        try:

            cmd = [
                "ffmpeg",
                "-hide_banner",
                "-y",

                # background
                "-loop", "1",
                "-i", background,

                # audio
                "-i", audio_path,

                "-filter_complex",
                (
                    "[1:a]"
                    f"showwaves=s={self.width}x600:"
                    f"mode=cline:"
                    f"rate={self.fps}:"
                    "colors=0x00D4FF"
                    "[waves];"

                    "[0:v][waves]"
                    "overlay=0:(H-h)/2"
                    "[v]"
                ),

                "-map", "[v]",
                "-map", "1:a",

                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "medium",

                "-c:a", "aac",

                "-shortest",

                output_path,
            ]

            print("\nRunning FFmpeg...\n")
            print(" ".join(cmd))
            print()

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            print(result.stdout)
            print(result.stderr)

            result.check_returncode()

        finally:

            if os.path.exists(background):
                os.remove(background)

        return output_path