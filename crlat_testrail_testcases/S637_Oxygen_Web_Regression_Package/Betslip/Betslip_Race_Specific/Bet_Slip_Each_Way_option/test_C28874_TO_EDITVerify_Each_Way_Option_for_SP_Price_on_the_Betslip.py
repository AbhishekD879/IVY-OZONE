import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C28874_TO_EDITVerify_Each_Way_Option_for_SP_Price_on_the_Betslip(Common):
    """
    TR_ID: C28874
    NAME: [TO-EDIT]Verify Each Way Option for 'SP' Price on the Betslip
    DESCRIPTION: [TO-EDIT]This case should also include check on QB
    DESCRIPTION: This test case verifies how Each Way option influence 'Total Returns' and 'Total Stakes' values ONLY when 'SP' selection is added to the Bet Slip.
    DESCRIPTION: AUTOTEST [C2302699]
    PRECONDITIONS: **There is a race event with market with Each Way available**
    PRECONDITIONS: To retrieve information from the Site Server (TST-2) use the following links:
    PRECONDITIONS: 1) To get class IDs for <Race> Sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Horse Racing Category ID = 21
    PRECONDITIONS: Greyhounds Ctegory ID = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for Class use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes :
    PRECONDITIONS: **'priceTypeCodes'**='SP' on a market level
    PRECONDITIONS: **'isEachWayAvailable'** on market level to see whether Each Way checkbox should be displayed on the Bet Slip
    """
    keep_browser_open = True

    def test_001_add_sp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'SP' selection to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_002_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: 1.  Bet Slip with bet details is opened
        EXPECTED: 2.  EachWay checkbox is displayed under the Stake field
        """
        pass

    def test_003_verify_each_way_checkbox(self):
        """
        DESCRIPTION: Verify Each Way checkbox
        EXPECTED: 1.  Checkbox is not selected by default
        EXPECTED: 2.  Checkbox label is 'Each Way'
        """
        pass

    def test_004_enter_a_stake_in_a_stake_field(self):
        """
        DESCRIPTION: Enter a stake in a Stake field
        EXPECTED: 1.  'Stake' value corresponds to the entered stake
        EXPECTED: 2.  'Total Stake' is equal to entered stake
        EXPECTED: 3.  'Total Est. Returns' is not calculated for 'SP' odds and displays "N/A"
        """
        pass

    def test_005_on_a_bet_slip_select_checkbox_each_way(self):
        """
        DESCRIPTION: On a Bet Slip select checkbox 'Each Way'
        EXPECTED: 1. EachWay checkbox is selected
        EXPECTED: 2. 'Stake' value corresponds to the entered stake
        EXPECTED: 3. 'Total Stake' value is doubled
        EXPECTED: 4. 'Total Est. Returns is not calculated for 'SP' odds and displays "N/A"
        """
        pass
