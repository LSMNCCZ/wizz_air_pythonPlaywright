import time

import pytest

from conftest import loadData
from wizz_main.constants import flight_constants

@pytest.mark.one_way_flight_regression
@pytest.mark.test1
@pytest.mark.parametrize("loadData", [("test_data", "test1", 1)], indirect=True)
def test_1_one_way_flight(common,request,loadData):
    #test Data
    print()
    test_name = "test1_one_way_flight"
    test_folder = "test 1"

    adult_pax = int(loadData["adult_pax"])
    run = loadData["run_num"]
    departure_date = loadData["departure_date"]

    origin = flight_constants.VIENNA
    destination = flight_constants.NICE


    # Set up logger
    test_logger = common.get_test_logger("test1_run"+run)
    common.home.log = test_logger
    common.show_flights.log = test_logger


    # Accept cookies and select One way flight
    common.home.accept_necessary_cookies()

    # Click One wait Flight
    common.home.select_one_way_flight()

    # Enter origin and destination
    common.home.enter_origin_via_enter(origin)
    common.home.enter_destination_via_enter(destination)

    # Enter the departure date
    common.home.enter_date(type = "departure",date = departure_date)

    # Select what Passenger types you'll include and will increase/decrease
    common.home.select_pax("Adults",adult_pax)
    common.home.take_screenshot(test_name+"_input", test_folder, "partial", request=request)

    # Switch page(control) to the new tab and return it as show_flights with new page
    common.show_flights = common.show_flights.switch_to_new_page(
        action=common.home.goto_flight_lists
    )

    # Verify that the flight_selected_header is present
    # on the new tab to confirm correct redirection
    time.sleep(5)
    common.assert_element(
        condition=common.show_flights.locators.flight_selected_outbound.is_visible(),
        success_msg="Flight Outbound is visible on the new tab.",
        failure_msg="The flight Outbound was not visible on the new tab.",
        failure_screenshot_name=test_name+"noOutbound",
        test_folder = test_folder,
        whole_partial = "whole",
        request=request
    )
    #Verify correct URL
    common.assert_element(
        condition=common.show_flights.page.url == "https://www.wizzair.com/en-gb/booking/select-flight/VIE/NCE/2025-09-15/null/1/0/0/null",
        success_msg="Page URL is correct after redirection.",
        failure_msg="Page URL is incorrect after redirection.",
        failure_screenshot_name=test_name+"_failure_url",
        test_folder=test_folder,
        whole_partial="partial",
        request=request
    )
    #take screenshot as proof of redirection
    common.show_flights.take_screenshot(test_name+"_newPage",test_folder, "whole", request=request)












