import Quartz
import numpy as np
import cv2 as cv
from mss import mss
import subprocess


class WindowCaptureMac:

    # Properties
    window_name = None
    bounds = None
    region = None

    def __init__(self, window_name):
        self.window_name = window_name.lower()

        # Focus the window
        if not self._focus_window(self.window_name):
            raise Exception(f"Failed to focus window: {window_name}")

        # Get the window details
        window = self._get_window_by_name(self.window_name)
        if not window:
            raise Exception(f"Window not found: {window_name}")

        # Extract window bounds
        self.bounds = window['kCGWindowBounds']
        self.region = {
            "top": int(self.bounds['Y']),
            "left": int(self.bounds['X']),
            "width": int(self.bounds['Width']),
            "height": int(self.bounds['Height']),
        }

    def _get_window_by_name(self, target_title):
        # Get a list of all windows
        windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)

        # Find the window with the matching title
        for window in windows:
            window_name = window.get('kCGWindowName', 'Unnamed')
            if target_title in window_name.lower():
                return window
        return None

    def _focus_window(self, title):
        try:
            # Use AppleScript to focus the window by title
            script = f"""
            tell application "System Events"
                set frontmost of the first process whose name contains "{title}" to true
            end tell
            """
            subprocess.run(["osascript", "-e", script], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_screenshot(self):
        # Capture the specified region
        with mss() as sct:
            screenshot = np.array(sct.grab(self.region))
            frame = cv.cvtColor(screenshot, cv.COLOR_BGRA2BGR)  # Drop alpha channel
            return frame

    def list_window_names(self):
        # List all open windows and their names
        windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)
        for window in windows:
            print(window.get('kCGWindowName', 'Unnamed'))

    @staticmethod
    def display_screenshot(window_name, screenshot):
        cv.imshow(window_name, screenshot)

    def get_screen_position(self, pos):
        return (pos[0] + self.region['left'], pos[1] + self.region['top'])


if __name__ == "__main__":
    # Define the target window title
    target_window = "Albion Online Client"

    # Initialize the WindowCapture class
    try:
        wincap = WindowCaptureMac(target_window)

        # Create OpenCV window
        display_window_name = target_window
        cv.namedWindow(display_window_name)
        cv.moveWindow(display_window_name, wincap.region["left"] + wincap.region["width"] + 10, wincap.region["top"])

        while True:
            # Get updated screenshot
            screenshot = wincap.get_screenshot()

            # Display the screenshot
            WindowCaptureMac.display_screenshot(display_window_name, screenshot)

            # Quit the loop when 'q' is pressed
            if cv.waitKey(1) == ord('q'):
                break

        # Cleanup
        cv.destroyAllWindows()

    except Exception as e:
        print(f"Error: {e}")