import os
from datetime import datetime

class ScreenshotUtils:
    def __init__(self, page):
        self.page = page
        self.screenshot_dir = r"C:\Users\Monica\PycharmProjects\wizz_air\screenshots"

    def take_screenshot(self, test_name: str, test_folder: str, whole_partial:str ,request=None):

        self.screenshot_dir = self.screenshot_dir+"\\"+test_folder
        os.makedirs((self.screenshot_dir), exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{test_name}_{today}.png"
        file_path = os.path.join(self.screenshot_dir, file_name)

        # Take screenshot
        if whole_partial =="whole":
            self.page.screenshot(path=file_path, full_page=True)
        else:
            self.page.screenshot(path=file_path, full_page=False)

        # Attach to pytest-html
        if request:
            request.node.screenshot_path = file_path

        return file_path
