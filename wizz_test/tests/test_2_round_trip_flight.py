import time
import pytest
from wizz_main.constants import flight_constants


@pytest.mark.round_trip_flight_regression
@pytest.mark.test2
@pytest.mark.parametrize("loadData", [("test_data", "test2", 1)], indirect=True)
def test_2_round_trip_flight(common,request, loadData):
    # test Data
    test_name = "test2_two_way_flight"
    test_folder = "test 2"

    adult_pax = int(loadData["adult_pax"])
    run = loadData["run_num"]
    departure_date = loadData["departure_date"]
    return_date = loadData["return_date"]

    origin = flight_constants.VIENNA
    destination = flight_constants.NICE

    # Set up logger
    test_logger = common.get_test_logger("test2_run" + run)
    common.home.log = test_logger
    common.show_flights.log = test_logger

    # Accept required cookies
    common.home.accept_necessary_cookies()

    # Enter flight origin and flight destination
    common.home.enter_origin_via_enter(origin)
    common.home.enter_destination_via_enter(destination)

    # Select departure and return Date
    common.home.enter_date(type = "departure",date=departure_date)
    common.home.enter_date(type = "return",date=return_date)

    # Select Passenger Type and Pax
    common.home.select_pax(passenger="Adults",desired_pax=adult_pax)

    # Take a screenshot of all inout
    common.home.take_screenshot(test_name+"_inputs", test_folder, "partial", request=request)

    # Proceed to Show Flights page
    common.home.goto_flight_lists()

    # Assert if user is redirected to Page showing Flights
    # that has inbound and outbound flights(to and from)
    time.sleep(5)
    common.assert_element(
        condition=common.show_flights_page.flight_selected_outbound.is_visible(),
        success_msg="Outbound Flight header is visible",
        failure_msg="The Outbound flight is not visible.",
        failure_screenshot_name="test2_round_trip_flight_no_outbound",
        test_folder=test_folder,
        whole_partial="whole",
        request=request
    )

    common.assert_element(
        condition= common.show_flights_page.flight_selected_return.is_visible(),
        success_msg="Return Flight header is visible.",
        failure_msg="The Return Flight is not visible.",
        failure_screenshot_name="test2_round_trip_flight_no_outbound",
        test_folder=test_folder,
        whole_partial="whole",
        request=request
    )

    common.assert_element(
        condition=common.show_flights.page.url == "https://www.wizzair.com/en-gb/booking/select-flight/VIE/NCE/2025-09-15/2025-10-18/1/0/0/null",
        success_msg="Redirected Page's URL is correct.",
        failure_msg="Redirected Page's URL is incorrect.",
        failure_screenshot_name="test2_round_trip_flight_no_return",
        test_folder=test_folder,
        whole_partial="partial",
        request=request
    )

    # Take screenshot of page redirection and Flights
    common.home.take_screenshot(test_name+"_ShowFlightsPage", test_folder, "whole",request=request)







