import pyautogui
import time
import subprocess
import os
from pathlib import Path


class ScreenRecorder:
    def __init__(self, output_file="retrocycles_recording.mp4"):
        self.output_file = output_file
        self.process: subprocess.Popen | None = None

    def start_recording(self):
        """Start screen recording using ffmpeg"""
        # First, get screen resolution
        width, height = pyautogui.size()

        # Command to record screen with ffmpeg on macOS
        # Using AVFoundation (macOS screen capture backend)
        command = [
            "ffmpeg",
            "-f",
            "avfoundation",
            "-i",
            "0",  # Screen 0, Audio 0 (no audio)
            "-vcodec",
            "libx264",
            "-preset",
            "ultrafast",
            "-r",
            "60",  # 60 fps
            "-crf",
            "28",  # Quality (lower = better, but larger files)
            "-y",  # Overwrite output
            self.output_file,
        ]

        self.process: subprocess.Popen = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(1)  # Give ffmpeg time to start

    def stop_recording(self):
        """Stop recording and save file"""
        if self.process and self.process is not None:
            assert isinstance(self.process, subprocess.Popen)
            self.process.stdin.write(b"q")  # Send quit command
            self.process.stdin.flush()
            self.process.wait()

    def capture_screenshot(self, filename="frame.png"):
        """Capture a single screenshot"""
        # Use macOS native screencapture command
        subprocess.run(["screencapture", "-x", filename])


def create_gif_from_video(
    video_file, output_gif, start_time=0, duration=5, fps=10, scale="320:-1"
):
    """
    Convert video to GIF using ffmpeg
    """
    command = [
        "ffmpeg",
        "-ss",
        str(start_time),
        "-i",
        video_file,
        "-t",
        str(duration),
        "-vf",
        f"fps={fps},scale={scale}",
        "-loop",
        "0",
        output_gif,
    ]

    subprocess.run(command, check=True)


class RetrocyclesPatternRecorder:
    def __init__(self):
        self.recorder = None

    def record_pattern(self, sequence, output_dir="patterns"):
        """
        Record a Retrocycles mazing pattern
        sequence: list of ("key", duration_ms) tuples
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate unique filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        video_file = os.path.join(output_dir, f"pattern_{timestamp}.mp4")
        gif_file = os.path.join(output_dir, f"pattern_{timestamp}.gif")

        # Start recording
        print(f"Starting recording to {video_file}")
        self.recorder = ScreenRecorder(video_file)
        self.recorder.start_recording()

        # Add countdown for user preparation
        for i in range(3, 0, -1):
            print(f"Recording in {i}...")
            time.sleep(1)

        print("Recording pattern!")

        # Simulate the pattern
        start_time = time.time()
        self.simulate_pattern(sequence)
        total_time = time.time() - start_time

        print(f"Pattern completed in {total_time:.2f} seconds")

        # Stop recording
        time.sleep(1)  # Brief pause at end
        self.recorder.stop_recording()

        # Convert to GIF
        print(f"Converting to GIF: {gif_file}")
        create_gif_from_video(
            video_file, gif_file, start_time=0, duration=total_time + 1
        )

        print(f"Done! Files: {video_file}, {gif_file}")
        return video_file, gif_file

    def simulate_pattern(self, sequence):
        """Simulate a sequence of key presses"""
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

        for key, duration_ms in sequence:
            # Press key down
            pyautogui.keyDown(key)

            # Wait for specified duration
            time.sleep(duration_ms / 1000.0)

            # Release key
            pyautogui.keyUp(key)

            # Small pause between moves
            time.sleep(0.05)


# Example usage
if __name__ == "__main__":
    # Define a mazing pattern (Left, Right, Left, Right)
    pattern = [
        ("left", 100),  # Hold left for 100ms
        ("right", 100),  # Hold right for 100ms
        ("left", 100),
        ("right", 100),
    ]

    recorder = RetrocyclesPatternRecorder()
    video, gif = recorder.record_pattern(pattern)

    print(f"Created: {video}")
    print(f"Created: {gif}")
