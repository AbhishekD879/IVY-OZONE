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
class Test_C29010_Making_Sport_Single_Selection(Common):
    """
    TR_ID: C29010
    NAME: Making <Sport> Single Selection
    DESCRIPTION: This test case verifies Making Single Selections on the <Sport> pages.
    DESCRIPTION: AUTOTEST [C527777]
    PRECONDITIONS: To retrieve information from Site Server use steps:
    PRECONDITIONS: 1)To get class IDs and type IDs for <Sport>  use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Category ID (Sport id)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for types use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXXX?translationLang=LL?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   Notice XXXX is the type ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) To get a list of events' details use link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: *   Notice XXXX is the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: *   **'name'** to see the event name
    PRECONDITIONS: *   **'className'** to see the region/country name
    PRECONDITIONS: *   **'typeName'** to see the league name
    PRECONDITIONS: *   **'name'** on the market level - to see the market name
    PRECONDITIONS: *   **'name' **on the outcome level - to see selection name
    PRECONDITIONS: *   **'livePriceNum'/'livePriceDen'** in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: *   **'priceDec'** in the outcome level - to see odds for selection in decimal format
    PRECONDITIONS: - User can be logged in/logged out
    PRECONDITIONS: - User is on Home page or other <Sport> related
    """
    keep_browser_open = True

    def test_001_add_single_sport_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single <sport> selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        pass

    def test_002_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: *   Added selection is present
        EXPECTED: **From OX99**
        EXPECTED: * [Section is named Your Selections]
        EXPECTED: * 'Stake' box is NOT focused by default
        EXPECTED: Coral: Numeric keyboard with quick stake buttons are shown above 'Total Stake' and 'Estimated Returns' (when clicking on stake input field)
        EXPECTED: Ladbrokes: Numeric keyboard with quick stake buttons are shown above 'Total Stake' and 'Total Potential Returns' ((when clicking on stake input field))
        """
        pass

    def test_003_verify_selection_displaying(self):
        """
        DESCRIPTION: Verify selection displaying
        EXPECTED: **From OX99**
        EXPECTED: * Section is displayed as expandable section
        """
        pass

    def test_004_step_for_ox99verify_selection_information(self):
        """
        DESCRIPTION: **Step for OX99**
        DESCRIPTION: Verify selection information
        EXPECTED: The appropriate info is shown:
        EXPECTED: - selection name
        EXPECTED: - market name
        EXPECTED: - event name
        EXPECTED: - price
        EXPECTED: - stake box
        EXPECTED: - Est. Returns for that individual bet (Coral), Potential Returns (Ladbrokes)
        EXPECTED: - Remove ('X')' button
        """
        pass

    def test_005_tap_stake_box_mobile(self):
        """
        DESCRIPTION: Tap 'Stake' box (mobile)
        EXPECTED: *   Box becomes focused
        EXPECTED: **From OX99**
        EXPECTED: * Coral: Numeric keyboard with quick stake buttons are shown above 'Total Stake' and 'Estimated Returns'
        EXPECTED: * Ladbrokes: Numeric keyboard with quick stake buttons are shown above 'Total Stake' and 'Total Potential Returns'
        """
        pass

    def test_006_change_focus_on_bet_slip_slide_tap_somewhere_outside_stake_box(self):
        """
        DESCRIPTION: Change focus on Bet Slip slide (tap somewhere outside 'Stake' box)
        EXPECTED: *   'Stake' box is NOT focused
        EXPECTED: *   Numeric keyboard is NOT shown
        """
        pass

    def test_007_tap_stake_box_and_add_amount_to_bet_using_numeric_keyboard_or_quick_stake(self):
        """
        DESCRIPTION: Tap 'Stake' box and add amount to bet using numeric keyboard or quick stake
        EXPECTED: The following fields are changed due to selected stake:
        EXPECTED: *   Value in the **Stake** box
        EXPECTED: *   **Estimated Returns** (in format XX.XX)
        EXPECTED: *   **Total Stake** (in format XX.XX)
        EXPECTED: *   **Total Est. Returns** (in format XX.XX)
        EXPECTED: **From OX99:
        EXPECTED: Coral: 'Estimated Returns'; Ladbrokes: 'Potential Returns'
        """
        pass

    def test_008_close_betslip_for_mobile_only(self):
        """
        DESCRIPTION: Close Betslip (**for Mobile only**)
        EXPECTED: Betslip overlay is closed
        """
        pass

    def test_009_go_to_betslip_again(self):
        """
        DESCRIPTION: Go to Betslip  again
        EXPECTED: *  Selection and entered stake are remembered
        """
        pass
