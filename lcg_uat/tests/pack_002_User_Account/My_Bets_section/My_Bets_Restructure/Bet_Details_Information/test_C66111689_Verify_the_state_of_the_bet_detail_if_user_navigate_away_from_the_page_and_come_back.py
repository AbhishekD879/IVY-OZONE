import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66111689_Verify_the_state_of_the_bet_detail_if_user_navigate_away_from_the_page_and_come_back(Common):
    """
    TR_ID: C66111689
    NAME: Verify the state of the bet detail  if user navigate away from the page and come back
    DESCRIPTION: This test case verify the state of the bet detail  if user navigate away from the page and come back
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_000_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_000_place_singlemutiple_bets__from_sportsraces(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from Sports/Races
        EXPECTED: Bets should be placed successfully
        """
        pass

    def test_000_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        pass

    def test_000_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Placed bet is displayed
        """
        pass

    def test_000_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        pass

    def test_000_expand_the_bet_details_and_check_the_state(self):
        """
        DESCRIPTION: Expand the bet details and check the state
        EXPECTED: Bet details area  should be expanded
        """
        pass

    def test_000_navigate_to_any_other_page_form_my_bets(self):
        """
        DESCRIPTION: Navigate to any other page form my bets
        EXPECTED: User should  navigate from my bets  to any other screen
        """
        pass

    def test_000_go_back_to_my_bets_open_tab_and_check_the_bet_detail_state(self):
        """
        DESCRIPTION: Go back to My bets open tab and check the bet detail state
        EXPECTED: Bet details should be in collapse state
        """
        pass

    def test_000_repeat_the_above_steps_for_cashout_tab(self):
        """
        DESCRIPTION: Repeat the above steps for cashout tab
        EXPECTED: 
        """
        pass
