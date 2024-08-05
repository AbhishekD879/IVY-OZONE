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
class Test_C2988046_Tracking_of_bet_placing_without_odds_boost_in_Betslip(Common):
    """
    TR_ID: C2988046
    NAME: Tracking of bet placing without odds boost in Betslip
    DESCRIPTION: This Test Case verifies tracking of bet placing without odds boost button in Betslip
    PRECONDITIONS: User is logged in and has positive balance
    PRECONDITIONS: Browser console should be opened
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add just created odds boost tokens to USER1
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

    def test_002_do_not_tap_boost_buttontap_place_bet_buttonverify_that_bet_is_placed_without_odds_boost_title(self):
        """
        DESCRIPTION: Do NOT Tap 'BOOST' button
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Verify that bet is placed without odds boost title
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed without odds boost title
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'oddsBoost' : 'no'
        """
        pass

    def test_004_navigate_to_cmsodds_boostdeactivate_odds_boost_feature_toggle(self):
        """
        DESCRIPTION: Navigate to CMS>Odds Boost
        DESCRIPTION: Deactivate "Odds Boost" Feature Toggle
        EXPECTED: 'Odds Boost' is deactivated
        """
        pass

    def test_005_navigate_back_to_applicationadd_selection_to_betslipverify_that_odds_boost_button_is_not_shown(self):
        """
        DESCRIPTION: Navigate back to application
        DESCRIPTION: Add selection to Betslip
        DESCRIPTION: Verify that odds boost button is NOT shown
        EXPECTED: 'BOOST' button is NOT shown
        """
        pass

    def test_006_add_stake_and_tap_place_bet_buttonverify_that_bet_is_placed(self):
        """
        DESCRIPTION: Add Stake and tap 'PLACE BET' button
        DESCRIPTION: Verify that bet is placed
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed
        """
        pass

    def test_007_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'oddsBoost' : 'no'
        """
        pass
