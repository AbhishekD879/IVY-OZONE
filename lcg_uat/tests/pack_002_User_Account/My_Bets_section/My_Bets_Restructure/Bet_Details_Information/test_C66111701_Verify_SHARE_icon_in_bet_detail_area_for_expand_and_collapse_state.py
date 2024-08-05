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
class Test_C66111701_Verify_SHARE_icon_in_bet_detail_area_for_expand_and_collapse_state(Common):
    """
    TR_ID: C66111701
    NAME: Verify SHARE icon in bet detail area for expand and collapse state
    DESCRIPTION: This test case verify  SHARE icon in bet detail area for expand and collapse state
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

    def test_000_click_on_expand_to_see_share_icon_position_the_bet_details_in_open_tab(self):
        """
        DESCRIPTION: Click on expand to see share icon position the bet details in open tab
        EXPECTED: Share icon position (right justified) in bet details should be as per Figma up on expand
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/5ab154b4-ce5a-49d1-a32b-bc73dc162fae)
        """
        pass

    def test_000_collapse_the_bet_detail_and_check_the_share_icon_position(self):
        """
        DESCRIPTION: Collapse the bet detail and check the share icon position
        EXPECTED: Share icon position (right justified) in bet details should be as per Figma up on  collapse
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/fcc44ca2-70d8-46f3-bb9b-b7e4ac486486)
        """
        pass

    def test_000_repeat_the_above_steps_for_cashout_tab(self):
        """
        DESCRIPTION: Repeat the above steps for cashout tab
        EXPECTED: 
        """
        pass

    def test_000_repeat_the_above_steps_for_settle_tab_by_expanding_the_bet_detail(self):
        """
        DESCRIPTION: Repeat the above steps for settle tab by expanding the bet detail
        EXPECTED: 
        """
        pass
