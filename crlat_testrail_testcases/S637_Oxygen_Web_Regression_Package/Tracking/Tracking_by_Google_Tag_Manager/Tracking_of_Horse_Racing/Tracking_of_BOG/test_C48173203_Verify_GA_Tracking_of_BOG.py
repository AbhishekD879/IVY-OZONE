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
class Test_C48173203_Verify_GA_Tracking_of_BOG(Common):
    """
    TR_ID: C48173203
    NAME: Verify GA Tracking of BOG
    DESCRIPTION: This test case verifies tracking in Google Analytic's data Layer of BOG
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-49331]
    PRECONDITIONS: 1. Open Ladbrokes/Coral
    PRECONDITIONS: 2. Events with BOG configured are available
    PRECONDITIONS: 3. BOG has been enabled in CMS
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_rlp_and_click_on_bog_icon_shown_in_the_race_type(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' RLP and Click on 'BOG' icon shown in the race type
        EXPECTED: - BOG Pop-up window is shown
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser Console:
        DESCRIPTION: >> "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push ({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "promotions"
        EXPECTED: eventMarket: "MKTFLAG_BOG"
        EXPECTED: eventAction: "Best Odds Guaranteed"
        EXPECTED: eventLabel: "ok"
        EXPECTED: gtm.uniqueEventId: #
        EXPECTED: });
        """
        pass

    def test_003_click_on_ok_buttons_in_the_bog_pop_up(self):
        """
        DESCRIPTION: Click on "OK" buttons in the 'BOG' Pop-up
        EXPECTED: - Pop-up is closed. User remains on the same page.
        """
        pass

    def test_004_navigate_to_horse_racing_edp_and_repeat_steps_2_and_3(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' EDP and repeat steps **2** and **3**
        EXPECTED: Expected results should match those from steps **2** and **3**
        """
        pass

    def test_005_place_a_bet_on_the_selection_from_the_market_with_bog_rules(self):
        """
        DESCRIPTION: Place a bet on the selection from the market with BOG rules
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_my_bets_tab_and_click_on_bog_icon_in_the_bet_from_step_5(self):
        """
        DESCRIPTION: Navigate to 'My Bets' tab and click on 'BOG' icon in the bet from step **5**
        EXPECTED: - BOG Pop-up window is NOT shown
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser Console:
        DESCRIPTION: >> "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is **NOT** present in data layer
        """
        pass
