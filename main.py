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
        # Command to record screen with ffmpeg on macOS
        # Using AVFoundation (macOS screen capture backend)
        command = [
            "ffmpeg",
            "-f",
            "avfoundation",
            "-i",
            "3:none",  # <--- Changed from "0" to "3:none"
            "-vcodec",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-preset",
            "ultrafast",
            "-r",
            "60",  # 60 fps
            "-y",  # Overwrite output
            self.output_file,
        ]

        # We redirect stderr to a pipe so we can read why it crashed if it fails
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give it a moment to initialize the screen capture session
        time.sleep(2)

        # Check if it crashed immediately (e.g. permission denied)
        if self.process.poll() is not None:
            err = self.process.stderr.read().decode()
            print(f"FFMPEG failed to start: {err}")

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
    def __init__(self, left_key="a", right_key="d"):
        self.recorder = None
        # Allow user to define their own keybinds
        self.left_key = left_key
        self.right_key = right_key

    def record_pattern(self, sequence, output_dir="patterns"):
        os.makedirs(output_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        video_file = os.path.join(output_dir, f"pattern_{timestamp}.mp4")
        gif_file = os.path.join(output_dir, f"pattern_{timestamp}.gif")

        self.recorder = ScreenRecorder(video_file)
        self.recorder.start_recording()

        for i in range(3, 0, -1):
            print(f"Recording in {i}...")
            time.sleep(1)

        print("Executing Pattern!")

        # Track execution time for the GIF trimmer
        start_time = time.time()
        self.simulate_pattern(sequence)
        total_time = time.time() - start_time

        time.sleep(1.5)  # Buffer to show the finished shape
        self.recorder.stop_recording()

        print(f"Converting to GIF...")
        # Add the buffer to the duration
        create_gif_from_video(
            video_file, gif_file, start_time=0, duration=total_time + 2
        )
        return video_file, gif_file

    def simulate_pattern(self, sequence):
        """
        sequence: list of (direction, duration_ms)
        direction: 'l' or 'r'
        duration_ms: time to drive straight AFTER the turn
        """
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.0

        # Initialize the reference clock
        start_time = time.perf_counter()
        elapsed_target = 0.0

        for direction, duration_ms in sequence:
            # 1. Execute the turn immediately
            key = self.left_key if direction.lower() == "l" else self.right_key
            pyautogui.press(key)

            # 2. Update the cumulative target time
            # (Where we SHOULD be in the timeline)
            elapsed_target += duration_ms / 1000.0

            # 3. Calculate the necessary sleep to hit the next target
            current_time = time.perf_counter()
            actual_elapsed = current_time - start_time
            sleep_duration = elapsed_target - actual_elapsed

            # 4. Only sleep if we aren't already running behind
            if sleep_duration > 0:
                time.sleep(sleep_duration)
            else:
                # If sleep_duration is negative, the system lagged.
                # We skip sleeping to try and 'catch up' to the timeline.
                pass


# Example usage
if __name__ == "__main__":
    # Notation: (Direction, Delay until next turn)
    # This creates a tight "S" curve mazing pattern
    maze_notation = [
        ("l", 100),  # Turn left, drive for 200ms
        ("l", 100),  # Turn right, drive for 200ms
        ("l", 100),
        ("r", 1),
    ]

    # Initialize with your specific in-game binds
    recorder = RetrocyclesPatternRecorder(left_key="e", right_key="t")
    recorder.record_pattern(maze_notation)
