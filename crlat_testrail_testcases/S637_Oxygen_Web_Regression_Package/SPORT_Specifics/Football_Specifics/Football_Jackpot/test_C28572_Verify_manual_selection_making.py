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
class Test_C28572_Verify_manual_selection_making(Common):
    """
    TR_ID: C28572
    NAME: Verify manual selection making
    DESCRIPTION: This test case verifies manual selection making on Football Jackpot page
    DESCRIPTION: AUTOTEST [C9647726]
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
        EXPECTED: Selections that were made are highlighted in green
        """
        pass

    def test_005_deselect_these_made_in_step4_selections_manually(self):
        """
        DESCRIPTION: Deselect these (made in step№4) selections manually
        EXPECTED: Deselected items are now unhighlighted
        """
        pass

    def test_006_manually_make_two_or_three_selections_for_each_event(self):
        """
        DESCRIPTION: Manually make two or three selections for each event
        EXPECTED: *   It is possible to select more than one outcome for each event
        EXPECTED: *   There is no restriction on the number of possible selections (i.e. all 45 selections could be made)
        """
        pass
