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
class Test_C1234496_Not_actual_from_OX_99_Free_Bets_dropdown(Common):
    """
    TR_ID: C1234496
    NAME: [Not actual from OX 99] Free Bets dropdown
    DESCRIPTION: This test case verifies Free Bets dropdown
    DESCRIPTION: AUTOTEST [C2779953]
    PRECONDITIONS: * Coral application is loaded
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * User has added selection(s) Betslip (or Quick bet betslip)
    PRECONDITIONS: 4. The user has free bets added to next levels:
    PRECONDITIONS: * all
    PRECONDITIONS: * class
    PRECONDITIONS: * type
    PRECONDITIONS: * event
    PRECONDITIONS: * market
    PRECONDITIONS: * selection
    PRECONDITIONS: 5. [How to add Free bets to user`s account] [1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: 5. Open Dev Tools -> Network -> XHR filter to see response of **user** request
    """
    keep_browser_open = True

    def test_001_verify_free_bets_drop_down(self):
        """
        DESCRIPTION: Verify Free bets drop-down
        EXPECTED: * 'Free Bets Available' text is displayed within drop-down
        """
        pass

    def test_002_tap_free_bets_drop_down(self):
        """
        DESCRIPTION: Tap Free bets drop-down
        EXPECTED: * List of available for particular selection free bets is displayed within drop-down
        EXPECTED: * Each free bet is displayed in next format:
        EXPECTED: <Free bet name> <currency symbol> <free bet value>
        EXPECTED: where <currency symbol>  - currency set during registration
        """
        pass

    def test_003_verify_free_bet_token_name(self):
        """
        DESCRIPTION: Verify Free bet token name
        EXPECTED: Free bet token name corresponds to **freebets.data.[i].freebetOfferName** attribute received in **user** response
        EXPECTED: where i - number of free bets returned in response
        """
        pass

    def test_004_verify_free_bet_token_value(self):
        """
        DESCRIPTION: Verify Free bet token value
        EXPECTED: Free bet token value corresponds to **freebets.data.[i].freebetTokenValue** attribute received in **user** response
        EXPECTED: where i - number of free bets returned in response
        """
        pass

    def test_005_choose_some_free_bet_from_drop_down(self):
        """
        DESCRIPTION: Choose some free bet from drop-down
        EXPECTED: * Free bet is selected
        EXPECTED: * Name of selected free bet is displayed within dropdown
        """
        pass

    def test_006_click_within_dropdown_again(self):
        """
        DESCRIPTION: Click within dropdown again
        EXPECTED: * 'Don't Use Free Bet' text is displayed at the top of drop-down
        EXPECTED: * List of available free bets is displayed within drop-down
        """
        pass

    def test_007_select_dont_use_free_bet_option(self):
        """
        DESCRIPTION: Select 'Don't Use Free Bet' option
        EXPECTED: * The previously selected value is cleared
        EXPECTED: * 'Free Bets Available' message appears instead
        """
        pass
