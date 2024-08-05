import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732011_Verify_Odds_calculations(Common):
    """
    TR_ID: C57732011
    NAME: Verify Odds calculations
    DESCRIPTION: This test case verifies Odds calculations
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. User on 'Current Tab'
    """
    keep_browser_open = True

    def test_001_set_scores_and_tap_on_submit_button_on_current_tab(self):
        """
        DESCRIPTION: Set scores and Tap on 'Submit' button on 'Current Tab'
        EXPECTED: - 'You are in' page opened successfully
        EXPECTED: - Carousel with markets successfully displayed
        EXPECTED: - Odds displayed eg. '£10 pays £130 (odds 12/1)'
        """
        pass

    def test_002_verifies_odds_calculationopen_prediction_response_and_check_multipleprice_value(self):
        """
        DESCRIPTION: Verifies odds calculation
        DESCRIPTION: (Open prediction response, and check 'multiplePrice' value)
        EXPECTED: odds = 'multiplePrice-1'/1
        """
        pass

    def test_003_verifies_pays_calculationopen_prediction_response_and_check_multipleprice_value(self):
        """
        DESCRIPTION: Verifies pays calculation
        DESCRIPTION: (Open prediction response, and check 'multiplePrice' value)
        EXPECTED: pays = multiplePrice*M (M = £10, hardcoded for now)
        """
        pass
