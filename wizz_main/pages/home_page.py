

class Homepage:
    def __init__(self, page):
        self.page = page
        """ one way flight"""
        self.one_way_flight_button = page.locator("//label[normalize-space()='One way']//preceding-sibling::input")
        self.origin_input_box = page.locator("#wa-autocomplete-input-7")
        self.destination_input_box = page.locator("#wa-autocomplete-input-9")
        self.departure_date_input_box = page.locator("//input[@placeholder='Departure']")
        self.start_booking_button = page.locator("//button[@data-test = 'flight-search-submit']")
        self.accept_all_cookies_button = page.locator("//button[@id='onetrust-accept-btn-handler']")
        self.return_date_input_box = page.locator("//input[@id='wa-input-122']")
        self.error_no_return_date = page.locator("//div[contains(@class,'error')]/strong")
        self.passenger_input_box = page.locator("//div [@aria-describedby ='pax-helper']")


    def date_selector(self, departure_date: str):
        return self.page.locator(f"span[aria-label='{departure_date}']")

    def passenger_section(self, passenger: str):
        return self.page.locator(f"//div[@aria-valuetext='{passenger}']")

    def passenger_value(self, passenger: str):
        return self.passenger_section(passenger).locator("xpath=.//input[@data-test='stepper-input']")

    def increase_passenger_count(self, passenger: str):
        return self.passenger_section(passenger).locator("xpath=.//button[contains(@data-test, 'increase')]")

    def decrease_passenger_count(self, passenger: str):
        return self.passenger_section(passenger).locator("xpath=.//button[contains(@data-test, 'decrease')]")


