from utilities.screen_capture import ScreenshotUtils
from wizz_main.pages.show_flights_page import ShowFlightsPage
import logging


class ShowFlights(ScreenshotUtils):
    def __init__(self, page, common, logger=None):
        super().__init__(page)
        self.page = page
        self.locators = ShowFlightsPage(page)
        self.log = logger or logging.getLogger(__name__)
        self.common = common

    def switch_to_new_page(self, action):
        try:
            self.log.info("*** Switching to new Page ***")

            page_context = self.page.context

            try:
                with page_context.expect_page() as new_page_info:
                    action()
                new_page = new_page_info.value
                self.log.info("=== New page opened successfully. ===")
            except Exception as e:
                self.log.error(f"Failed to open new page: {e}")
                raise

            try:
                new_page.wait_for_load_state()
                self.log.info("=== New page finished Loading ===")
            except Exception as e:
                self.log.error(f"New page failed to load: {e}")
                raise

            try:
                self.log.info("*** Closing previous page ***")
                self.page.close()
                self.log.info("=== Previous Page Closed ===")
            except Exception as e:
                self.log.error(f"=== Failed to close previous page: {e} ===")

            # Give the new page to ShowFlights Action and return it
            new_show_flights_page = ShowFlights(page=new_page, common=self.common, logger=self.log)
            self.log.info("*** Switched to new ShowFlights page*** ")
            return new_show_flights_page

        except Exception as e:
            self.log.error(f"=== switch_to_new_page encountered an error: {e} ===")
            raise