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
class Test_C66111692_Verify_Displaying_Bet_details_in_Pre_play_for_Races_in_open_tab(Common):
    """
    TR_ID: C66111692
    NAME: Verify Displaying Bet details in Pre-play for Races in open tab
    DESCRIPTION: This test case verify Displaying Bet details in Pre-play for Races in open tab
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

    def test_000_navigate_any_racing_page(self):
        """
        DESCRIPTION: Navigate any racing page
        EXPECTED: Racing page should be opened
        """
        pass

    def test_000_place_singlemutiple_bets__from_races__for_pre_play_events(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from races  for pre-play events
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
        EXPECTED: Placed bet is displayed
        """
        pass

    def test_000_check_new_setion_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new setion with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        pass

    def test_000_check_the_bet_detail_information_for_sports_singlesmultiples_for__bets_placed_for_pre_play_events(self):
        """
        DESCRIPTION: Check the bet detail information for sports singles/multiples for  bets placed for pre play events
        EXPECTED: Bet detail information should be as per Figma for pre play events
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/b0942b78-bf65-4269-9216-02fc01b37a97)
        """
        pass

    def test_000_repeat_the_above_steps_for_cashout_tab(self):
        """
        DESCRIPTION: Repeat the above steps for cashout tab
        EXPECTED: 
        """
        pass
