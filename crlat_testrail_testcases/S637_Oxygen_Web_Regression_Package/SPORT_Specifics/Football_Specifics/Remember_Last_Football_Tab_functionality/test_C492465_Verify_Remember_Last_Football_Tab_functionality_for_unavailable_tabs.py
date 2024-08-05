import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C492465_Verify_Remember_Last_Football_Tab_functionality_for_unavailable_tabs(Common):
    """
    TR_ID: C492465
    NAME: Verify Remember Last Football Tab functionality for unavailable tabs
    DESCRIPTION: This test case verifies Remember Last Football Tab functionality for unavailable tabs
    PRECONDITIONS: 1) User should be logged in
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) To get info for event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to verify remembered football tab for particular user go to:
    PRECONDITIONS: Dev Tools -> Application -> Local Storage ->"key" column: **OX./football-tab-{username}** and "value" column: **"{tabname}"**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * Matches tab is selected by default and highlighted
        """
        pass

    def test_003_choose_specials_tab(self):
        """
        DESCRIPTION: Choose 'Specials' tab
        EXPECTED: * 'Specials' tab is selected and highlighted
        EXPECTED: * Appropriate content is  displayed on Specials page
        """
        pass

    def test_004_navigate_to_homepage_or_other_areas_of_application(self):
        """
        DESCRIPTION: Navigate to Homepage or other areas of application
        EXPECTED: 
        """
        pass

    def test_005_trigger_situation_that_tab_from_step_3_is_no_longer_available(self):
        """
        DESCRIPTION: Trigger situation that tab from step 3 is no longer available
        EXPECTED: 
        """
        pass

    def test_006_return_to_football_landing_page(self):
        """
        DESCRIPTION: Return to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Specials' tab is no longer available
        EXPECTED: * 'Matches' tab is selected and highlighted
        EXPECTED: * Appropriate content is displayed for Matches tab
        """
        pass

    def test_007_trigger_situation_that_tab_from_step_3_is_available_again(self):
        """
        DESCRIPTION: Trigger situation that tab from step 3 is available again
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_3(self):
        """
        DESCRIPTION: Repeat steps 1-3
        EXPECTED: * 'Specials' tab is selected and highlighted
        EXPECTED: * Appropriate content is  displayed on Specials page
        """
        pass

    def test_009_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: * User is successfully logged out
        EXPECTED: * User is redirected to Homepage
        """
        pass

    def test_010_trigger_situation_that_tab_from_step_3_is_no_longer_available(self):
        """
        DESCRIPTION: Trigger situation that tab from step 3 is no longer available
        EXPECTED: 
        """
        pass

    def test_011_log_into_app_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app and return to Football Landing page
        EXPECTED: * User is successfully logged in
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Specials' tab is no longer available
        EXPECTED: * 'Matches' tab is selected and highlighted
        EXPECTED: * Appropriate content is displayed for Matches tab
        """
        pass

    def test_012_repeat_steps_1_11_for_jackpot_tab(self):
        """
        DESCRIPTION: Repeat steps 1-11 for 'Jackpot' tab
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Jackpot' tab is no longer available
        EXPECTED: * 'Matches' tab is selected and highlighted
        EXPECTED: * Appropriate content is displayed for Matches tab
        """
        pass
