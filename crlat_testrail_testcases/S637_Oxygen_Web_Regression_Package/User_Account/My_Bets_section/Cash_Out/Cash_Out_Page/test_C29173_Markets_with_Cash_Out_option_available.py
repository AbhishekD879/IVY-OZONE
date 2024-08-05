import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C29173_Markets_with_Cash_Out_option_available(Common):
    """
    TR_ID: C29173
    NAME: Markets with Cash Out option available
    DESCRIPTION: This test case verifies Markets with Cash Out option available on Event Details Pages.
    DESCRIPTION: **Jira tickets**:
    DESCRIPTION: * BMA-2942, BMA-3925
    PRECONDITIONS: In order to check event/market data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: *   XXX - Event ID
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapsporticon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details page
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_verify_cash_out_icon_for_market_withcashoutavaily_attribute_on_market_level(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="Y"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is displayed from the right side on corresponding market accordion
        """
        pass

    def test_005_verify_cash_out_icon_for_market_withcashoutavailn_attribute_on_market_level(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="N"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is NOT displayed from the right side on corresponding market accordion
        """
        pass

    def test_006_verify_cash_out_icon_for_combined_marketsfootball_scorecastpopular_goalscorer_markets_etc(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for **combined** markets
        DESCRIPTION: (<Football>: Scorecast/Popular Goalscorer Markets etc.)
        EXPECTED: If one of combined markets has **cashoutAvail="Y"** then 'Cash out' icon should be displayed from the right side on corresponding market accordion
        """
        pass

    def test_007_tapraceicon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> Landing Page is opened
        """
        pass

    def test_008_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details page
        EXPECTED: <Race> Event Details page is opened
        """
        pass

    def test_009_verify_cash_out_icon_for_market_withcashoutavaily_attribute_on_market_levelnote_for_now_cash_out_is_available_for__horse_racing__win_or_each_way_market_lp_and_sp_prices__grey_hounds_win_or_each_way_market_only_lp(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="Y"** attribute on Market level
        DESCRIPTION: **Note:** For now cash out is available for:
        DESCRIPTION: *  Horse Racing:  **Win or Each Way** market (LP and SP prices)
        DESCRIPTION: *  Grey Hounds: **Win or Each Way** market (only LP)
        EXPECTED: 'CASH OUT' icon is displayed in the same line as the Each-way terms below <Race> Event markets tabs
        """
        pass

    def test_010_verify_cash_out_icon_for_market_withcashoutavailn_attribute_on_market_level(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="N"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is NOT displayed in the same line as the Each-way terms below <Race> Event markets tabs
        """
        pass
