import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28845_Verify_Class_of_Race_displaying_on_Race_Event_Details_page(Common):
    """
    TR_ID: C28845
    NAME: Verify Class of Race displaying on Race Event Details page
    DESCRIPTION: This test case verifies Class of Race displaying on Race Event Details page
    DESCRIPTION: JIRA TIckets:
    DESCRIPTION: BMA-12171 HR Racecard - Display Class of race
    PRECONDITIONS: 1. Events with preset Class of Race parameter are available
    PRECONDITIONS: 2. To check Class of Race parameter use link: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.16/EventToOutcomeForEvent/*Event_ID*?translationLang=en&racingForm=outcome&racingForm=event
    PRECONDITIONS: EXAMPLE:
    PRECONDITIONS: racingFormEvent id="1" refRecordType="event" refRecordId="4251354" raceNumber="1" title="Ben Maiden Stakes (5) 2yo" overview="Full Intention has the form to make him hard to beat in maiden company but that's also been the case on his last two starts and he's been turned over at odds-on on each occasion. He still has to be taken seriously but Midaawi and SAINT EQUIANO will ensure he doesn't get things all his own way. The latter has the hood left off here but his second over 7f last time was an effort that suggested he wouldn't be long in going one better.[Paul Smith]" going="S" class="5" prize="3234.50" distance="Yards,1320," drawBias="H"/>
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_go_to_horse_racing_section(self):
        """
        DESCRIPTION: Go to Horse Racing section
        EXPECTED: 
        """
        pass

    def test_003_select_race_with_class_of_race_available_and_open_race_event_details_page(self):
        """
        DESCRIPTION: Select Race with Class of Race available and open Race Event Details page
        EXPECTED: Race Event Details page is opened
        """
        pass

    def test_004_verify_class_of_race_parameter_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify Class of Race parameter displaying on the page
        EXPECTED: Class of Race parameter is displayed next to the Race Place terms
        """
        pass

    def test_005_verify_value_for_class_of_race_parameter(self):
        """
        DESCRIPTION: Verify value for Class of Race parameter
        EXPECTED: Class of Race value  is taken from SiteServer data for selected event (See step 2 of Preconditions)
        """
        pass

    def test_006_select_event_with_not_set_class_of_race_parameter_and_open_event_details_page(self):
        """
        DESCRIPTION: Select event with not set Class Of Race parameter and open Event Details page
        EXPECTED: 
        """
        pass

    def test_007_verify_class_of_race_parameter_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify Class of Race parameter displaying on the page
        EXPECTED: Space is blank and name of the parameter with empty value is NOT displayed
        """
        pass
