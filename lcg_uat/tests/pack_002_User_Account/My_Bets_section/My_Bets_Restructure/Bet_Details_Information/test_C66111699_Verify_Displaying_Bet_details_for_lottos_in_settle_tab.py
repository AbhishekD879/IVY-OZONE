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
class Test_C66111699_Verify_Displaying_Bet_details_for_lottos_in_settle_tab(Common):
    """
    TR_ID: C66111699
    NAME: Verify Displaying Bet details for lotto's in settle tab
    DESCRIPTION: This test case verify displaying Bet details for lotto's  in settle tab
    PRECONDITIONS: Bets should be available in Settle bets
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

    def test_000_navigate_to_lottos_page(self):
        """
        DESCRIPTION: Navigate to Lottos page
        EXPECTED: Racing page should be opened
        """
        pass

    def test_000_place_lotto_bets(self):
        """
        DESCRIPTION: Place lotto bets
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

    def test_000_check_the_bets_placed_for_lotto(self):
        """
        DESCRIPTION: Check the bets placed for Lotto
        EXPECTED: Bets should be available in open tab
        """
        pass

    def test_000_click_on_settle_tab_after_the_above_lotto__bets_got__settled(self):
        """
        DESCRIPTION: Click on Settle tab after the above lotto  bets got  settled
        EXPECTED: Bets should be available in settle tab after settlement
        """
        pass

    def test_000_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        pass

    def test_000_check_the_bet_detail_information_for_lotto_bets_settle_tab(self):
        """
        DESCRIPTION: Check the bet detail information for Lotto bets settle tab
        EXPECTED: Bet detail information should be as per Figma
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/cbc70040-0564-462c-8f11-053c57cb47ac)
        EXPECTED: ![](index.php?/attachments/get/bc1328ad-e67f-45f9-b55f-17628eafe07b)
        """
        pass
