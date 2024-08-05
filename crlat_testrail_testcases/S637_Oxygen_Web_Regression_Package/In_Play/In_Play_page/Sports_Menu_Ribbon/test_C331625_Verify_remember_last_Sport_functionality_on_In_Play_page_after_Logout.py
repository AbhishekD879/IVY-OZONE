import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C331625_Verify_remember_last_Sport_functionality_on_In_Play_page_after_Logout(Common):
    """
    TR_ID: C331625
    NAME: Verify remember last Sport functionality on In-Play page after Logout
    DESCRIPTION: This test case verifies remember last Sport functionality on In-Play page after Logout
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Category, where X.XX - the latest OpenBet release
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Log in
    """
    keep_browser_open = True

    def test_001_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default
        """
        pass

    def test_002_choose_any_sports_icon(self):
        """
        DESCRIPTION: Choose any Sports icon
        EXPECTED: * Selected Sports tab is underlined by red line
        EXPECTED: * The appropriate content is displayed for selected Sports
        """
        pass

    def test_003_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User is logged out successfully
        """
        pass

    def test_004_navigate_to_in_play_page(self):
        """
        DESCRIPTION: Navigate to 'In-Play' page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        """
        pass

    def test_005_go_out_from_in_play_page(self):
        """
        DESCRIPTION: Go out from 'In-Play' page
        EXPECTED: 
        """
        pass

    def test_006_log_in_again_with_the_same_user_account(self):
        """
        DESCRIPTION: Log in again with the same user account
        EXPECTED: User is logged in successfully
        """
        pass

    def test_007_navigate_to_in_play_page(self):
        """
        DESCRIPTION: Navigate to 'In-Play' page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * Tab from step 2 is selected and underlined by red line
        """
        pass

    def test_008_log_into_application_using_another_account(self):
        """
        DESCRIPTION: Log into application using another account
        EXPECTED: User is logged in successfully
        """
        pass

    def test_009_navigate_to_in_play_page(self):
        """
        DESCRIPTION: Navigate to 'In-Play' page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        """
        pass

    def test_010_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User is logged out successfully
        """
        pass

    def test_011_log_into_application_again_but_trigger_situation_when_there_are_no_in_play_events_for_saved_sport(self):
        """
        DESCRIPTION: Log into application again but trigger situation when there are no In-Play events for saved sport
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        """
        pass
