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
class Test_C66132275_Verify_no_Show_Results_element_within_the_Bet_for_only_one_line_of_results_shown_in_open_settle(Common):
    """
    TR_ID: C66132275
    NAME: Verify no Show Results element within the Bet  for only one line of results shown in open/settle
    DESCRIPTION: This test case  verify no Show Results element within the Bet  for only one line of results shown in open/settle
    PRECONDITIONS: User should login successfully with valid credentials
    PRECONDITIONS: Lottos data should be available
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_000_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: Lotto' page is opened with following New elements:
        """
        pass

    def test_000_choose_your_lucky_dip(self):
        """
        DESCRIPTION: Choose Your Lucky Dip
        EXPECTED: Lucky dip pop up display with numbers
        """
        pass

    def test_000_lucky3lucky4lucky5(self):
        """
        DESCRIPTION: Lucky3/Lucky4/Lucky5
        EXPECTED: 
        """
        pass

    def test_000_click_on_any_of_number(self):
        """
        DESCRIPTION: Click on any of Number
        EXPECTED: User should able to select number and click on Add to line CTA
        """
        pass

    def test_000_check_the_data_added_to_the_line(self):
        """
        DESCRIPTION: Check the data added to the line
        EXPECTED: Selected numbers should be shown with line summary
        """
        pass

    def test_000_choose_your_draws_section(self):
        """
        DESCRIPTION: Choose your draws Section
        EXPECTED: User should able to select single draw
        """
        pass

    def test_000_select_number_week_from_weeks_section(self):
        """
        DESCRIPTION: Select number week from weeks section
        EXPECTED: User should able to select week 1
        """
        pass

    def test_000_click_on_add_to_bet_slip(self):
        """
        DESCRIPTION: Click on add to bet slip
        EXPECTED: Selections are added to bet slip
        """
        pass

    def test_000_enter_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: Enter stake and click on place bet
        EXPECTED: Bet should be placed successfully
        """
        pass

    def test_000_navigate_to_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Navigate to 'My Bets' item on Top Menu
        EXPECTED: My Bets' page/'Bet Slip' widget is opened
        """
        pass

    def test_000_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: Check for the Lotto bets placed
        """
        pass

    def test_000_check_show_results_display_for__line_1(self):
        """
        DESCRIPTION: Check show results display for  Line 1
        EXPECTED: No show results display if bet has only Line1
        """
        pass

    def test_000_tab_on_settle__tab(self):
        """
        DESCRIPTION: Tab on 'Settle ' tab
        EXPECTED: Check Lotto bets available in settle tab
        """
        pass

    def test_000_check_show_results_display_for__line_1(self):
        """
        DESCRIPTION: Check show results display for  Line 1
        EXPECTED: No show results display if bet has only Line1
        """
        pass
