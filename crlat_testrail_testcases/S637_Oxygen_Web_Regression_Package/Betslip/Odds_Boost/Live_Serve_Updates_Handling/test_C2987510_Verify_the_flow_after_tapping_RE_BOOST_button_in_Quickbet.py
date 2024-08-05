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
class Test_C2987510_Verify_the_flow_after_tapping_RE_BOOST_button_in_Quickbet(Common):
    """
    TR_ID: C2987510
    NAME: Verify the flow after tapping RE-BOOST button in Quickbet
    DESCRIPTION: This test case verifies the flow after tapping RE-BOOST button in Quickbet
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to the Quickbet
    PRECONDITIONS: Tap 'Boost' button
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
        EXPECTED: The boost button text changes to 'BOOSTED'
        EXPECTED: The boost button remains selected
        """
        pass

    def test_004_verify_that_the_returns_values_are_updated(self):
        """
        DESCRIPTION: Verify that the returns values are updated
        EXPECTED: The returns values are updated
        """
        pass

    def test_005_verify_that_the_header_notification_message_price_changed_from_xx_to_yy_is_removed(self):
        """
        DESCRIPTION: Verify that the header notification message 'Price changed from X/X to Y/Y' is removed
        EXPECTED: The header notification message is removed
        """
        pass
