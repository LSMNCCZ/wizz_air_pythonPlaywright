from utilities.screen_capture import ScreenshotUtils
from wizz_main.pages.home_page import Homepage
from datetime import datetime
import time
import logging



class Home(ScreenshotUtils):
    def __init__(self, page, common, logger=None):
        super().__init__(page)
        self.page = page
        self.locators = Homepage(page)
        self.common = common
        self.log = logger or logging.getLogger(__name__)

    # Enter origin
    def enter_origin_via_enter(self, origin: str):
        try:
            self.locators.origin_input_box.fill(origin)
            self.page.keyboard.press("Enter")
            self.log.info(f"*** Entered origin: {origin} ***")
        except Exception as e:
            self.log.error(f"=== Failed to enter origin '{origin}': {e} ===")

    # Enter destination
    def enter_destination_via_enter(self, destination: str):
        try:
            self.locators.destination_input_box.fill(destination)
            self.page.keyboard.press("Enter")
            self.log.info(f"*** Entered destination: {destination} ***")
        except Exception as e:
            self.log.error(f"=== Failed to enter destination '{destination}': {e} ===")

    # Selecting Pax according to passenger Type
    def select_pax(self, passenger: str, desired_pax: int):

        self.log.info(f"*** Getting Current {passenger} Count ***")
        current_passengers_count = int(self.locators.passenger_value(passenger).input_value())

        self.log.info(f"*** Current {passenger} Count: {current_passengers_count} ***")
        if current_passengers_count < desired_pax:
            pax_to_increase = desired_pax - current_passengers_count
            for _ in range(pax_to_increase):
                try:
                    self.common.wait_for_clickable(self.locators.increase_passenger_count(passenger), 10000).click()
                    self.log.info("*** Clicked Increase Button ***")
                    self.log.info(f"=== Increased {passenger} count by 1, Current Count: {self.locators.passenger_value(passenger).input_value()} ===")
                except TimeoutError as e:
                    self.log.error(f"=== Failed to click increase button for {passenger}: {e} ====")
                except Exception as e:
                    self.log.error(f"===Unexpected error increasing {passenger}: {e}===")

        elif current_passengers_count > desired_pax:
            pax_to_decrease = current_passengers_count - desired_pax
            for _ in range(pax_to_decrease):
                try:
                    self.common.wait_for_clickable(self.locators.decrease_passenger_count(passenger), 10000 ).click()
                    self.log.info("*** Clicked Increase Button ***")
                    self.log.info(f"=== Decreased {passenger} count by 1, Current Count: {self.locators.passenger_value(passenger).input_value()} ===")
                except TimeoutError as e:
                    self.log.error(f"=== Failed to click decrease button for {passenger}: {e} ===")
                except Exception as e:
                    self.log.error(f"=== Unexpected error decreasing {passenger}: {e} ===")

    # Entering data according to Flight type
    def enter_date(self, type: str, date: str):
        try:
            if type.lower() == "departure":
                self.common.wait_for_clickable(self.locators.departure_date_input_box, 10000)
                self.locators.departure_date_input_box.click()
                self.log.info("*** Clicked departure date input box ***")

            if date is None:
                self.page.keyboard.press('Escape')
                self.log.info("*** No date provided, pressed Escape ***")
            else:
                parsed_date = datetime.strptime(date, "%d-%B-%Y")
                formatted_date = parsed_date.strftime("%A %d %B %Y")
                self.locators.date_selector(formatted_date).click()
                self.log.info(f"*** Selected date: {formatted_date} ***")
        except Exception as e:
            self.log.error(f"=== Failed to enter date '{date}' for '{type}': {e} ===")

    # Next page redirection
    def goto_flight_lists(self):
        try:
            self.locators.start_booking_button.click()
            self.log.info("*** Clicked Start Booking button ***")
        except Exception as e:
            self.log.error(f"=== Failed to go to flight lists: {e} ===")

    # Accepting necessary cookies
    def accept_necessary_cookies(self):
        try:
            self.common.wait_for_visibility(self.locators.accept_all_cookies_button, 10000)
            self.locators.accept_all_cookies_button.click()
            self.log.info("*** Accepted necessary cookies ***")
        except Exception as e:
            self.log.error(f"=== Failed to accept cookies: {e} ===")

    # Clicking radio Button for One way flight
    def select_one_way_flight(self):
        try:
            self.locators.one_way_flight_button.click()
            self.log.info("*** Selected one-way flight option ***")
        except Exception as e:
            self.log.error(f"=== Failed to select one-way flight: {e} ===")
