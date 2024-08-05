import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.virtual_sports
@vtest
class Test_C869664_Bet_Placement_on_Virtual_Sports(Common):
    """
    TR_ID: C869664
    NAME: Bet Placement on Virtual Sports
    DESCRIPTION: This test case verifies bet placement on  Virtual Football
    DESCRIPTION: AUTOTEST [C9770817]
    PRECONDITIONS: Login with user account that has positive balance
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_virtual_football_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Football' sport page
        EXPECTED: - 'Virtual Football' sport page is opened
        """
        pass

    def test_002_select_two_priceodds_button_for_verified_event(self):
        """
        DESCRIPTION: Select two 'Price/Odds' button for verified event
        EXPECTED: - Selected 'Price/Odds' buttons are highlighted in green
        EXPECTED: - Betslip counter is increased
        """
        pass

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: - Selections with bet details is displayed in the Betlsip
        EXPECTED: - Selections are present in Section 'Singles (2)'
        EXPECTED: - 'Multiples(1)' section contains multiples calculated based on added selections
        """
        pass

    def test_004_set_stake_for_singles2_and_multiples1_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Set 'Stake' for 'Singles(2)' and 'Multiples(1)' and tap 'Bet Now' button
        EXPECTED: - Bet is placed
        EXPECTED: - Bet receipt appears in Betslip
        EXPECTED: - 'Reuse selections' and 'Done' buttons are present in footer
        """
        pass

    def test_005_tap_reuse_selections_button(self):
        """
        DESCRIPTION: Tap 'Reuse selections' button
        EXPECTED: - Betslip contains all the same selections
        """
        pass

    def test_006_repeat_step_6(self):
        """
        DESCRIPTION: Repeat step #6
        EXPECTED: 
        """
        pass

    def test_007_click_done_button(self):
        """
        DESCRIPTION: Click 'Done' button
        EXPECTED: - Betslip is empty with no selections
        """
        pass

    def test_008_repeat_this_test_case_for_the_following_virtual_sports_football_speedway_tennis(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Football,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        EXPECTED: 
        """
        pass
