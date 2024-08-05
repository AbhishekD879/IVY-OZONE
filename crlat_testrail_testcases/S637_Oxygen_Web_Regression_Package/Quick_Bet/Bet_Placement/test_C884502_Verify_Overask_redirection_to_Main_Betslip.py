import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C884502_Verify_Overask_redirection_to_Main_Betslip(Common):
    """
    TR_ID: C884502
    NAME: Verify Overask redirection to Main Betslip
    DESCRIPTION: This test case verifies Overask handling within Quick Bet
    DESCRIPTION: AUTOTEST: [C1296553]
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Login under user with positive balance and Overask enabled
    PRECONDITIONS: 3. To enable/disable Overask for the Customer/Event type please follow this path:
    PRECONDITIONS: Backoffice Tool -> Trader Interface -> Customer -> (Search by Username) -> Click on the Account name -> Account Rules -> Select No Intercept value in the Control column  -> click Update
    PRECONDITIONS: User is logged in
    PRECONDITIONS: ======
    PRECONDITIONS: [How to accept/decline/make an Offer with Overask functionality](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955)
    PRECONDITIONS: [How to disable/enable Overask functionality for User or Event Type](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    """
    keep_browser_open = True

    def test_001_select_sportrace_selection(self):
        """
        DESCRIPTION: Select <Sport>/<Race> selection
        EXPECTED: Quick Bet is opened with selection added
        """
        pass

    def test_002_enter_higher_than_max_allowed_stake_value_and_tap_on_place_bet(self):
        """
        DESCRIPTION: Enter higher than max allowed stake value and tap on 'PLACE BET'
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Betslip is opened with selection added
        EXPECTED: * Overask overlay appears
        EXPECTED: ![](index.php?/attachments/get/31295)
        EXPECTED: ![](index.php?/attachments/get/31296)
        """
        pass

    def test_003_verify_that_overask_is_triggered_by_default(self):
        """
        DESCRIPTION: Verify that Overask is triggered by default
        EXPECTED: * Stake field and 'Delete' button are disabled
        EXPECTED: * Spinning icon is displayed instead of 'Bet Now' on green button
        EXPECTED: * Warning message is shown to user on yellow background
        """
        pass

    def test_004_reload_the_page_or_app_and_try_to_add_one_more_selection(self):
        """
        DESCRIPTION: Reload the page or app and try to add one more selection
        EXPECTED: * Selection can not be added during Overask process
        EXPECTED: * After trying to add selection user is navigated to Betslip with bet in review automatically
        """
        pass

    def test_005_open_betslip_and_proceed_with_overask_in_backoffice_acceptdeclinemake_an_offersplit_offer(self):
        """
        DESCRIPTION: Open Betslip and proceed with Overask in Backoffice:
        DESCRIPTION: * accept/decline/make an offer/split offer
        EXPECTED: Main Betslip reflects to Trader action in Backoffice
        """
        pass

    def test_006_in_the_betslip_chose_cancel_button(self):
        """
        DESCRIPTION: In the betslip chose "Cancel" button
        EXPECTED: Selection with the offer was removed
        """
        pass

    def test_007_log_out_and_log_in_under_user_with_positive_balance_and_disabled_overask(self):
        """
        DESCRIPTION: Log out and log in under user with positive balance and disabled Overask
        EXPECTED: 
        """
        pass

    def test_008_repeat_step__1_2(self):
        """
        DESCRIPTION: Repeat step # 1-2
        EXPECTED: * Bet is not places and Overask is not triggered
        EXPECTED: * 'The stake specified in the bet is too high.' error message is shown
        EXPECTED: * Bet remains in Quick Bet
        """
        pass
