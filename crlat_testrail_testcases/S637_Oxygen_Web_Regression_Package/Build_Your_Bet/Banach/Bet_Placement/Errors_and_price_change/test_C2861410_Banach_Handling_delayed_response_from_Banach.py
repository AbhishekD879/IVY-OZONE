import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2861410_Banach_Handling_delayed_response_from_Banach(Common):
    """
    TR_ID: C2861410
    NAME: Banach. Handling delayed response from Banach
    DESCRIPTION: Test case verifies behavior when Banach response is delayed for more than 5 seconds
    DESCRIPTION: Should be tested with mocked data (small remotebetslip timeout value on the environment)
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: **Build Your Bet selections are added to Dashboard**
    """
    keep_browser_open = True

    def test_001_enter_a_stake_and_tap_place_bet_buttonand_there_is_no_response_from_banach_for_5_seconds_by_default(self):
        """
        DESCRIPTION: Enter a stake and tap Place bet button
        DESCRIPTION: (and there is no response from Banach {for 5 seconds by default})
        EXPECTED: UI message above betslip is shown:
        EXPECTED: **We have experienced some difficulties during bet placement, please check your open bets to see if your bet was placed.**
        """
        pass

    def test_002_tap_on_the_open_bets_link_inside_the_message(self):
        """
        DESCRIPTION: Tap on the **open bets** link inside the message
        EXPECTED: User is taken to Open Bets
        """
        pass
