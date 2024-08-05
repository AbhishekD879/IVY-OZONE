import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732012_Verify_button_Add_to_Bet_Slip(Common):
    """
    TR_ID: C57732012
    NAME: Verify button 'Add to Bet Slip'
    DESCRIPTION: This test case verifies 'Add to Slip' button
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. User on 'Current Tab'
    PRECONDITIONS: 2. Events with 3 markets configured
    """
    keep_browser_open = True

    def test_001_set_scores_and_tap_on_submit_button_on_current_tab(self):
        """
        DESCRIPTION: Set scores and Tap on 'Submit' button on 'Current Tab'
        EXPECTED: - 'You are in' page opened successfully
        EXPECTED: - Upsell Market options displayed
        """
        pass

    def test_002_tap_on_add_to_slip_button_for_any_of_the_available_upsell_markets(self):
        """
        DESCRIPTION: Tap on 'Add to Slip' button for any of the available UpSell markets
        EXPECTED: - "One-Two-Free" widget is closed
        EXPECTED: - Betslip opened in the same window
        EXPECTED: (eg. https://m.ladbrokes.com/en-gb/?externalSelectionId=670266374,670338200,670266442#!slip)
        EXPECTED: - User see Bets in Betslip according to selected market (check market and selections in the POST predictions response)
        """
        pass
