import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@vtest
class Test_C2490957_Banach_Trigger_Betslip_Quick_Bet(Common):
    """
    TR_ID: C2490957
    NAME: Banach. Trigger Betslip (Quick Bet)
    DESCRIPTION: Test case verifies Betslip (Quick Bet) triggering and info, buttons and Est.Returns calculation
    DESCRIPTION: AUTOTEST [C2593962]
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To retrieve odds value check Network tab: "price" request
    PRECONDITIONS: **Banach selections are added to the dashboard**
    """
    keep_browser_open = True

    def test_001_tap_on_the_place_bet_button_with_odds(self):
        """
        DESCRIPTION: Tap on the Place bet button with odds
        EXPECTED: -  Betslip appears
        """
        pass

    def test_002_verify_betslip_quick_bet_info_and_buttons(self):
        """
        DESCRIPTION: Verify Betslip (Quick Bet) info and buttons
        EXPECTED: - Title Betslip and X button
        EXPECTED: - Selections names are the same as they were on dashboard in the next format: - Selection name Market Name
        EXPECTED: - Odds value
        EXPECTED: - Stake box
        EXPECTED: - "Use Free Bet" link is displayed under selections name (if free bets are available for user)
        EXPECTED: - Quick stakes
        EXPECTED: - 'Total Stake' and 'Estimated Returns' have value 0.00
        EXPECTED: - 'Back' button
        EXPECTED: - Disabled 'Place bet' button
        """
        pass

    def test_003_enter_value_in_a_stake_box(self):
        """
        DESCRIPTION: Enter value in a Stake box
        EXPECTED: - Total Stake and Estimated Returns are populated with the values
        EXPECTED: Total Stake - amount entered by user
        EXPECTED: Estimated Returns - calculated based on Odds value: (odds + 1)*stake
        EXPECTED: - 'PLACE BET' button is enabled
        """
        pass
