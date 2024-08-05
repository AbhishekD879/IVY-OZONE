import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C15392971_CMS_configurable_message_for_OverAsk_Trader_offer_message(Common):
    """
    TR_ID: C15392971
    NAME: CMS configurable message for OverAsk Trader offer message
    DESCRIPTION: This test case verifies CMS configurable message for OverAsk Trader offer message
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User's balance is more that allowed Max stake value
    PRECONDITIONS: CMS: System Configuration-> Structure-> Overask-> text in **traderOfferNotificationMessage** is entered
    PRECONDITIONS: ![](index.php?/attachments/get/31338)
    PRECONDITIONS: ![](index.php?/attachments/get/31339)
    """
    keep_browser_open = True

    def test_001_add_selection_and_go_betslip(self):
        """
        DESCRIPTION: Add selection and go Betslip
        EXPECTED: 
        """
        pass

    def test_002_enter_value_in_stake_field_that_exceeds_max_allowed_bet_limit_for_particular_selection_and_click__tap_place_bet_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Place bet' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_003_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * CMS configurable **traderOfferNotificationMessage** for OverAsk Trader offer is displayed.
        EXPECTED: * Expires offer counter is displayed
        """
        pass

    def test_005_change_traderoffernotificationmessage_in_cmsrepeat_step_2_3(self):
        """
        DESCRIPTION: Change **traderOfferNotificationMessage** in CMS
        DESCRIPTION: Repeat step 2-3
        EXPECTED: Text is changed according to CMS
        EXPECTED: ![](index.php?/attachments/get/31340)
        """
        pass
