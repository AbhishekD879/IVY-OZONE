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
class Test_C492094_Verify_Remember_Last_Football_Tab_functionality_for_logged_in_user(Common):
    """
    TR_ID: C492094
    NAME: Verify Remember Last Football Tab functionality for logged in user
    DESCRIPTION: This test case verifies Remember Last Football Tab functionality for logged in user
    PRECONDITIONS: 1. User should be logged in
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

    def test_003_choose_in_play_tab(self):
        """
        DESCRIPTION: Choose 'In-Play' tab
        EXPECTED: * 'In-Play' tab is selected and highlighted
        EXPECTED: * Appropriate events are displayed on In-Play page
        """
        pass

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * 'In-Play' tab is still selected and highlighted
        EXPECTED: * Appropriate events are displayed on In-Play page
        """
        pass

    def test_005_navigate_to_homepage_or_other_areas_of_application(self):
        """
        DESCRIPTION: Navigate to Homepage or other areas of application
        EXPECTED: 
        """
        pass

    def test_006_return_to_football_landing_page(self):
        """
        DESCRIPTION: Return to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * In-Play tab is selected and highlighted
        EXPECTED: * Appropriate content is displayed for In-Play tab
        """
        pass

    def test_007_repeat_steps_3_6_for_the_next_tabs_matches_competitions_coupons_outrights_specials_jackpot(self):
        """
        DESCRIPTION: Repeat steps 3-6 for the next tabs:
        DESCRIPTION: * Matches
        DESCRIPTION: * Competitions
        DESCRIPTION: * Coupons
        DESCRIPTION: * Outrights
        DESCRIPTION: * Specials
        DESCRIPTION: * Jackpot
        EXPECTED: * Football Landing page is opened
        EXPECTED: * Previously chosen tab is displayed as selected and highlighted
        EXPECTED: * Appropriate content is displayed for selected tab
        """
        pass
