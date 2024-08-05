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
class Test_C64663382_Verify_the_Updated_Handicap_value_in_Quickbet_and_Betslip_WW_Market(Common):
    """
    TR_ID: C64663382
    NAME: Verify the Updated Handicap value in Quickbet and Betslip_WW Market
    DESCRIPTION: Verify the Updated Handicap value in Quickbet and Betslip_WW Market
    PRECONDITIONS: Market should have handicap values
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_page_where_handicap_markets_are_applicable(self):
        """
        DESCRIPTION: Navigate to EDP page where Handicap markets are applicable
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_handicap_2_way_market_ww_and_add_one_selection_to_quickbetbetslip(self):
        """
        DESCRIPTION: Expand Handicap 2-Way Market WW and Add one selection to Quickbet/BetSlip
        EXPECTED: Mobile:
        EXPECTED: Market should be expanded and Selection added to QuickBet
        EXPECTED: Desktop:
        EXPECTED: Market should be expanded and Selection added to BetSlip
        """
        pass

    def test_004_open_ti_update_handicap_value_and_validate_changes_in_quickbet_and_betslip(self):
        """
        DESCRIPTION: Open Ti, Update Handicap Value and validate changes in Quickbet and betslip
        EXPECTED: Changes should be reflected in Quickbet and betslip
        """
        pass

    def test_005_place_bet_and_verify_bet_placed_with_updated_handicap_values(self):
        """
        DESCRIPTION: Place bet and verify bet placed with Updated handicap values
        EXPECTED: Bet should be placed with Updated handicap value
        """
        pass
