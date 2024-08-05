import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2594315_Verify_Football_Event_Details_page_Header(Common):
    """
    TR_ID: C2594315
    NAME: Verify Football Event Details page Header
    DESCRIPTION: This test case verifies header on Football EDP (event details page)
    PRECONDITIONS: You can find New Designs here:
    PRECONDITIONS: https://app.zeplin.io/project/5c86355fe1c597198e2a34f9/dashboard
    PRECONDITIONS: To retrieve information about event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note! Oxygen header is shown in case Opta Scoreboard isn't mapped to event** (status code 404 (not found) is received in response to **<OpenBet event id>?&api-key=COMc368624411e44b6e80e83c5a7f7c03c8** request)
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. This case should be confirmed for all sports.
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_football_in_play_event(self):
        """
        DESCRIPTION: Navigate to EDP of football in-play event
        EXPECTED: * EDP is loaded
        EXPECTED: * Oxygen header is present
        """
        pass

    def test_002_verify_elements_within_header(self):
        """
        DESCRIPTION: Verify elements within header
        EXPECTED: Header contains:
        EXPECTED: - 'Live' label and event 'start time' in one line
        EXPECTED: - Event name in second line
        EXPECTED: - Watch icon (as access point to watch stream)
        EXPECTED: - Done icon (If the user taps on the Done button
        EXPECTED: then user should see sub header return to original state with Watch icon)
        EXPECTED: - Notifications icon (if the event has  match notification available the user can see the bell icon for notifications, only on Wrappers)
        """
        pass

    def test_003_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify Event start date/time
        EXPECTED: * Event start date corresponds to **startTime** attribute
        EXPECTED: * Event start time/date is shown in the following format: 24 hours - DD/MM/YY. E.g. 19:30 - 26/02/18
        """
        pass

    def test_004_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: * Event name corresponds to **name** attribute
        EXPECTED: * Long event name is displayed in 2 lines; text is centered
        """
        pass

    def test_005_navigate_to_edp_of_football_pre_match_event(self):
        """
        DESCRIPTION: Navigate to EDP of football pre-match event
        EXPECTED: * EDP is loaded
        EXPECTED: * Oxygen header is present
        """
        pass

    def test_006_verify_elements_within_header(self):
        """
        DESCRIPTION: Verify elements within header
        EXPECTED: Header contains:
        EXPECTED: - 'Live' label and event 'start time' in one line
        EXPECTED: - Event name in second line
        EXPECTED: - Watch icon (as access point to watch stream)
        EXPECTED: - Done icon (If the user taps on the Done button
        EXPECTED: then user should see sub header return to original state with Watch icon)
        EXPECTED: - Notifications icon (if the event has  match notification available the user can see the bell icon for notifications, only on Wrappers)
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_008_navigate_to_edp_of_football_outrights_event_and_verify_header(self):
        """
        DESCRIPTION: Navigate to EDP of football Outrights event and verify header
        EXPECTED: Header contains:
        EXPECTED: - Event 'start time' in one line
        EXPECTED: - Event name in second line
        """
        pass

    def test_009_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_010_navigate_to_edp_of_football_specials_event_and_verify_header(self):
        """
        DESCRIPTION: Navigate to EDP of football Specials event and verify header
        EXPECTED: Header contains:
        EXPECTED: - Event 'start time' in one line
        EXPECTED: - Event name in second line
        """
        pass

    def test_011_verify_that_red_bar_is_not_displayed_on_the_ui(self):
        """
        DESCRIPTION: Verify that red bar is not displayed on the UI
        EXPECTED: Red bar should be absent on UI(it was situated below the scoreboard on EDP)
        EXPECTED: Design(https://app.zeplin.io/project/5c86355fe1c597198e2a34f9/screen/5d2f2aaafd92de63c05f3ba9 )
        """
        pass

    def test_012_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass
