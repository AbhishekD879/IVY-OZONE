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
class Test_C2988040_Tracking_of_clicking_on_odds_boost_button_on_Betslip(Common):
    """
    TR_ID: C2988040
    NAME: Tracking of clicking on odds boost button on Betslip
    DESCRIPTION: This Test Case verifies tracking of clicking on odds boost button in Betslip
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

    def test_001_add_one_selection_to_betslipverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Add one selection to Betslip
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_tap_on_boost_buttonverify_odds_are_boosted(self):
        """
        DESCRIPTION: Tap on 'BOOST' button
        DESCRIPTION: Verify odds are boosted
        EXPECTED: 'BOOSTED' button is shown
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
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
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'odds boost',
        EXPECTED: 'eventLabel' : 'toggle off',
        """
        pass

    def test_006_add_few_more_selection_to_betslipturn_on_and_turn_off_odds_boost_buttonverify_that_tracking_works_the_same_as_for_one_selection(self):
        """
        DESCRIPTION: Add few more selection to Betslip
        DESCRIPTION: Turn on and Turn off odds boost button
        DESCRIPTION: Verify that tracking works the same as for one selection
        EXPECTED: The same pushes are sent to GA
        """
        pass
