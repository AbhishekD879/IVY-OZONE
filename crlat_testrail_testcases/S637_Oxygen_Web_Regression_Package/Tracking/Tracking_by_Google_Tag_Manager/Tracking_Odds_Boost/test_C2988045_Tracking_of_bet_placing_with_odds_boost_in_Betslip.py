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
class Test_C2988045_Tracking_of_bet_placing_with_odds_boost_in_Betslip(Common):
    """
    TR_ID: C2988045
    NAME: Tracking of bet placing with odds boost in Betslip
    DESCRIPTION: This Test Case verifies tracking of bet placing with odds boost button in Betslip
    PRECONDITIONS: User is logged in and has positive balance
    PRECONDITIONS: Browser console should be opened
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add 2 (two) just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1.
    PRECONDITIONS: To view response open Dev tools -> Network -> WS -> choose the last request
    """
    keep_browser_open = True

    def test_001_add_selection_to_betslipadd_stakeverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Add selection to Betslip
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
        EXPECTED: - Original odds are  shown as crossed out
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
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'oddsBoost' : 'yes'
        """
        pass

    def test_005_tap_reuse_selectionverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Reuse selection'
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_006_add_one_more_selection_to_betslipnavigate_to_betslipverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Add one more selection to Betslip
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_007_add_stake_to_singles_and_multiplestap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Add Stake to SINGLES and MULTIPLES
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds is shown for SINGLES and MULTIPLES
        EXPECTED: - Original odds are shown as crossed out for SINGLES and MULTIPLES
        """
        pass

    def test_008_tap_place_bet_buttonverify_that_bet_is_placed_with_odds_boost_title(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Verify that bet is placed with odds boost title
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed with odds boost title
        """
        pass

    def test_009_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'oddsBoost' : 'yes'
        """
        pass
