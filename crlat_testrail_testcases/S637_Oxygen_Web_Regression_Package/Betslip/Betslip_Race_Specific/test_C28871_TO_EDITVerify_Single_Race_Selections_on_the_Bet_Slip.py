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
class Test_C28871_TO_EDITVerify_Single_Race_Selections_on_the_Bet_Slip(Common):
    """
    TR_ID: C28871
    NAME: [TO-EDIT]Verify Single Race Selections on the Bet Slip
    DESCRIPTION: [TO-EDIT]This case should also include check on QB
    DESCRIPTION: This test case verifies how single selections which are added to the Bet Slip are displayed
    DESCRIPTION: AUTOTEST: [C820554]
    DESCRIPTION: Designs for OX99:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5b801d678d472e7c23e481fa/screen/5c73cda946f9a133003808cc
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c01259e7c06af027fe0065a/screen/5c0a99b2bbd4745ef2ec4acf
    PRECONDITIONS: The following events are required:
    PRECONDITIONS: - Race with SP prices
    PRECONDITIONS: - Race with LP prices
    PRECONDITIONS: - Race with Lp and SP prices
    PRECONDITIONS: To retrieve information from Site Server use the following steps:
    PRECONDITIONS: 1) To get Class IDs for <Race> Sport use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Horse Racing Category ID = 21
    PRECONDITIONS: Greyhounds Category ID = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for Class use the folowing link :
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Note,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes :
    PRECONDITIONS: **'name'** to see the event name and local time
    PRECONDITIONS: **'typeName'** to see the league name
    PRECONDITIONS: **'name'** on the market level - to see the market name
    PRECONDITIONS: **'name' **on the outcome level - to see selection name
    PRECONDITIONS: **'livePriceNum'/'livePriceDen'** in the outcome level - to see odds for a selection in a fractional format
    PRECONDITIONS: **'priceDec'** in the outcome level - to see odds for a selection in a decimal format
    """
    keep_browser_open = True

    def test_001_add_single_sp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add single 'SP' selection to the Bet Slip
        EXPECTED: Bet Slip counter is increased by 1
        """
        pass

    def test_002_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_003_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: **Before OX99**
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level) and "+" sign on the left
        EXPECTED: 2.  Market name ( **'name'** attribute on the market level)
        EXPECTED: 3.  Event name (**'name'** attributes on event level), Event date and time are shown after clicking "+"
        EXPECTED: 4.  'Odds' is 'SP'
        EXPECTED: 5.  'Each Way' checkbox and label
        EXPECTED: 6.  'Stake' label and edit box
        EXPECTED: 7.  'Est. Returns' is "N/A"
        EXPECTED: 8.  Bin icon
        EXPECTED: **After OX99**
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level)
        EXPECTED: 2.  Market name ( **'name'** attribute on the market level)
        EXPECTED: 3.  Time and Event name (**'name'** attributes on event level)
        EXPECTED: 4.  'SP' is shown from the side of 'Stake' edit box
        EXPECTED: 5.  'Est. Returns' is "N/A"
        EXPECTED: 6. 'E/W' checkbox and label
        EXPECTED: 7.  'X' button for removing selection
        EXPECTED: ![](index.php?/attachments/get/31311)
        EXPECTED: ![](index.php?/attachments/get/31312)
        """
        pass

    def test_004_add_single_lp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add single 'LP' selection to the Bet Slip
        EXPECTED: Bet Slip counter is increased by 1
        """
        pass

    def test_005_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_006_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: **Before OX99**
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level) and "+" sign on the left
        EXPECTED: 2.  Market name ( **'name'** attribute on the market level)
        EXPECTED: 3.  Event name (**'name'** attributes on event level), Event date and time are shown after clicking "+"
        EXPECTED: 4.  Odds ( **'livePriceNum'/'livePriceDen' **attributes in a fractional format or **'price Dec'** in decimal format)
        EXPECTED: 5.  'Each Way' checkbox and label
        EXPECTED: 6.  'Stake' label and edit box
        EXPECTED: 7. 'Est. Returns' is "0.00" and is re-calculated after entering Stake
        EXPECTED: 8.  Bin icon
        EXPECTED: **After OX99**
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level)
        EXPECTED: 2.  Market name ( **'name'** attribute on the market level)
        EXPECTED: 3.  Time and Event name (**'name'** attributes on event level)
        EXPECTED: 4.  Price ( **'livePriceNum'/'livePriceDen' **attributes in a fractional format or **'price Dec'** in decimal format) is shown from the side of 'Stake' edit box
        EXPECTED: 5.  'Est. Returns' is "0.00" and is re-calculated after entering Stake
        EXPECTED: 6. 'E/W' checkbox and label
        EXPECTED: 7.  'X' button for removing selection
        EXPECTED: ![](index.php?/attachments/get/31313)
        EXPECTED: ![](index.php?/attachments/get/31314)
        """
        pass

    def test_007_add_a_selection_of_the_event_with_attribute_pricetypecodes__lp_sp(self):
        """
        DESCRIPTION: Add a selection of the event with attribute 'priceTypeCodes' = 'LP, SP'
        EXPECTED: Bet Slip counter is increased by 1
        """
        pass

    def test_008_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_009_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: **Before OX99**
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type ( **'name'** attribute on the market level)
        EXPECTED: 3.  Event name ( **'name'** attributes on event level), Event date and time are shown after clicking "+"
        EXPECTED: 4.  'Odds' field is a dropdown which contains LP value and SP. User has a possibility to switch between 'LP' and 'SP' bets
        EXPECTED: 5.  'Each Way' checkbox and label
        EXPECTED: 6.  'Stake' label and edit box
        EXPECTED: 7. 'Est. Returns' are changed according to selected price type
        EXPECTED: 8.  Bin icon
        EXPECTED: **After OX99**
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level)
        EXPECTED: 2.  Market name ( **'name'** attribute on the market level)
        EXPECTED: 3.  Time and Event name (**'name'** attributes on event level)
        EXPECTED: 4.  Price is a dropdown which contains LP value and SP. User has a possibility to switch between 'LP' and 'SP' bets
        EXPECTED: 5. 'Est. Returns' are changed according to selected price type
        EXPECTED: 6. 'E/W' checkbox and label
        EXPECTED: 7.  'X' button for removing selection
        EXPECTED: ![](index.php?/attachments/get/31315)
        EXPECTED: ![](index.php?/attachments/get/31316)
        """
        pass
