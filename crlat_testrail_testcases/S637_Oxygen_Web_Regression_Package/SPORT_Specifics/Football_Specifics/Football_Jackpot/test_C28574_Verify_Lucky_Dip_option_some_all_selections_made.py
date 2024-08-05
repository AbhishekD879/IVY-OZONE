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
class Test_C28574_Verify_Lucky_Dip_option_some_all_selections_made(Common):
    """
    TR_ID: C28574
    NAME: Verify 'Lucky Dip' option (some/all selections made)
    DESCRIPTION: This test case verifies 'Lucky Dip' option (i.e. button on the bottom of the page) on Football Jackpot page, when there are some/all selections made by user
    DESCRIPTION: AUTOTEST [C9689048]
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

    def test_004_make_one_or_more_selections_manually_from_the_football_jackpot_page(self):
        """
        DESCRIPTION: Make one or more selections manually from the Football Jackpot page
        EXPECTED: Selections that were made are highlighted
        """
        pass

    def test_005_tap_lucky_dip_button(self):
        """
        DESCRIPTION: Tap 'Lucky Dip' button
        EXPECTED: Warning pop-up is shown
        """
        pass

    def test_006_verify_warning_pop_up(self):
        """
        DESCRIPTION: Verify warning pop-up
        EXPECTED: *   Warning message: "**Proceed to replace your selections with Lucky Dip selections?**" is shown
        EXPECTED: *   Two buttons are present: '**Accept**' and '**Cancel**'
        """
        pass

    def test_007_tap_cancel_button(self):
        """
        DESCRIPTION: Tap 'CANCEL' button
        EXPECTED: *   Lucky Dip is not processed
        EXPECTED: *   All previously manually made selections are present and remain highlighted
        """
        pass

    def test_008_repeat_step_5(self):
        """
        DESCRIPTION: Repeat step №5
        EXPECTED: 
        """
        pass

    def test_009_tap_accept_button(self):
        """
        DESCRIPTION: Tap 'ACCEPT' button
        EXPECTED: Random selections are made and highlighted (1 random selection from each **active **event) replacing previously made selections
        """
        pass
