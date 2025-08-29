import pytest
from wizz_main.constants import flight_constants, error_constants


@pytest.mark.round_trip_flight_regression
@pytest.mark.test3
@pytest.mark.parametrize("loadData", [("test_data", "test3", 1)], indirect=True)
def test_3_round_trip_with_missing_return_date(common,request, loadData):
    # test Data
    test_name="test_3_round_trip_with_missing_return_date"

    test_folder = "test 3"

    adult_pax = int(loadData["adult_pax"])
    run = loadData["run_num"]
    departure_date = loadData["departure_date"]



    origin = flight_constants.VIENNA
    destination = flight_constants.NICE
    expected_no_return_date_error_message = error_constants.NO_RETURN_DATE_ERROR

    # Set up logger
    test_logger = common.get_test_logger("test3_run"+run)
    common.home.log = test_logger
    common.show_flights.log = test_logger

    # Accept required cookies
    common.home.accept_necessary_cookies()

    # Enter flight origin and flight destination
    common.home.enter_origin_via_enter(origin)
    common.home.enter_destination_via_enter(destination)

    # Enter departure date but no return date
    common.home.enter_date(type = "departure",date = departure_date)
    common.home.enter_date(type = "return",date = None)
    common.home.take_screenshot(test_name+"_noReturnDate", test_folder, "partial",request=request)

    # Select Passenger Type and Pax
    common.homepage.passenger_input_box.click()
    common.home.select_pax(passenger="Adults", desired_pax=adult_pax)

    # Click Search Flight/Start Booking
    common.home.goto_flight_lists()

    #Wait for Error element to appear and Assert if error message is correct
    common.wait_for_visibility(locator=common.homepage.error_no_return_date, timeout=10000)

    common.assert_element(
        condition=common.homepage.error_no_return_date.text_content().lower() == expected_no_return_date_error_message.lower(),
        success_msg=f"Correct Error Message: {common.homepage.error_no_return_date.text_content()}",
        failure_msg=f"Wrong Error Message: \tExpected:{expected_no_return_date_error_message} \tActual:{common.homepage.error_no_return_date.text_content()}",
        failure_screenshot_name=test_name+"_incorrectError",
        test_folder=test_folder,
        whole_partial="partial",
        request=request
    )
    common.home.take_screenshot(test_name+"_errorMessage", test_folder, "partial",request=request)