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
class Test_C28865_To_edit_Making_a_Few_Race_Singles_Selections(Common):
    """
    TR_ID: C28865
    NAME: [To edit] Making a Few Race Singles Selections
    DESCRIPTION: Steps 19,21,23 are outdated
    DESCRIPTION: This test case verifies how several single selections should be added to the Bet Slip
    DESCRIPTION: AUTOTEST [C820554]
    PRECONDITIONS: 1. User balance is sufficient to place bets
    PRECONDITIONS: 2. To retrieve information from the Site Server use the following steps:
    PRECONDITIONS: To get class IDs for <Race> sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: XX - sport category id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse racing category id = 21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: To get a list of events for classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: XX - spoet category id
    PRECONDITIONS: YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: 'name' to see the event name
    PRECONDITIONS: 'startTime' to see the event start time
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

    def test_004_make_a_few_selection_for_the_same_market(self):
        """
        DESCRIPTION: Make a few selection for the same market
        EXPECTED: 1.  Selected price / odds buttons are highlighted in green
        EXPECTED: 2.  Betslip counter is increased to value which is equal to quantity of added selections
        EXPECTED: 3.  Call is made to add outcome selections to the betslip
        """
        pass

    def test_005_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip with bets details is opened
        """
        pass

    def test_006_add_20_single_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 20 single selections to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_007_click_binremove_button(self):
        """
        DESCRIPTION: Click 'Bin'(Remove) button
        EXPECTED: All selections are removed from betslip
        """
        pass

    def test_008_try_to_add_21st_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Try to add 21st selection to the Bet Slip
        EXPECTED: 1.  Ability to add selection is restricted
        EXPECTED: 2.  'Maximum number of selections allowed on betslip is 20' error message appears
        """
        pass

    def test_009_unselect_selection_from_the_event_page(self):
        """
        DESCRIPTION: Unselect selection from the event page
        EXPECTED: 1.  The price becomes highlighted in grey
        EXPECTED: 2.  Bet Slip counter is decreased by 1
        EXPECTED: 3.  Remove call is made to remove the outcome selection from the bet slip
        """
        pass

    def test_010_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Removed selection is no more displayed in the Bet Slip
        """
        pass

    def test_011_log_in_to_the_application(self):
        """
        DESCRIPTION: Log in to the application
        EXPECTED: 
        """
        pass

    def test_012_make_selections_for_different_markets(self):
        """
        DESCRIPTION: Make selections for different markets
        EXPECTED: The same as in step #4
        """
        pass

    def test_013_repeat_steps__5___13(self):
        """
        DESCRIPTION: Repeat steps # 5 - 13
        EXPECTED: 
        """
        pass

    def test_014_make_selections_for_different_events(self):
        """
        DESCRIPTION: Make selections for different events
        EXPECTED: The same as in step #4
        """
        pass

    def test_015_repeat_steps__5___13(self):
        """
        DESCRIPTION: Repeat steps # 5 - 13
        EXPECTED: 
        """
        pass

    def test_016_make_selections_for_different_sports(self):
        """
        DESCRIPTION: Make selections for different sports
        EXPECTED: The same as in step #4
        """
        pass

    def test_017_repeat_steps_5___13(self):
        """
        DESCRIPTION: Repeat steps #5 - 13
        EXPECTED: 
        """
        pass

    def test_018_add_several_selections_from_the_event_page___go_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Add several selections from the event page -> Go to Horse Racing landing page
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_019_add_selection_from_the_next_4_module(self):
        """
        DESCRIPTION: Add selection from the 'Next 4' module
        EXPECTED: 1.  Bet Slip counter is increased by 1
        EXPECTED: 2.  Bet Slip IS NOT opened automatically if some selections are already added to it
        """
        pass

    def test_020_remove_all_selection_from_the_bet_slip(self):
        """
        DESCRIPTION: Remove all selection from the Bet Slip
        EXPECTED: 1.  Selections are removed from the Bet Slip
        """
        pass

    def test_021_go_to_the_horse_racing_sport____add_selection_from_the_next_4_module(self):
        """
        DESCRIPTION: Go to the Horse Racing sport - > add selection from the 'Next 4' module
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Bet details are displayed
        """
        pass

    def test_022_add_several_selections_to_the_bet_slip___close_browser_window(self):
        """
        DESCRIPTION: Add several selections to the Bet Slip -> close browser window
        EXPECTED: Browser window is closed
        """
        pass

    def test_023_load_invictus___go_to_the_bet_slip(self):
        """
        DESCRIPTION: Load Invictus -> go to the Bet Slip
        EXPECTED: Added selections are not remembered in the Bet Slip
        """
        pass
