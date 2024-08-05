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
class Test_C28866_To_edit_Making_One_Race_Single_Selections(Common):
    """
    TR_ID: C28866
    NAME: [To edit] Making One Race Single Selections
    DESCRIPTION: Steps 5,8,10,13,15 are outdated
    DESCRIPTION: This test case verifies Making One Single Selection.
    PRECONDITIONS: To retrieve an information from Site Server use steps:
    PRECONDITIONS: 1) To get class IDs for <Race> sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id = 21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2) To get a list of events for classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: **'priceTypeCodes'=**'SP'
    PRECONDITIONS: **'priceTypeCodes'=**'LP'
    PRECONDITIONS: **'priceTypeCodes'=**'SP,LP'
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_add_single_sp_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single 'SP' selection to bet slip
        EXPECTED: 1.  Single bet is added to bet slip.
        EXPECTED: 2.  Bet slip counter is increased to 1.
        """
        pass

    def test_005_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: * Bet Slip with bet details is opened
        EXPECTED: * Numeric keyboard with 'quick stakes' buttons are shown by default
        """
        pass

    def test_006_enter_stake_for_sp_selection(self):
        """
        DESCRIPTION: Enter stake for 'SP' selection
        EXPECTED: 1.  The total wager for the bet is entered.
        EXPECTED: 2.  Amounts of **'Est. Returns'**, **'Total Est. Returns'** are equal to 'N/A' value
        EXPECTED: 3.  **'Total Stake'** is changed due to selected stake.
        """
        pass

    def test_007_tap_close_button(self):
        """
        DESCRIPTION: Tap 'Close' button
        EXPECTED: Page from which navigation was is shown
        """
        pass

    def test_008_go_to_bet_slip_again(self):
        """
        DESCRIPTION: Go to Bet Slip  again
        EXPECTED: * Selection and entered stake are remembered
        EXPECTED: * Numeric keyboard with 'quick stakes' buttons are shown by default
        """
        pass

    def test_009_add_lp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'LP' selection to the bet Slip
        EXPECTED: 1.  Single bet is added to the Bet Slip
        EXPECTED: 2.  Bet slip indicator is increased
        """
        pass

    def test_010_enter_a_stake_for_lp_selectionpoint_2_of_expected_result___should_be_updated___estimated_returns_is__na_the_same_behaviour_on_prod(self):
        """
        DESCRIPTION: Enter a stake for 'LP' selection
        DESCRIPTION: [Point 2 of expected result - Should be updated? - "Estimated Returns" is  N/A, the same behaviour on prod]
        EXPECTED: 1.  The total wager for the bet is entered.
        EXPECTED: 2.  Amounts of **'Estimated Returns'**,** 'Total Est. Returns'** are calculated according to the predefined formula
        EXPECTED: 3.  **'Total Stake' ** is changed due to selected stake
        """
        pass

    def test_011_repeat_steps_7___8(self):
        """
        DESCRIPTION: Repeat steps #7 - 8
        EXPECTED: 
        """
        pass

    def test_012_add_selection_to_the_bet_slip_for_the_event_with_attribute_pricetypecodes__lp_sp(self):
        """
        DESCRIPTION: Add selection to the Bet Slip for the event with attribute **'priceTypeCodes'** = 'LP, SP'
        EXPECTED: 1.  Single Bet is added to the Bet Slip
        EXPECTED: 2.  Bet Slip counter is increased to 1
        """
        pass

    def test_013_on_a_bet_slip_select_sp_price_from_the_dropdown(self):
        """
        DESCRIPTION: On a Bet Slip select 'SP' price from the dropdown
        EXPECTED: 1. Selection is shown
        EXPECTED: 2. Numeric keyboard with quick stakes' buttons are shown
        """
        pass

    def test_014_repeat_steps__6___8(self):
        """
        DESCRIPTION: Repeat steps # 6 - 8
        EXPECTED: 
        """
        pass

    def test_015_on_a_bet_slip_select_lp_price_from_the_dropdown_control(self):
        """
        DESCRIPTION: On a Bet Slip select 'LP' price from the dropdown control
        EXPECTED: 1. Selection is shown
        EXPECTED: 2. Numeric keyboard with 'quick stakes' buttons are shown
        """
        pass

    def test_016_repeat_steps__11___12(self):
        """
        DESCRIPTION: Repeat steps # 11 - 12
        EXPECTED: 
        """
        pass

    def test_017_add_suspended_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add suspended selection to the Bet Slip
        EXPECTED: 1.  It is impossible to add suspended selections to the Bet Slip
        EXPECTED: 2.  Suspended bubble is disabled
        """
        pass
