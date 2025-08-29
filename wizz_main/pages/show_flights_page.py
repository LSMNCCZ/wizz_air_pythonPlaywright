from utilities.screen_capture import ScreenshotUtils


class ShowFlightsPage(ScreenshotUtils):
    def __init__(self, page):
        self.page = page
        self.flight_selected_outbound = page.locator("//div [contains(@data-test, 'outbound')]")
        self.flight_selected_return =  page.locator("//div [contains(@data-test, 'return')]")