import numpy as np
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionOnScreenOnly
from Quartz.CoreGraphics import (
    CGWindowListCreateImage,
    CGRectMake,
    kCGWindowImageDefault,
    CGImageGetWidth,
    CGImageGetHeight,
    CGDataProviderCopyData,
    CGImageGetDataProvider,
)
import Quartz
from PIL import Image
import cv2


class WindowCapture:
    def __init__(self, window_name):
        self.window_name = window_name
        self.window_info = self.find_window_info(window_name)
        if not self.window_info:
            raise Exception(f"Window not found: {window_name}")

    def find_window_info(self, window_name):
        # Retrieve the list of active windows
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        for window in window_list:
            name = window.get("kCGWindowName", "")
            owner = window.get("kCGWindowOwnerName", "")
            if window_name in name or window_name in owner:
                bounds = window["kCGWindowBounds"]
                return {
                    "id": window["kCGWindowNumber"],
                    "bounds": bounds,
                }
        return None

    def get_screenshot(self):
        # Extract the window bounds
        bounds = self.window_info["bounds"]
        x = int(bounds["X"])
        y = int(bounds["Y"])
        width = int(bounds["Width"])
        height = int(bounds["Height"])
        window_bounds = CGRectMake(x, y, width, height)

        # Capture the screen for the specific window
        screenshot = CGWindowListCreateImage(
            window_bounds,
            kCGWindowListOptionOnScreenOnly,
            self.window_info["id"],
            kCGWindowImageDefault,
        )
        if screenshot is None:
            raise Exception("Failed to capture the window screenshot")

        # Extract raw pixel data
        provider = CGImageGetDataProvider(screenshot)
        data = CGDataProviderCopyData(provider)
        raw_data = np.frombuffer(data, dtype=np.uint8)

        # Get image dimensions
        img_width = CGImageGetWidth(screenshot)
        img_height = CGImageGetHeight(screenshot)

        # Reshape and convert to OpenCV BGR format
        pixel_data = raw_data.reshape((img_height, img_width, 4))  # RGBA format
        cv_image = cv2.cvtColor(pixel_data, cv2.COLOR_RGBA2BGR)
        return cv_image

    def list_window_names(self):
        # List all active windows
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        for window in window_list:
            name = window.get("kCGWindowName", "Unnamed")
            owner = window.get("kCGWindowOwnerName", "Unknown Owner")
            print(f"Window Name: {name}, Owner: {owner}")