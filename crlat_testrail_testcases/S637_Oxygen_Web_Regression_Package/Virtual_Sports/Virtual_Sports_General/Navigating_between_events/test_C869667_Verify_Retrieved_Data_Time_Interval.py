import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869667_Verify_Retrieved_Data_Time_Interval(Common):
    """
    TR_ID: C869667
    NAME: Verify Retrieved Data Time Interval
    DESCRIPTION: This test case verifies that data are retrieved for the next 6 hours after sports page opening
    DESCRIPTION: Eg. Request URL: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForEvent/14672490,14672491,14672492,14672493,14672494,14672495,14672496,14672497,14672498,14672499,14672500,14672501,14672502,14672503,14672504,14672505,14672506,14672507,14672508,14672509,14672510,14672511,14672512,14672513,14672514,14672515,14672516,14672517,14672518,14672519,14672520,14672521,14672522,14672523,14672524,14672525,14672526,14672527,14672528,14672529,14672530,14672531,14672532,14672533,14672534,14672535,14672536,14672537,14672538,14672539,14672540,14672541,14672542,14672543,14672544,14672545,14672546,14672550,14672553,14672558,14672563,14672564,14672565,14672566,14672567,14672568,14672569,14672570,14672571,14672572,14672573,14672574?racingForm=outcome&prune=market&translationLang=en&responseFormat=json
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001___open_siteserve_request__check_start_timestart_date_for_the_first_event(self):
        """
        DESCRIPTION: - Open SiteServe request
        DESCRIPTION: - Check start time/start date for the first event
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_last_event_in_siteserve_request(self):
        """
        DESCRIPTION: Navigate to the last event in SiteServe request
        EXPECTED: 
        """
        pass

    def test_003_check_start_timestart_date_for_the_last_event_in_siteserve_request(self):
        """
        DESCRIPTION: Check start time/start date for the last event in SiteServe request
        EXPECTED: 
        """
        pass

    def test_004_compare_start_timestart_date_from_steps_2_and_4(self):
        """
        DESCRIPTION: Compare start time/start date from steps №2 and №4
        EXPECTED: - Data is retrieved for 6 hours
        EXPECTED: - Nubber of events displayed according to CMS config
        """
        pass

    def test_005_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis,
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
