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
class Test_C2988033_Verify_the_flow_after_tapping_RE_BOOST_button_in_Betslip(Common):
    """
    TR_ID: C2988033
    NAME: Verify the flow after tapping RE-BOOST button in Betslip
    DESCRIPTION: This test case verifies the flow after tapping RE-BOOST button in Betslip
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to the Betslip
    PRECONDITIONS: Add Stake and tap 'Boost' button
    PRECONDITIONS: Change price for this bet in https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Tap 'Re-boost' button
    """
    keep_browser_open = True

    def test_001_verify_that_non_boosted_prices_are_updated(self):
        """
        DESCRIPTION: Verify that non-boosted prices are updated
        EXPECTED: Non-boosted prices are updated
        """
        pass

    def test_002_verify_that_the_boosted_prices_are_updated(self):
        """
        DESCRIPTION: Verify that the boosted prices are updated
        EXPECTED: The boosted prices are updated
        """
        pass

    def test_003_verify_the_boost_button(self):
        """
        DESCRIPTION: Verify the 'Boost' button
        EXPECTED: - The boost button text changes to 'BOOSTED'
        EXPECTED: - The boost button remains selected
        """
        pass

    def test_004_verify_that_the_returns_values_are_updated(self):
        """
        DESCRIPTION: Verify that the returns values are updated
        EXPECTED: The returns values are updated
        """
        pass

    def test_005_verify_that_the_header_notification_message_the_price_has_changed_and_new_boosted_odds_will_be_applied_to_your_bet_hit_re_boost_to_see_your_new_boosted_price_is_removed(self):
        """
        DESCRIPTION: Verify that the header notification message 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted price' is removed
        EXPECTED: The header notification message is removed
        """
        pass

    def test_006_check_accept__place_bet_button(self):
        """
        DESCRIPTION: Check 'ACCEPT & PLACE BET' button
        EXPECTED: The 'ACCEPT & PLACE BET' button returns to 'PLACE BET'
        """
        pass
