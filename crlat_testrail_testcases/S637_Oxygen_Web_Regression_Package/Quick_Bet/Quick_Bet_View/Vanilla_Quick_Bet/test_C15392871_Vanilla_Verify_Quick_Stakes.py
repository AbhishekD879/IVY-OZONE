import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C15392871_Vanilla_Verify_Quick_Stakes(Common):
    """
    TR_ID: C15392871
    NAME: [Vanilla] Verify Quick Stakes
    DESCRIPTION: Update: No 'SEK' currency in vanilla
    DESCRIPTION: This test case verifies Quick Stakes within Quick Bet section
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_one_selection_to_betslipnote_before_adding_there_should_be_(self):
        """
        DESCRIPTION: Add one selection to Betslip
        DESCRIPTION: (Note: before adding there should be )
        EXPECTED: Quick Bet is displayed at the bottom of page
        EXPECTED: ![](index.php?/attachments/get/31326)
        """
        pass

    def test_003_verify_quick_stakes(self):
        """
        DESCRIPTION: Verify Quick Stakes
        EXPECTED: Quick Stakes buttons are displayed with the next values:
        EXPECTED: * +<currency symbol>5
        EXPECTED: * +<currency symbol>10
        EXPECTED: * +<currency symbol>50
        EXPECTED: * +<currency symbol>100
        EXPECTED: where <currency symbol> may be :
        EXPECTED: * 'GBP': symbol = **£**;
        EXPECTED: * 'USD': symbol = **$**;
        EXPECTED: * 'EUR': symbol = **€**;
        EXPECTED: * 'SEK': symbol = **Kr**'
        EXPECTED: **NOTE** that for SEK currency the values of quick stakes are: 50, 100, 500, 1000
        EXPECTED: ![](index.php?/attachments/get/31327)
        """
        pass

    def test_004_tap_pluscurrency_symbol5_button_eg_5(self):
        """
        DESCRIPTION: Tap '+<currency symbol>5' button (e.g. £5)
        EXPECTED: * Value of 5 is added to 'Stake' field
        EXPECTED: * 'Estimated Returns' value is calculated according to added value
        EXPECTED: ![](index.php?/attachments/get/31328)
        """
        pass

    def test_005_tap_pluscurrency_symbol10_button_eg_10(self):
        """
        DESCRIPTION: Tap '+<currency symbol>10' button (e.g. £10)
        EXPECTED: * Value of 10 is added to 'Stake' field
        EXPECTED: * 'Estimated. Returns' value is calculated according to added value
        """
        pass

    def test_006_tap_pluscurrency_symbol50_button_eg_50(self):
        """
        DESCRIPTION: Tap '+<currency symbol>50' button (e.g. £50)
        EXPECTED: * Value of 50 is added to 'Stake' field
        EXPECTED: * 'Estimated Returns' value is calculated according to added value
        """
        pass

    def test_007_tap_pluscurrency_symbol100_button_eg_100(self):
        """
        DESCRIPTION: Tap '+<currency symbol>100' button (e.g. £100)
        EXPECTED: * Value of 100 is added to 'Stake' field
        EXPECTED: * 'Estimated Returns' value is calculated according to added value
        """
        pass

    def test_008_enter_stake_manually_in_stake_field_and_then_tap_one_of_quick_stakes_buttons(self):
        """
        DESCRIPTION: Enter stake manually in 'Stake' field and then tap one of Quick Stakes buttons
        EXPECTED: Value is 'Stake' field is equal to Quick Stakes value + entered manually stake
        """
        pass
