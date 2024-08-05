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
class Test_C58420433_Verify_calculation_of_the_potential_returns_for_boosted_multiple_bet(Common):
    """
    TR_ID: C58420433
    NAME: Verify calculation of the potential returns for boosted multiple bet.
    DESCRIPTION: This test case verifies calculation of the potential returns for boosted multiple bet.
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS.
    PRECONDITIONS: Load application and login with User with odds boost token ANY available
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: OpenBet Systems: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_log_in_into_the_app_and_open_settings_betting_settingschange_price_to_decimal(self):
        """
        DESCRIPTION: Log in into the app and open Settings->betting settings.
        DESCRIPTION: Change price to 'Decimal'
        EXPECTED: Price changed.
        """
        pass

    def test_002_add_selections_to_betslip__selection_1_selection_2_with_available_odds_boost(self):
        """
        DESCRIPTION: Add selections to Betslip:
        DESCRIPTION: - Selection_1, Selection_2 with available odds boost.
        EXPECTED: Selections are added. 'BOOST' button is available.
        """
        pass

    def test_003___input_1__into_the_stake_field__tap_boost_button(self):
        """
        DESCRIPTION: - Input '1'  into the stake field.
        DESCRIPTION: - Tap 'BOOST' button
        EXPECTED: - ''BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Odds are boosted
        EXPECTED: - Original odds are displayed as crossed out for Selection_1 and Selection_2
        EXPECTED: - Updated  'potential returns'/'Est. Returns' are shown for singles and for multiples section.
        EXPECTED: Potential returns should be the same as the boosted price.
        EXPECTED: There could be small difference between price and potential payout with stake = 1 for example, because of roundation logic for potential payouts(we round down them). Example price is 11.6/1 and  potential payout is 11.5
        EXPECTED: ![](index.php?/attachments/get/101693959)
        """
        pass

    def test_004_open_settings_betting_settingschange_price_to_fractional(self):
        """
        DESCRIPTION: Open Settings->betting settings.
        DESCRIPTION: Change price to 'Fractional'
        EXPECTED: Price changed.
        """
        pass

    def test_005_open_betslip_and_verify_potential_returnsest_returns_for_boosted_multiple(self):
        """
        DESCRIPTION: Open Betslip and verify 'potential returns'/'Est. Returns' for boosted multiple.
        EXPECTED: - Updated  'potential returns'/'Est. Returns' are shown for singles and for multiples section.
        EXPECTED: Potential returns should be the same as the 'boosted price+1'.
        EXPECTED: There could be small difference between price and potential payout with stake = 1 for example, because of roundation logic for potential payouts(we round down them). Example price is 11.6/1 and potential payout is 11.5
        EXPECTED: ![](index.php?/attachments/get/101693964)
        """
        pass

    def test_006_tap_place_bet_buttonverify_that_bet_receipts_for_multiples_bet_is_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet receipts for multiples bet is shown
        EXPECTED: Receipts for multiple bet is shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boost odds taken by the user are shown
        EXPECTED: - 'potential returns'/'Est. Returns' are shown correspondingly to boosted odds.
        """
        pass
