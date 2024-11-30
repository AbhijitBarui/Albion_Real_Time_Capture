import Quartz
import numpy as np
import cv2 as cv
from mss import mss
import subprocess


def get_window_by_name(target_title):
    # Get a list of all windows
    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)

    # Find the window with the matching title
    for window in windows:
        window_name = window.get('kCGWindowName', 'Unnamed')
        if 'albion' in window_name.lower():
            return window
    return None


def focus_window(title):
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


# Define the target window title
target_title = "Albion Online Client"

# Focus the window
if focus_window(target_title):
    print("Window focused successfully!")
else:
    print("Failed to focus the window.")

# Find the window
window = get_window_by_name(target_title)

if window:
    # Get the window's bounds
    bounds = window['kCGWindowBounds']
    left = int(bounds['X'])
    top = int(bounds['Y'])
    width = int(bounds['Width'])
    height = int(bounds['Height'])

    # Define the region for mss
    region = {"top": top, "left": left, "width": width, "height": height}
    print(f"Capture Region: {region}")

    # Capture the window using mss
    # Capture the window using mss
    with mss() as sct:
        while True:
            # Temporarily destroy OpenCV window
            cv.destroyWindow("Albion Online Client")
            
            # Capture the specific region
            screenshot = np.array(sct.grab(region))
            frame = cv.cvtColor(screenshot, cv.COLOR_BGRA2BGR)  # Drop alpha channel

            # Recreate the OpenCV window
            cv.imshow("Albion Online Client", frame)

            # Quit the loop when '1' is pressed
            if cv.waitKey(1) & 0xFF == ord('1'):
                break

    # Cleanup
    cv.destroyAllWindows()
else:
    print(f"Window with title '{target_title}' not found.")