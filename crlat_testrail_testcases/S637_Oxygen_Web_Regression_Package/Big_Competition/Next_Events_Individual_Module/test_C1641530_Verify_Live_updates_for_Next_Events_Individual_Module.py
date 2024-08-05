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
class Test_C1641530_Verify_Live_updates_for_Next_Events_Individual_Module(Common):
    """
    TR_ID: C1641530
    NAME: Verify Live updates for Next Events Individual Module
    DESCRIPTION: 
    PRECONDITIONS: Link Open Bet TI:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Credentials:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: World Cup' competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: 'Featured' tab should be created, set up and enabled in CMS -> 'World Cup' competition
    PRECONDITIONS: 'Next events Individual module should be created, set up and enabled in CMS
    PRECONDITIONS: List of individual added events should be configured in 'Next events Individual' module
    PRECONDITIONS: To verify valid price updates and suspended/unsuspended status see microservice - Development tool> Network> WS> /?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: App loads successfully
        """
        pass

    def test_002_navigate_to_big_competition___groups_tab___group_x_tab___next_events_individual_module(self):
        """
        DESCRIPTION: Navigate to 'Big Competition' -> 'Groups' tab -> 'Group x' tab -> 'Next Events Individual' module
        EXPECTED: 'Next Events Individual' module is displayed successfully
        """
        pass

    def test_003_in_backoffice_tool_change_the_price_for_any_selection_from_next_events_individual_module_and_save_changes(self):
        """
        DESCRIPTION: In Backoffice tool change the price for any selection from 'Next Events Individual' module and save changes
        EXPECTED: 
        """
        pass

    def test_004_verify_that_price_is_updated_automatically(self):
        """
        DESCRIPTION: Verify that price is updated automatically
        EXPECTED: Corresponding 'Price/Odds' selection displays new price and for a few seconds it changes its color to:
        EXPECTED: * blue color if price has decreased
        EXPECTED: * pink color if price has increased
        """
        pass

    def test_005_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: The same price is displayed for the selection
        """
        pass

    def test_006_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        EXPECTED: All prices are displayed in Decimal format
        """
        pass

    def test_007_repeat_steps_2_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 2-5 for logged in user
        EXPECTED: Expected results are the same
        """
        pass

    def test_008_navigate_to_big_competition___groups_tab___group_x_tab___next_events_individual_module(self):
        """
        DESCRIPTION: Navigate to 'Big Competition' -> 'Groups' tab -> 'Group x' tab -> 'Next Events Individual' module
        EXPECTED: 'Next Events Individual' module is displayed successfully
        """
        pass

    def test_009_suspend_selection_in_backoffice_tool_trigger_the_following_situation_for_this_eventstatus_s(self):
        """
        DESCRIPTION: Suspend selection in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: Status= "S"
        EXPECTED: 
        """
        pass

    def test_010_verify_that_selection_is_suspended_automatically(self):
        """
        DESCRIPTION: Verify that selection is suspended automatically
        EXPECTED: Corresponding Price/Odds selection is displayed as greyed out and become disabled
        """
        pass

    def test_011_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Selection is still disabled
        """
        pass

    def test_012_unsuspend_selection_in_backoffice_tool_trigger_the_following_situation_for_this_eventstatus_a(self):
        """
        DESCRIPTION: Unsuspend selection in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: Status= "A"
        EXPECTED: Corresponding Price/Odds selection becomes active
        """
        pass

    def test_013_go_to_settings_and_switch_odds_format_to_fractional(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Fractional
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_9_13_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 9-13 for logged in user
        EXPECTED: Expected results are the same
        """
        pass

    def test_015_repeat_steps_9_13_but_in_backoffice_tool_suspendunsuspend_on_event_and_market_level(self):
        """
        DESCRIPTION: Repeat steps 9-13, but in Backoffice tool suspend/unsuspend on Event and Market level
        EXPECTED: Expected results are the same
        """
        pass

    def test_016_navigate_to_big_competition___groups_tab___group_x_tab___next_events_individual_module(self):
        """
        DESCRIPTION: Navigate to 'Big Competition' -> 'Groups' tab -> 'Group x' tab -> 'Next Events Individual' module
        EXPECTED: 'Next Events Individual' module is displayed successfully
        """
        pass

    def test_017_in_backoffice_tool_and_set_any_selection_from_next_events_individual_module_to_not_displayed_and_save_changes(self):
        """
        DESCRIPTION: In Backoffice tool and set any selection from 'Next Events Individual' module to 'Not Displayed' and save changes
        EXPECTED: Corresponding selection should not be displayed
        """
        pass

    def test_018_back_to_backoffice_tool_and_set_selection_to_displayed_and_save_changesrefresh_page(self):
        """
        DESCRIPTION: Back to Backoffice tool and set selection to 'Displayed' and save changes
        DESCRIPTION: Refresh page
        EXPECTED: Corresponding selection should be displayed in Oxygen app
        """
        pass

    def test_019_repeat_steps_16_18_but_in_backoffice_tool_displayundisplay_on_event_and_market_level(self):
        """
        DESCRIPTION: Repeat steps 16-18, but in Backoffice tool Display/Undisplay on Event and Market level
        EXPECTED: Expected results are the same
        """
        pass
