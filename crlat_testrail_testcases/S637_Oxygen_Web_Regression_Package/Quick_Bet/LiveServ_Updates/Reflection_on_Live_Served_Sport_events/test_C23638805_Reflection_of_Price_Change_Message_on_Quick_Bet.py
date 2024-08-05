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
class Test_C23638805_Reflection_of_Price_Change_Message_on_Quick_Bet(Common):
    """
    TR_ID: C23638805
    NAME: Reflection of Price Change Message on Quick Bet
    DESCRIPTION: This test case verifies the reflection of price change message in case there is a difference/delay between the price of In-Play page and Quick Bet on sports page.
    PRECONDITIONS: -Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: -Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: -Quick Bet is enabled in account settings
    PRECONDITIONS: -The user logged in and the app is open
    PRECONDITIONS: In order to Block push updates: Navigate to EDP of a live event -> Open Network on Devtools -> find the recent push -> right click -> Select "Block request domain"
    PRECONDITIONS: Credentials to TI https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_navigate_to_an_edp_of_a_live_event(self):
        """
        DESCRIPTION: Navigate to an EDP of a live event
        EXPECTED: EDP page with live event is open
        """
        pass

    def test_002_block_push_updates_block_request_domain(self):
        """
        DESCRIPTION: Block push updates (Block request domain)
        EXPECTED: The push updates are blocked on EDP
        """
        pass

    def test_003_trigger_price_change_in_ti(self):
        """
        DESCRIPTION: Trigger price change in TI
        EXPECTED: On EDP the price update is not received and not reflected
        """
        pass

    def test_004_add_a_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add a selection to Quick Bet
        EXPECTED: *The selection is added to Quick Bet
        EXPECTED: *The price update is received via Request URL: wss://remotebetslip-dev0.coralsports.dev.cloud.ladbrokescoral.com/quickbet/?EIO=3&transport=websocket
        """
        pass

    def test_005_pay_attention_to_quick_bet(self):
        """
        DESCRIPTION: Pay attention to Quick Bet
        EXPECTED: Before OX 100
        EXPECTED: -The message 'Please be aware that your selection had a price change'is displayed
        EXPECTED: -The button is changed to "Accept & Place Bet"
        """
        pass
