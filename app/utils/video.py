import os
import subprocess


class VideoComposer:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.fps = 30

    def compose(
        self,
        audio_path,
        output_path,
        title="AI Generated Podcast",
        segments=None,
    ):

        host_a_enable = []
        host_b_enable = []

        if segments:
            for segment in segments:
                expr = f"between(t,{segment['start']:.2f},{segment['end']:.2f})"

                if segment["speaker"] == "Host_A":
                    host_a_enable.append(expr)
                else:
                    host_b_enable.append(expr)

        host_a_enable = "+".join(host_a_enable) or "0"
        host_b_enable = "+".join(host_b_enable) or "0"
        
        if segments:
            print("\n========== SPEAKER TIMELINE ==========")

            for segment in segments:
                print(
                    f"{segment['speaker']} | "
                    f"{segment['start']:.2f}s -> "
                    f"{segment['end']:.2f}s | "
                    f"{segment['text']}"
                )

            print("======================================\n")

        assets_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
        )

        background = os.path.abspath(
            os.path.join(assets_dir, "background.jpg")
        )

        host_a_glow = os.path.abspath(
            os.path.join(assets_dir, "host_a_glow.png")
        )

        host_a = os.path.abspath(
            os.path.join(assets_dir, "host_a.png")
        )

        host_b_glow = os.path.abspath(
            os.path.join(assets_dir, "host_b_glow.png")
        )

        host_b = os.path.abspath(
            os.path.join(assets_dir, "host_b.png")
        )

        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-y",

            "-loop", "1",
            "-i", background,

            "-loop", "1",
            "-i", host_a_glow,

            "-loop", "1",
            "-i", host_a,

            "-loop", "1",
            "-i", host_b_glow,

            "-loop", "1",
            "-i", host_b,

            "-i", audio_path,

            "-filter_complex",
            (
                # Background
                "[0:v]"
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "gblur=sigma=10"
                "[bg];"

                # Dark overlay
                "[bg]"
                "drawbox=x=0:y=0:w=1080:h=1920:"
                "color=black@0.35:t=fill"
                "[dark];"

                # Glow A
                "[1:v]"
                "scale=560:-1"
                "[left_glow];"

                # Avatar A
                "[2:v]"
                "scale=520:-1"
                "[left];"

                # Glow B
                "[3:v]"
                "scale=635:-1"
                "[right_glow];"

                # Avatar B
                "[4:v]"
                "scale=595:-1"
                "[right];"

                # Background
                "[dark]"
                "[left_glow]"
                f"overlay=60:680:enable='{host_a_enable}'"
                "[tmp1];"

                "[tmp1]"
                "[right_glow]"
                f"overlay=480:660:enable='{host_b_enable}'"
                "[tmp2];"

                "[tmp2]"
                "[left]"
                "overlay=80:700"
                "[tmp3];"

                "[tmp3]"
                "[right]"
                "overlay=500:680"
                "[v]"
            ),

            "-map", "[v]",
            "-map", "5:a",

            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",

            "-c:a", "aac",
            "-b:a", "192k",

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

        return output_path