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
class Test_C66111684_Verify_collapsing_the_bet_detail_area_and_check_the_data(Common):
    """
    TR_ID: C66111684
    NAME: Verify collapsing the bet detail area and check the data
    DESCRIPTION: This test case verify collapsing the bet detail area and check the data
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
        EXPECTED: Placed bet is displayed
        """
        pass

    def test_000_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        pass

    def test_000_click_on_expand_to_to_see_the_bet_details_in_open_tab(self):
        """
        DESCRIPTION: Click on expand to to see the bet details in open tab
        EXPECTED: Bet details should be displayed up on expand
        """
        pass

    def test_000_collapse_the_bet_detail_in_open_tab(self):
        """
        DESCRIPTION: Collapse the bet detail in open tab
        EXPECTED: Bet detail should be collapsed and only stake and potential return/Est.Resturns are shown
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/061b7134-58bf-4dcc-8b3b-f29248cb80ca)
        """
        pass

    def test_000_repeat_the_above_steps_for_cashout_tab(self):
        """
        DESCRIPTION: Repeat the above steps for cashout tab
        EXPECTED: 
        """
        pass
