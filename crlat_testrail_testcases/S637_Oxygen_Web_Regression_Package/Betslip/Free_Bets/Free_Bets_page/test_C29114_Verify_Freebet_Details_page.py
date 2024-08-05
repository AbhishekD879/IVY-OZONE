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
class Test_C29114_Verify_Freebet_Details_page(Common):
    """
    TR_ID: C29114
    NAME: Verify Freebet Details page
    DESCRIPTION: This Test Case verified Freebet Details page.
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User have Free Bets available on his account
    PRECONDITIONS: 3. **accountFreebets?freebetTokenType=SPORT** request is used to get a list of all free bets and called on 'My Balance & Freebets' page ONLY (open dev tools -> Network ->XHR tab)
    PRECONDITIONS: 4. 'My Balance & Freebets' icon is present on the right menu
    """
    keep_browser_open = True

    def test_001_open_right_menu(self):
        """
        DESCRIPTION: Open right menu
        EXPECTED: 'My Balance & Freebets' icon displayed
        """
        pass

    def test_002_tap_onmy_balance__freebets(self):
        """
        DESCRIPTION: Tap on 'My Balance & Freebets'
        EXPECTED: 'My Balance & Freebets' page is opened
        """
        pass

    def test_003_tap_onfreebet_details(self):
        """
        DESCRIPTION: Tap on Freebet details
        EXPECTED: Freebet Details page is opened
        """
        pass

    def test_004_freebet_details_page_contain(self):
        """
        DESCRIPTION: Freebet Details page contain:
        EXPECTED: -Freebet description
        EXPECTED: -Freebet value in pounds (including 2 decimal places)
        EXPECTED: -'Use by' (greater than a week) or 'Expires' (less than a week): date in format of DD/MM/YYYY
        EXPECTED: -Freebet Icon
        EXPECTED: -Back button
        EXPECTED: -'Bet Now' button
        """
        pass

    def test_005_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on Back button
        EXPECTED: User is navigated to homepage
        """
        pass
