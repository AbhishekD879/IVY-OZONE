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
class Test_C28875_TO_EDITVerify_Each_Way_option_for_LP_price_on_the_Betslip(Common):
    """
    TR_ID: C28875
    NAME: [TO-EDIT]Verify Each Way option for 'LP' price on the Betslip
    DESCRIPTION: [TO-EDIT]This case should also include check on QB
    DESCRIPTION: This test case verifies how Each Way option influence 'Total Est. Returns' and 'Total Stake' values when 'LP' odd is added to the Bet Slip
    DESCRIPTION: AUTOTEST [C2302700]
    PRECONDITIONS: **There is a race event with market with Each Way available**
    PRECONDITIONS: To retrieve information from the Site Server (TST-2) use the following links:
    PRECONDITIONS: 1) To get class IDs for <Race> Sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Horse Racing Category ID = 21
    PRECONDITIONS: Greyhounds Category ID = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for Class use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes :
    PRECONDITIONS: **'priceTypeCodes'**='LP on a market level
    PRECONDITIONS: **'isEachWayAvailable'** on a market level to see whether Each Way checkbox should be displayed on the Bet Slip
    PRECONDITIONS: **'eachWayFactorNum', 'eachWayFactorDen', 'eachWayPlaces'** on a market level to see market terms attributes
    PRECONDITIONS: **'priceNum', 'priceDen'** in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: **'priceDec'** in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True

    def test_001_add_lp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'LP' selection to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_002_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: 1.  Bet Slip with bet details is opened
        EXPECTED: 2.  Each Way option is displayed under the 'Stake' field
        """
        pass

    def test_003_verify_each_way_checkbox(self):
        """
        DESCRIPTION: Verify Each Way checkbox
        EXPECTED: 1.  Checkbox is not selected by default
        EXPECTED: 2.  Checkbox label is 'Each Way'
        """
        pass

    def test_004_enter_stake_in_a_stake_field(self):
        """
        DESCRIPTION: Enter stake in a stake field
        EXPECTED: 1.  'Stake' field corresponds to the entered stake
        EXPECTED: 2.  'Total Stake' is equal to the enetered stake
        EXPECTED: 3.  'Total Est. Returns' value is shown
        """
        pass

    def test_005_verify_total_est_returns_correctness(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' correctness
        EXPECTED: 'Total Est. Returns' is calculated according to the formula:
        EXPECTED: **(*'Total Est. Returns'* = *'stake' *+ *'profit'*)**
        EXPECTED: where
        EXPECTED: **stake** - is entered value in a stake field
        EXPECTED: **profit** = **(priceNum / priceDen)** * **stake** in case when price/odds are in a fractional format
        """
        pass

    def test_006_on_bet_slip_select_checkbox_each_way(self):
        """
        DESCRIPTION: On Bet Slip select checkbox  'Each Way'
        EXPECTED: Each Way option is enabled
        """
        pass

    def test_007_verify_total_est_returns_correctness(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' correctness
        EXPECTED: 'Total Est. Returns' is calculated according to the formula :
        EXPECTED: **(Total Est. Returns = stake + profit + extra_profit)**
        EXPECTED: where
        EXPECTED: **stake** - is entered value in a stake field
        EXPECTED: **profit** = **(priceNum / priceDen)** * **stake** in case when price/odds are in a fractional format
        EXPECTED: ***'extra_profit'***= ***'stake'*** + ***[*** (**eachWayFactorNum** / **eachWayFactorDen** ) **** (***'priceNum'/'priceDen') **** ***'stake' ]***
        """
        pass
