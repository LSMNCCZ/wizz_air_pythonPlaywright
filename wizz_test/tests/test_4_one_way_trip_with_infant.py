
import pytest
from wizz_main.constants import flight_constants


@pytest.mark.one_way_flight_regression
@pytest.mark.test4
@pytest.mark.parametrize("loadData", [("test_data", "test4", 1)], indirect=True)
def test_4_one_way_flight_with_infant(common,request,loadData):
    #test Data
    test_name=f"test_4_one_way_flight_with_infant"
    test_folder = "test 4"

    adult_pax = int(loadData["adult_pax"])
    run = loadData["run_num"]
    departure_date = loadData["departure_date"]
    infant_pax = int(loadData["infant_pax"])

    origin = flight_constants.VIENNA
    destination = flight_constants.NICE

    # Set up logger
    test_logger = common.get_test_logger("test4_run"+run)
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

    common.scroll("up", 200)
    # Select Passenger type and their pax
    common.home.select_pax("Adults", adult_pax)
    common.home.select_pax("Infants", infant_pax)



    # Assert if Infants increase button is disabled
    common.assert_element(
        condition=common.home.locators.increase_passenger_count("Infants").is_disabled(),
        success_msg="Infant Passenger increase button is correctly disabled.",
        failure_msg="The Infants passenger increase button is not disabled.",
        failure_screenshot_name=test_name+"_error_enabledIncrease",
        test_folder=test_folder,
        whole_partial="partial",
        request=request
    )


    common.home.take_screenshot(test_name+"_increaseDisabled", test_folder, "partial",request=request)