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
class Test_C2490628_Banach_The_price_for_this_bet_is_not_available_error__Third_parties_assistance(Common):
    """
    TR_ID: C2490628
    NAME: Banach. The price for this bet is not available error - Third parties assistance
    DESCRIPTION: Test case verifies error when price for selections is not delivered from the provider
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: For Odds calculation check Dev tools > Network: price request
    PRECONDITIONS: Requires assistance from Banach provider
    PRECONDITIONS: To trigger this type of error, BYB of this event should be suspended on Banach side or request should be faked with duplicated selections using web debugging proxy tool
    """
    keep_browser_open = True

    def test_001_add_selections_from_markets_provided_by_banach_for_error_testing(self):
        """
        DESCRIPTION: Add selections from markets provided by Banach for error testing
        EXPECTED: - Error message text appears above Dashboard:
        EXPECTED: **"The price for this bet is not available, please try another combination"**
        EXPECTED: - Place bet button with price is hidden from Dashboard
        """
        pass

    def test_002_check_price_request(self):
        """
        DESCRIPTION: Check **price** request
        EXPECTED: - responseCode: 3
        EXPECTED: responseMessage: null
        EXPECTED: (The 'null' value triggers the generic front-end message: "The price for this bet is not available, please try another combination")
        """
        pass

    def test_003_verify_info_message_after_editingadding_selection_for_valid_combination(self):
        """
        DESCRIPTION: Verify info message after editing/adding selection for valid combination
        EXPECTED: * Info message disappears
        EXPECTED: * Odds area is shown with a price
        """
        pass
