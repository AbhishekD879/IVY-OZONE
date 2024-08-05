import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869707_Verify_Event_Start_Date_and_Time(Common):
    """
    TR_ID: C869707
    NAME: Verify Event Start Date and Time
    DESCRIPTION: This test case verifies that the data which is displayed for the event corresponds to the SiteServer response
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: List of relevant class id's:
    PRECONDITIONS: Horse Racing class id 285
    PRECONDITIONS: Greyhounds class id 286
    PRECONDITIONS: Football class id 287
    PRECONDITIONS: Motorsports class id 288
    PRECONDITIONS: Speedway class id 289
    PRECONDITIONS: Cycling class id 290
    PRECONDITIONS: Tennis class id 291
    PRECONDITIONS: Grand National class id 26604
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: The next event is displayed
        """
        pass

    def test_002_check_event_name(self):
        """
        DESCRIPTION: Check event name
        EXPECTED: Event name corresponds to the SiteServer response ('name' attribute)
        """
        pass

    def test_003_check_start_date_for_verified_event(self):
        """
        DESCRIPTION: Check start date for verified event
        EXPECTED: Start date corresponds to the SiteServer response (see 'startTime' attribute).
        EXPECTED: Date format: YYYY-MM-DD
        """
        pass

    def test_004_check_start_time_for_verified_event(self):
        """
        DESCRIPTION: Check start time for verified event
        EXPECTED: Event start time corresponds to SiteServer response (see 'startTime' attribute)).
        EXPECTED: Time format: HH:MM (timezone should be taken into consideration)
        """
        pass

    def test_005_repeat_steps_3_5_for_few_events(self):
        """
        DESCRIPTION: Repeat steps №3-5 for few events
        EXPECTED: Data is updated according to the event we navigated to
        """
        pass

    def test_006_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
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
