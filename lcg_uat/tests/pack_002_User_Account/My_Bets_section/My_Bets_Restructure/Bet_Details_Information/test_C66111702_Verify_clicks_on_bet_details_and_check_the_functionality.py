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
class Test_C66111702_Verify_clicks_on_bet_details_and_check_the_functionality(Common):
    """
    TR_ID: C66111702
    NAME: Verify clicks on bet details and check the  functionality
    DESCRIPTION: This test case Verify Bet Details area to contain Collapsible / Expandable Bet Details section
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

    def test_000_click_on_expand_for_bet_details_and_check_the_size(self):
        """
        DESCRIPTION: Click on Expand for bet details and check the size
        EXPECTED: Bet details should be expanded and area size should be as per Figma
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/49e10bdb-b78d-4b89-842d-1facd57ac880)
        """
        pass

    def test_000_repeat__the_above_steps_for_cashout_tab_for_bet_details(self):
        """
        DESCRIPTION: Repeat  the above steps for cashout tab for bet details
        EXPECTED: 
        """
        pass

    def test_000_repeat_the_above_steps_for_settle_tab_for_bet_details(self):
        """
        DESCRIPTION: Repeat the above steps for settle tab for bet details
        EXPECTED: 
        """
        pass
