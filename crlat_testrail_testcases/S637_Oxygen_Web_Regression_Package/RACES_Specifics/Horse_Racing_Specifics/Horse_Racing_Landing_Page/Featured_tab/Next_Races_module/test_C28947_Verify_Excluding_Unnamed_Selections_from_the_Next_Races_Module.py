import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28947_Verify_Excluding_Unnamed_Selections_from_the_Next_Races_Module(Common):
    """
    TR_ID: C28947
    NAME: Verify Excluding 'Unnamed' Selections from the 'Next Races' Module
    DESCRIPTION: This test case verifies how to generate event in the Open Bet system in order to check excluding 'unnamed
    DESCRIPTION: selections from the 'Next Races' module
    DESCRIPTION: 2. Make sure there is an event in the 'Next Races' module which contains 'Unnamed Favorite' and 'Unnamed 2nd Favorite' selections
    PRECONDITIONS: 1) In order to open OpenBet system (TI tool) use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: 2) Make sure there is an event in the 'Next Races' module which contains 'Unnamed Favorite' and 'Unnamed 2nd Favorite' selections (On Selection level in TI tool choose 'Unnamed Favorite' and 'Unnamed 2nd Favorite' values within 'Selection Type' field)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is opened
        EXPECTED: * 'Next Races' module is displayed
        """
        pass

    def test_003_open_bet_system_ti_tool_and_find_the_event_which_is_displayed_in_the_next__races_module(self):
        """
        DESCRIPTION: Open Bet system (TI tool) and find the event which is displayed in the 'Next  Races' module
        EXPECTED: Event is shown
        """
        pass

    def test_004_go_to_the_win_or_each_way_market_and_remove_all_selections_except_onemake_sure_two_unnamed_selections_remain(self):
        """
        DESCRIPTION: Go to the 'Win or Each Way' market and remove all selections except one
        DESCRIPTION: Make sure two 'unnamed' selections remain
        EXPECTED: Only three selections are available for the 'Win or Each Way' market
        """
        pass

    def test_005_go_to_the_oxygen_application_and_check_the_event_in_the_next_races_module(self):
        """
        DESCRIPTION: Go to the Oxygen application and check the event in the 'Next Races' module
        EXPECTED: * Only one selection is shown for this event
        EXPECTED: * 'Unnamed' selections are excluded from the 'Next Races' module
        """
        pass

    def test_006_for_mobile_and_tabletgo_to_the_homepage___tap_next_races_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Go to the homepage -> tap 'Next Races' tab from the module selector ribbon
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 'Next Races' module is shown
        """
        pass

    def test_007_for_mobile_and_tabletrepeat_steps__3___5(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Repeat steps # 3 - 5
        EXPECTED: 
        """
        pass

    def test_008_for_desktopgo_to_the_desktop_homepage___check_next_races_carousel_under_the_in_play_section(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' carousel under the 'In-Play' section
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' section is shown
        """
        pass

    def test_009_for_desktoprepeat_steps__3___5(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 3 - 5
        EXPECTED: 
        """
        pass
