import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C28870_Verify_Adding_Several_Race_Selection_with_Different_Price_Types(Common):
    """
    TR_ID: C28870
    NAME: Verify Adding Several Race Selection with Different Price Types
    DESCRIPTION: This test case verifies how different types of prices will be displayed on the Bet Slip
    DESCRIPTION: AUTOTEST [C820554]
    PRECONDITIONS: Make sure that events with the following attributes are available on the Site Server:
    PRECONDITIONS: **'priceTypeCodes'**='LP'
    PRECONDITIONS: **'priceTypeCodes'**='LP, SP'
    PRECONDITIONS: **'priceTypeCodes'**='SP'
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> Event landing page is opened
        """
        pass

    def test_003_add_sp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'SP' selection to the Bet Slip
        EXPECTED: Bet Slip counter is increased by 1
        """
        pass

    def test_004_add_lp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'LP' selection to the Bet Slip
        EXPECTED: Bet Slip counter is increased by 1
        """
        pass

    def test_005_add_a_selection_to_the_bet_slip_from_the_event_with_the_attribute_pricetypecodeslpsp_in_ss(self):
        """
        DESCRIPTION: Add a selection to the Bet Slip from the event with the attribute 'priceTypeCodes'='LP,SP' in SS
        EXPECTED: Bet Slip counter is increased by 1
        """
        pass

    def test_006_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Bet Slip with bets details is opened
        """
        pass

    def test_007_enter_stake_value_only_for_the_lp_selection(self):
        """
        DESCRIPTION: Enter stake value only for the 'LP' selection
        EXPECTED: 1.  Calculated **'Est. Returns'** is shown
        EXPECTED: 2.  Calculated **'Total Est. Returns'** is shown
        EXPECTED: 3.  **'Total Stake'** corresponds to the entered stake value
        """
        pass

    def test_008_enter_stake_value_only_for_the_sp_selection(self):
        """
        DESCRIPTION: Enter stake value only for the 'SP' selection
        EXPECTED: 1.  **'Est. Returns'** is equal to the 'N/A' value
        EXPECTED: 2.  **'Total Est. Returns'** is equal to the 'N/A' value
        EXPECTED: 3.  **'Total Stake'** corresponds to the entered stake value
        """
        pass

    def test_009_enter_stake_value_only_for_the_lpsp_selection(self):
        """
        DESCRIPTION: Enter stake value only for the 'LP'/'SP' selection
        EXPECTED: If 'SP' value is selected from dropdown list :
        EXPECTED: *   **Est. Returns'** is equal to 'N/A' value
        EXPECTED: *   **'Total Est. Returns'** is equal to the 'N/A' value
        EXPECTED: *   **'Total Stake'** is equal to the sum of stake values from both fields
        EXPECTED: If 'LP' value is selected from dropdown list :
        EXPECTED: *   Calculated **'Est. Returns'** is shown
        EXPECTED: *   Calculated **'Total Est. Returns'** is shown
        EXPECTED: *   **'Total Stake' **corresponds to the entered stake value
        """
        pass
