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
class Test_C16689466_Vanilla_Winning_a_Single_Bet(Common):
    """
    TR_ID: C16689466
    NAME: [Vanilla] Winning a Single Bet
    DESCRIPTION: This test case verifies Winning a Bet for single selection
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User should have positive balance (and sufficient funds to place a bet)
    PRECONDITIONS: 3. At least one event is available for placing a bet
    PRECONDITIONS: (Event creation: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Event+creation+path )
    PRECONDITIONS: (Trigger situation when user wins a bet: https://confluence.egalacoral.com/pages/viewpage.action?pageId=96150627 )
    """
    keep_browser_open = True

    def test_001_add_one_selection_to_betslipindexphpattachmentsget34283(self):
        """
        DESCRIPTION: Add one selection to BetSlip
        DESCRIPTION: ![](index.php?/attachments/get/34283)
        EXPECTED: -
        """
        pass

    def test_002_on_mobiletablet_open_betslip(self):
        """
        DESCRIPTION: (on mobile/tablet) Open BetSlip
        EXPECTED: Added selection is displayed
        EXPECTED: ![](index.php?/attachments/get/34284)
        """
        pass

    def test_003_enter_correct_stake_in_stake_field_and_tap_place_betindexphpattachmentsget34285(self):
        """
        DESCRIPTION: Enter correct Stake in 'Stake' field and tap 'Place Bet'
        DESCRIPTION: ![](index.php?/attachments/get/34285)
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_004_trigger_the_situation_when_user_wins_a_betlink_in_preconditions(self):
        """
        DESCRIPTION: Trigger the situation when user wins a bet
        DESCRIPTION: (link in preconditions)
        EXPECTED: User balance is increased on bet win amount
        """
        pass

    def test_005_go_to_my_bets___settled_bets___desktop_my_account___history___bet_history___desktoptabletmobile(self):
        """
        DESCRIPTION: Go to:
        DESCRIPTION: * My Bets -> Settled Bets - desktop
        DESCRIPTION: * My Account -> History -> Bet history - desktop/tablet/mobile
        EXPECTED: * Won' label is present on the Singles header
        EXPECTED: * 'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: * Green tick is shown on the left of the bet
        EXPECTED: ![](index.php?/attachments/get/34286)
        """
        pass
