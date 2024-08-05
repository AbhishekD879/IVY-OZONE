import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1696891_Verify_live_serve_updates_for_Pre_Play_card(Common):
    """
    TR_ID: C1696891
    NAME: Verify live serve updates for Pre Play card
    DESCRIPTION: This test case verifies live updates (suspension/price change) for Pre Play card on Knockouts tab
    DESCRIPTION: Price
    PRECONDITIONS: - Big Competition > Competition (e.g. World Cup) is configured in CMS
    PRECONDITIONS: - All Knockout Rounds (Round of 16, Quarterfinals, Semifinals, Finals) are correctly configured in CMS. Use test case: https://ladbrokescoral.testrail.com/index.php?/cases/view/1473948
    PRECONDITIONS: - Coral app is opened
    """
    keep_browser_open = True

    def test_001_go_to_world_cup__knockouts_tab(self):
        """
        DESCRIPTION: Go to World Cup > Knockouts tab
        EXPECTED: Knockouts tab is opened
        """
        pass

    def test_002___in_ti_change_price_for_any_knockout_match_event__in_app_verify_odds_buttons_for_a_corresponding_knockout_match_card(self):
        """
        DESCRIPTION: - In TI: Change price for any Knockout match event
        DESCRIPTION: - In app: Verify Odds button(s) for a corresponding Knockout match card
        EXPECTED: - Price update is received in 'push' response (Network > All)
        EXPECTED: - Corresponding 'Price/Odds' button immediately display new price and for a few seconds it changes its color to:
        EXPECTED: *blue color if price has decreased
        EXPECTED: *red color if price has increased
        """
        pass

    def test_003_go_to_settings_and_change_odds_format_to_decimal_and_repeat_step_2(self):
        """
        DESCRIPTION: Go to Settings and change Odds format to Decimal and repeat step 2
        EXPECTED: All prices are displayed in Decimal format
        """
        pass

    def test_004___in_ti_suspend_eventmarketselection_of_any_knockout_match_event__in_app_verify_odds_buttons_for_corresponding_knockout_match_card(self):
        """
        DESCRIPTION: - In TI: Suspend event/market/selection of any Knockout match event
        DESCRIPTION: - In app: Verify Odds button(s) for corresponding Knockout match card
        EXPECTED: - Update for Event/market/selection is received in 'push' response (Network > All)
        EXPECTED: - Odds button(s) become disabled
        """
        pass

    def test_005___in_ti_unsuspend_eventmarketselection_of_any_knockout_match_event__in_app_verify_corresponding_knockout_match_card(self):
        """
        DESCRIPTION: - In TI: Unsuspend event/market/selection of any Knockout match event
        DESCRIPTION: - In app: Verify corresponding Knockout match card
        EXPECTED: - Update for Event/market/selection is received in 'push' response (Network > All)
        EXPECTED: - Odds button(s) become enabled
        """
        pass
