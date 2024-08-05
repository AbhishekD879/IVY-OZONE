import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C60911193_Verify_the_display_of_5_A_Side_Showdown_button_in_My_Bets(Common):
    """
    TR_ID: C60911193
    NAME: Verify the display of 5-A-Side Showdown button in My Bets
    DESCRIPTION: This test case verifies the display of 5-A-Side Showdown button in My Bets > Open Bets
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: User should place 5-A side bets
    PRECONDITIONS: **Configurations for Leaderboard widget**
    PRECONDITIONS: 1: Home Page
    PRECONDITIONS: 2: Football Page
    PRECONDITIONS: 3: My Bets - Enable
    PRECONDITIONS: CMS admin user should be able to enable/ disable the above toggles
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_my_bet_section__open_bets(self):
        """
        DESCRIPTION: Navigate to My Bet section > Open Bets
        EXPECTED: User should be able to view the 5-A side bet placed
        """
        pass

    def test_003_validate_the_display_of_5_a_side_showdown_button_on_5_a_side_bets_only(self):
        """
        DESCRIPTION: Validate the display of 5-A-Side Showdown button on 5-A side bets only
        EXPECTED: * 5-A-Side Showdown button should be displayed
        EXPECTED: * Blue logo should be displayed
        EXPECTED: ![](index.php?/attachments/get/141834871)
        """
        pass

    def test_004_click_on_5_a_side_showdown_button(self):
        """
        DESCRIPTION: Click on 5-A-Side Showdown button
        EXPECTED: * User should be navigated to Showdown Lobby
        EXPECTED: * Click should be **GA tagged**
        """
        pass

    def test_005__place_byb_bet_navigate_to_open_bets_validate_the_display_of_5_a_side_showdown_button(self):
        """
        DESCRIPTION: * Place BYB bet
        DESCRIPTION: * Navigate to Open Bets
        DESCRIPTION: * Validate the display of 5-A-Side Showdown button
        EXPECTED: 5-A-Side Showdown button should not be displayed for BYB bets
        """
        pass

    def test_006__place_any_sport_or_racing_bet_navigate_to_open_bets_validate_the_display_of_5_a_side_showdown_button(self):
        """
        DESCRIPTION: * Place ANY Sport or Racing bet
        DESCRIPTION: * Navigate to Open Bets
        DESCRIPTION: * Validate the display of 5-A-Side Showdown button
        EXPECTED: 5-A-Side Showdown button should not be displayed
        """
        pass

    def test_007_validate_the_display_of_5_a_side_showdown_button_in_settled_bets(self):
        """
        DESCRIPTION: Validate the display of 5-A-Side Showdown button in Settled Bets
        EXPECTED: * Button should be removed once the bet is settled and moved to Settled Bets
        EXPECTED: * 5-A-Side Showdown button should not be displayed
        """
        pass

    def test_008_disable_my_bets_toggle_in_cms_and_validatecms__system_configuration__structure__fiveasideleaderboardwidget(self):
        """
        DESCRIPTION: Disable My bets toggle in CMS and Validate
        DESCRIPTION: CMS > System Configuration > Structure > FiveASideLeaderBoardWidget
        EXPECTED: * 5-A-Side Showdown button should not be displayed
        """
        pass
