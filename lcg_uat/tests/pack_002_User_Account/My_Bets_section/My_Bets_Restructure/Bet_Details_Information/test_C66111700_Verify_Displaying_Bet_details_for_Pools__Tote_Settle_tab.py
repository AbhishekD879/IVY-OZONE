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
class Test_C66111700_Verify_Displaying_Bet_details_for_Pools__Tote_Settle_tab(Common):
    """
    TR_ID: C66111700
    NAME: Verify Displaying Bet details for Pools / Tote Settle tab
    DESCRIPTION: This test case verify displaying Bet details for Pools // Tote Settle tab
    PRECONDITIONS: Bets should be available in Settle tab
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

    def test_000_navigate_to_horse_racing__page(self):
        """
        DESCRIPTION: Navigate to Horse racing  page
        EXPECTED: Racing page should be opened
        """
        pass

    def test_000_click_on_any_of_the_meeting(self):
        """
        DESCRIPTION: Click on any of the meeting
        EXPECTED: HR EDP page should be opened
        """
        pass

    def test_000_place_totepool_bets(self):
        """
        DESCRIPTION: Place tote/pool bets
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

    def test_000_check_the_bets_placed_for_totepools(self):
        """
        DESCRIPTION: Check the bets placed for tote/pools
        EXPECTED: Bets should be available in open tab
        """
        pass

    def test_000_click_on_settle_tab_after_the_above_totepool__bets_got__settled(self):
        """
        DESCRIPTION: Click on Settle tab after the above tote/pool  bets got  settled
        EXPECTED: Bets should be available in settle tab after settlement
        """
        pass

    def test_000_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        pass

    def test_000_check_the_bet_detail_information_for_totepools_for_settle_bets(self):
        """
        DESCRIPTION: Check the bet detail information for tote/pools for settle bets
        EXPECTED: Bet detail information should be as per Figma in settle tab
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/f40fb1da-b148-4729-b34e-889de60b2b5c)
        EXPECTED: ![](index.php?/attachments/get/c69c4bb2-5dac-4bbb-9b85-02ac2f6f9e71)
        """
        pass
