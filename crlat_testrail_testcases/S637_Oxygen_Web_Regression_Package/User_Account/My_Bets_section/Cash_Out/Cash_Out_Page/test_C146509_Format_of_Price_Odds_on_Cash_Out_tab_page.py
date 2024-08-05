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
class Test_C146509_Format_of_Price_Odds_on_Cash_Out_tab_page(Common):
    """
    TR_ID: C146509
    NAME: Format of Price/Odds on 'Cash Out' tab/page
    DESCRIPTION: This test case verifies Price/Odds in decimal and fractional format.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-3180 Show bets on "Cash Out" tab in decimal format
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles and Multiple bets on events where Cash Out offer is available
    PRECONDITIONS: * Go to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
    PRECONDITIONS: * Open DevTools and check the next request to SS to get Price Odds data
    PRECONDITIONS: https://{domain}/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForOutcome/{outcomeIDs}?simpleFilter=event.suspendAtTime:greaterThan:2020-01-13T12:44:00.000Z&racingForm=outcome&includeUndisplayed=true&translationLang=en&includeRestricted=true&prune=event&prune=market
    PRECONDITIONS: where,
    PRECONDITIONS: *   outcomeIDs - valid ID(s) of outcome that bet was placed on
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   domain - resource domain
    PRECONDITIONS: e.g. ss-aka-ori.coral.co.uk - Prod
    PRECONDITIONS: ![](index.php?/attachments/get/52704924)
    """
    keep_browser_open = True

    def test_001_verify_priceodds_in_fractional_format_ofsingle_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in fractional format of Single selection
        EXPECTED: In fractional format Price/Odds corresponds to: *'priceNum'/'priceDen'* attributes from SS response (i.e.9/1)
        EXPECTED: ![](index.php?/attachments/get/52704923)
        """
        pass

    def test_002_verify_priceodds_in_fractional_format_of_multiples_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in fractional format of Multiples selection
        EXPECTED: The result is the same as in step #1
        """
        pass

    def test_003_go_to_settings_switch_odds_format_to_decimal_and_go_back_to_cashout_page(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format to Decimal and go back to Cashout page
        EXPECTED: Odds are shown in Decimal format
        """
        pass

    def test_004_verify_priceodds_in_decimal_format_of_single_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in decimal format of Single selection
        EXPECTED: In decimal format Price/Odds corresponds to: *'priceDec'* attribute from SS response(i.e.10)
        EXPECTED: ![](index.php?/attachments/get/52668624)
        """
        pass

    def test_005_verify_priceodds_in_decimal_format_of_multiples_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in decimal format of Multiples selection
        EXPECTED: The result is the same as in step #4
        """
        pass

    def test_006_verify_sp_price_displaying_forsingle_racing_selections(self):
        """
        DESCRIPTION: Verify SP price displaying for Single Racing selections
        EXPECTED: **SP** is shown next to 'Odds:' label
        """
        pass

    def test_007_verify_sp_price_displaying_for_racing_selections_in_multiple_bet(self):
        """
        DESCRIPTION: Verify SP price displaying for Racing selections in Multiple bet
        EXPECTED: The result is the same as in step #6
        """
        pass
