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
class Test_C2988038_Tracking_of_clicking_on_odds_boost_button_on_Quick_Bet(Common):
    """
    TR_ID: C2988038
    NAME: Tracking of clicking on odds boost button on Quick Bet
    DESCRIPTION: This Test Case verifies tracking of clicking on odds boost button in Quick Bet
    PRECONDITIONS: - User is logged in and has positive balance
    PRECONDITIONS: - Browser console should be opened
    PRECONDITIONS: - Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1.
    PRECONDITIONS: - To view response open Dev tools -> Network -> WS -> choose the last request
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_tap_on_boost_buttonverify_odds_are_boosted(self):
        """
        DESCRIPTION: Tap on 'BOOST' button
        DESCRIPTION: Verify odds are boosted
        EXPECTED: "BOOSTED' button is shown
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'odds boost',
        EXPECTED: 'eventLabel' : 'toggle on',
        """
        pass

    def test_004_tap_on_boosted_button(self):
        """
        DESCRIPTION: Tap on 'BOOSTED' button
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'odds boost',
        EXPECTED: 'eventLabel' : 'toggle off',
        """
        pass
