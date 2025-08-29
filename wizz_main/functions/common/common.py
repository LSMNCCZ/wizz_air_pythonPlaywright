import logging
import os
from utilities.screen_capture import ScreenshotUtils
from wizz_main.functions.home import Home
from wizz_main.functions.show_flights import ShowFlights
from wizz_main.pages.home_page import Homepage
from wizz_main.pages.show_flights_page import ShowFlightsPage
from playwright.sync_api import  Locator, TimeoutError
from pytest_html import extras

class Common(ScreenshotUtils):  # inherit screen capture
    def __init__(self, page):
        super().__init__(page)
        self.new_page = None
        self.original_page = page
        self.page = page

        self.home = Home(page=page, common=self)
        self.homepage = Homepage(page=self.page)
        self.show_flights_page = ShowFlightsPage(page=self.page)
        self.show_flights = ShowFlights(page=self.page,common=self)

        self.log = None

    # For Test Logger
    def get_test_logger(self, test_name: str, log_dir="C:\\Users\\Monica\\PycharmProjects\\wizz_air\\test_logs"):
        os.makedirs(log_dir, exist_ok=True)
        logger = logging.getLogger(test_name)
        logger.setLevel(logging.INFO)

        # Clear previous handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        # File handler
        log_file = os.path.join(log_dir, f"{test_name}.log")
        fh = logging.FileHandler(log_file, mode="w")
        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        self.log = logger
        return logger

    def wait_for_visibility(self, locator: Locator, timeout: int = 10000):
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return locator
        except TimeoutError:
            raise TimeoutError(f"Element {locator} not visible after {timeout} ms")

    def scroll_to_element(self, locator: Locator, timeout: int = 10000):
        try:
            locator.scroll_into_view_if_needed()
        except TimeoutError:
            raise TimeoutError(f"Element {locator} can't be scrolled to page view after {timeout} ms")

    def wait_for_clickable(self, locator: Locator, timeout: int = 10000):
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return locator
        except TimeoutError:
            raise TimeoutError(f"Element {locator} was not visible for clicking after {timeout} ms")

    def assert_element(
            self,
            condition: bool,
            success_msg: str,
            failure_msg: str,
            failure_screenshot_name: str = None,
            test_folder: str = "",
            whole_partial: str = "whole",
            request=None
    ):
        try:
            assert condition, failure_msg
            if self.log:
                self.log.info("=== "+success_msg+ " ===")
        except AssertionError:
            if self.log:
                self.log.error(f"=== {failure_msg} ===")
                self.take_screenshot(
                    test_name=failure_screenshot_name,
                    test_folder=test_folder,
                    whole_partial=whole_partial,
                    request=request)

            raise

    def scroll(self, direction: str = "down", pixels: int = 300):
        """Scroll the page in the given direction by a number of pixels."""
        direction = direction.lower()
        if direction == "up":
            self.page.evaluate(f"window.scrollBy(0, -{pixels});")
        elif direction == "down":
            self.page.evaluate(f"window.scrollBy(0, {pixels});")
        elif direction == "left":
            self.page.evaluate(f"window.scrollBy(-{pixels}, 0);")
        elif direction == "right":
            self.page.evaluate(f"window.scrollBy({pixels}, 0);")
        else:
            raise ValueError("Direction must be 'up', 'down', 'left', or 'right'")