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
class Test_C492472_Verify_Remember_Last_Football_Tab_functionality_after_Login_with_Different_User(Common):
    """
    TR_ID: C492472
    NAME: Verify Remember Last Football Tab functionality after Login with Different User
    DESCRIPTION: This test case verifies Remember Last Football Tab functionality after Login with Different User
    PRECONDITIONS: 1. All cookies and cache are cleared
    PRECONDITIONS: 2. User is logged out
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

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_log_into_app(self):
        """
        DESCRIPTION: Log into app
        EXPECTED: User is successfully logged in
        """
        pass

    def test_003_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * Matches tab is selected by default and highlighted
        """
        pass

    def test_004_choose_in_play_tab(self):
        """
        DESCRIPTION: Choose 'In-Play' tab
        EXPECTED: * 'In-Play' tab is selected and highlighted
        EXPECTED: * Appropriate events are displayed on In-Play page
        """
        pass

    def test_005_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: * User is successfully logged out
        EXPECTED: * User is redirected to Homepage
        """
        pass

    def test_006_log_into_app_with_another_user_that_has_never_visited_football_landing_page_before_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app with ANOTHER user that has never visited Football Landing page before and return to Football Landing page
        EXPECTED: * User is successfully logged in
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Matches' tab is selected and highlighted
        EXPECTED: * Appropriate content is displayed for 'Matches' tab
        """
        pass

    def test_007_choose_any_tab_except_in_play_and_matches(self):
        """
        DESCRIPTION: Choose any tab except 'In-Play' and 'Matches'
        EXPECTED: * Tab is selected and highlighted
        EXPECTED: * Appropriate content is displayed for selected tab
        """
        pass

    def test_008_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: * User is successfully logged out
        EXPECTED: * User is redirected to Homepage
        """
        pass

    def test_009_log_into_app_with_user_from_step_2_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app with user from step 2 and return to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'In-Play' tab is selected and highlighted
        EXPECTED: * Appropriate content is displayed for 'In-Play' tab
        """
        pass

    def test_010_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: * User is successfully logged out
        EXPECTED: * User is redirected to Homepage
        """
        pass

    def test_011_log_into_app_with_user_from_step_6_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app with user from step 6 and return to Football Landing page
        EXPECTED: * User is successfully logged in
        EXPECTED: * Football Landing page is opened
        EXPECTED: * Tab from step 7 is selected and highlighted
        EXPECTED: * Appropriate content is displayed for selected tab
        """
        pass

    def test_012_repeat_steps_1_11_for_all_tabs_on_football_landing_page_matches_competitions_coupons_outrights_specials_jackpot_player_bets(self):
        """
        DESCRIPTION: Repeat steps 1-11 for all tabs on Football Landing page:
        DESCRIPTION: * Matches
        DESCRIPTION: * Competitions
        DESCRIPTION: * Coupons
        DESCRIPTION: * Outrights
        DESCRIPTION: * Specials
        DESCRIPTION: * Jackpot
        DESCRIPTION: * Player Bets
        EXPECTED: 
        """
        pass
