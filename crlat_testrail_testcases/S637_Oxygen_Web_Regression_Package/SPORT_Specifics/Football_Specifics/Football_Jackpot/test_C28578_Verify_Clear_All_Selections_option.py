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
class Test_C28578_Verify_Clear_All_Selections_option(Common):
    """
    TR_ID: C28578
    NAME: Verify 'Clear All Selections' option
    DESCRIPTION: This test case verifies 'Clear All Selections' option (i.e. button on the bottom of the page) on Football Jackpot page
    PRECONDITIONS: 1) To retrieve a list of Football Jackpot pools please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?simpleFilter=pool.type:equals:V15&simpleFilter=pool.isActive&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Make sure there is at least one active pool available to be displayed on front-end
    PRECONDITIONS: 3) The user may be logged in or logged out for the functionality to work
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: *   Football Jackpot Page is opened with 15 events available
        EXPECTED: *   Each event has 3 buttons
        """
        pass

    def test_004_make_one_or_more_selections_from_the_football_jackpot_page_manually(self):
        """
        DESCRIPTION: Make one or more selections from the Football Jackpot page manually
        EXPECTED: Selections that were made are highlighted
        """
        pass

    def test_005_tap_clear_all_selections_button(self):
        """
        DESCRIPTION: Tap 'Clear All Selections' button
        EXPECTED: *   Text label is changed to: 'Confirm ?'
        EXPECTED: *   The button background is turned to Orange
        """
        pass

    def test_006_do_not_tap_confirm__button_during_5_sec(self):
        """
        DESCRIPTION: Do not tap 'Confirm ?' button during 5 sec
        EXPECTED: After 5 seconds the button goes back to the 'Clear All Selections' state
        """
        pass

    def test_007_tap_clear_all_selections_button_again_and_then_tap_confirm_(self):
        """
        DESCRIPTION: Tap 'Clear All Selections' button again and then tap 'Confirm ?'
        EXPECTED: All selections are cleared from the Football Jackpot coupon
        EXPECTED: All highlighted buttons are now unhighlighted
        """
        pass

    def test_008_tap_lucky_dip_button(self):
        """
        DESCRIPTION: Tap 'Lucky Dip' button
        EXPECTED: Random selections are made and highlighted
        """
        pass

    def test_009_repeat_step_5_7(self):
        """
        DESCRIPTION: Repeat step №5-7
        EXPECTED: 
        """
        pass
