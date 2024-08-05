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
class Test_C16761015_Vanilla_Coral_Verify_Freebet_Details_page(Common):
    """
    TR_ID: C16761015
    NAME: [Vanilla Coral]  Verify Freebet Details page
    DESCRIPTION: This Test Case verified Freebet Details page.
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User have Free Bets available on his account
    PRECONDITIONS: 3. **accountFreebets?freebetTokenType=SPORT** request is used to get a list of all free bets and called on 'My Balance & Freebets' page ONLY (open dev tools -> Network ->XHR tab)
    PRECONDITIONS: 4. 'Freebets' icon is present on the 'My Acount' menu ![](index.php?/attachments/get/25310456)
    """
    keep_browser_open = True

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_account_button_on_the_header(self):
        """
        DESCRIPTION: Tap Account button on the header
        EXPECTED: Account Menu is displayed
        """
        pass

    def test_003_tap_offers__free_bets_options_from_the_list(self):
        """
        DESCRIPTION: Tap 'OFFERS & FREE BETS' options from the list
        EXPECTED: 'OFFERS & FREE BETS' menu is open
        """
        pass

    def test_004_tap_sports_free_bets__option(self):
        """
        DESCRIPTION: Tap 'SPORTS FREE BETS ' option
        EXPECTED: 'MY FREEBETS/BONUSES' page is opened that contains list of available free bets with following information:
        EXPECTED: -Freebet name
        EXPECTED: -Freebet value in proper currency (including 2 decimal places)
        EXPECTED: -'Use by' (greater than a week) in date format of DD/MM/YYYY or 'Expires' (less than a week) with number of remaining days
        EXPECTED: -Freebet Icon
        EXPECTED: -Back button
        """
        pass

    def test_005_tap_on_one_of_the_free_bet_from_the_list(self):
        """
        DESCRIPTION: Tap on one of the free bet from the list
        EXPECTED: 'FREEBET INFORMATION' page is opened that contains information about selected free bet:
        EXPECTED: -Freebet name
        EXPECTED: -Freebet value in proper currency (including 2 decimal places)
        EXPECTED: -'Use by' (greater than a week) in date format of DD/MM/YYYY or 'Expires' (less than a week) with number of remaining days
        EXPECTED: -Freeet Icon
        EXPECTED: -Back button
        EXPECTED: -'Bet Now' button
        """
        pass

    def test_006_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on Back button
        EXPECTED: User is navigated to the 'My FREEBETS/BONUSES' page
        """
        pass
