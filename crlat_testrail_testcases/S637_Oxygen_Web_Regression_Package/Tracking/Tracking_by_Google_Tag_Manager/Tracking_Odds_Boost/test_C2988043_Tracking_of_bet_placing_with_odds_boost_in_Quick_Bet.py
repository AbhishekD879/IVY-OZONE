import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2988043_Tracking_of_bet_placing_with_odds_boost_in_Quick_Bet(Common):
    """
    TR_ID: C2988043
    NAME: Tracking of bet placing with odds boost in Quick Bet
    DESCRIPTION: This Test Case verifies tracking of bet placing with odds boost button in Quick Bet
    PRECONDITIONS: User is logged in and has positive balance
    PRECONDITIONS: Browser console should be opened
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1.
    PRECONDITIONS: To view response open Dev tools -> Network -> WS -> choose the last request
    PRECONDITIONS: Add User1
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betadd_stakeverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        DESCRIPTION: Add Stake
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds shown as crossed out
        """
        pass

    def test_003_tap_place_bet_buttonverify_that_bet_is_placed_with_odds_boost_title(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Verify that bet is placed with odds boost title
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed with odds boost title
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'oddsBoost' : 'yes'
        """
        pass
