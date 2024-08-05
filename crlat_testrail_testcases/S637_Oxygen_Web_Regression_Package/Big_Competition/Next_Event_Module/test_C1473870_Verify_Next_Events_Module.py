import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1473870_Verify_Next_Events_Module(Common):
    """
    TR_ID: C1473870
    NAME: Verify Next Events Module
    DESCRIPTION: This test case verifies Next Events Module
    PRECONDITIONS: Link Open Bet TI:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Credentials:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Have Big Competition created in CMS
    PRECONDITIONS: Have Next Events Module configured on current 'Big Competition'
    """
    keep_browser_open = True

    def test_001_load_oxygen_page_and_log_into_app(self):
        """
        DESCRIPTION: Load Oxygen page and log into app
        EXPECTED: - Oxygen page is loaded
        EXPECTED: - User successfully log into app
        """
        pass

    def test_002_navigate_to_all_sports__big_competition(self):
        """
        DESCRIPTION: Navigate to All Sports > "Big Competition"
        EXPECTED: "Big Competition" landing page is loaded
        """
        pass

    def test_003_verify_big_competition_tab_when_there_are_no_live_events(self):
        """
        DESCRIPTION: Verify 'Big Competition' tab when there are no live events
        EXPECTED: 'Next Events' module is under 'Big Competition' tab
        """
        pass

    def test_004_verify_big_competition_tab_with_live_events(self):
        """
        DESCRIPTION: Verify 'Big Competition' tab with live events
        EXPECTED: Live events are present above 'Next Events' module
        """
        pass

    def test_005_verify_next_events_module(self):
        """
        DESCRIPTION: Verify 'Next Events' module
        EXPECTED: - Events present belong to respective Big Competition type Id
        EXPECTED: - If there is only one event present it should take full width (mobile view)
        EXPECTED: - Card/List view is according to configuration set in CMS
        EXPECTED: - Card View/List View clickable icon to change view on 'Next Events' accordion
        EXPECTED: ![](index.php?/attachments/get/20325)
        EXPECTED: ![](index.php?/attachments/get/20326)
        EXPECTED: - Number of events are according to configuration set in CMS
        EXPECTED: - Only primary market is shown
        """
        pass

    def test_006_set_next_events_module_to_card_view_if_not_set_already_and_scroll_to_the_right_until_last_events_are_shown(self):
        """
        DESCRIPTION: Set 'Next Events' module to 'Card View' (if not set already) and scroll to the right until last events are shown
        EXPECTED: Please not 'n' - this is number of events that are set in CMS
        EXPECTED: - If there are more than e.g. 5 events (number of events that are set in CMS) present then there should be a CTA button: 'SHOW NEXT 'n' UPCOMING MATCHES'
        EXPECTED: ![](index.php?/attachments/get/20319)
        EXPECTED: - If there are e.g. 5 or less events present then CTA button should be absent
        """
        pass

    def test_007_press_show_next_n_upcoming_matches_button(self):
        """
        DESCRIPTION: Press ''SHOW NEXT 'n' UPCOMING MATCHES'' button
        EXPECTED: Next 'n' events should be displayed
        """
        pass

    def test_008_select_any_event_from_card_view_and_verify_it_structure(self):
        """
        DESCRIPTION: Select any event from 'Card View' and verify it structure
        EXPECTED: Next items are displayed for each event:
        EXPECTED: - 'Add to favorites' star
        EXPECTED: - Team abbreviations with flags/logo
        EXPECTED: - Start date and time
        EXPECTED: - Clickable link with the number of all available markets
        EXPECTED: - Price/Odds buttons and Name for each selection
        """
        pass

    def test_009_set_next_events_module_to_list_view_if_not_set_already_and_scroll_down_until_last_events_are_shown(self):
        """
        DESCRIPTION: Set 'Next Events' module to 'List View' (if not set already) and scroll down until last events are shown
        EXPECTED: Please not 'n' - this is number of events that are set in CMS
        EXPECTED: - If there are more than e.g. 5 events (number of events that are set in CMS) present then there should be a link: 'SHOW NEXT 'n' UPCOMING MATCHES'
        EXPECTED: ![](index.php?/attachments/get/20327)
        EXPECTED: - If there are e.g. 5 or less events present then link should be absent
        """
        pass

    def test_010_press_show_next_n_upcoming_matches_link(self):
        """
        DESCRIPTION: Press ''SHOW NEXT 'n' UPCOMING MATCHES'' link
        EXPECTED: Next 'n' events should be displayed
        """
        pass

    def test_011_select_any_event_from_the_list(self):
        """
        DESCRIPTION: Select any event from the list
        EXPECTED: On the top of the list there is a header with selections names
        EXPECTED: ![](index.php?/attachments/get/20331)
        EXPECTED: Next items are displayed for each event:
        EXPECTED: - 'Add to favorites' star
        EXPECTED: - Start date and time
        EXPECTED: - Clickable link with the number of all available markets
        EXPECTED: - Price/Odds buttons for each selection
        """
        pass

    def test_012_tap_on_add_to_favorites_icon_and_verify_if_the_event_is_present_in_the_favorites_list(self):
        """
        DESCRIPTION: Tap on 'Add to favorites' icon and verify if the event is present in the favorites list
        EXPECTED: - 'Add to favorites' icon becomes yellow
        EXPECTED: - The event is present in the favorites list
        """
        pass

    def test_013_tap_on_event_area_from_list_viewcard_view(self):
        """
        DESCRIPTION: Tap on event area from 'List View'/'Card view'
        EXPECTED: - All area should be clickable
        EXPECTED: - User is redirected to event page
        """
        pass

    def test_014_one_by_one_tap_on_each_selection_and_place_bet(self):
        """
        DESCRIPTION: One by one tap on each selection and place bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_015_go_to_backoffice_see_preconditions_and_set_sstrated__true_attributeindexphpattachmentsget20335wait_until_one_event_starts(self):
        """
        DESCRIPTION: Go to backoffice (see preconditions) and set 'sStrated = true' attribute.
        DESCRIPTION: ![](index.php?/attachments/get/20335)
        DESCRIPTION: Wait until one event starts
        EXPECTED: - Event is removed from Next Events module and displayed into Live section
        EXPECTED: - It is located at the right of any other live event already present
        EXPECTED: - It should be displayed in Hero view (Card view)
        EXPECTED: - Only primary market is shown
        EXPECTED: - If it is the only live event then it should take full width (mobile view)
        """
        pass

    def test_016_increase_prices_for_any_events_in_next_event_module_in_card_list_view_in_backoffice_ti_tool_and_verify_the_corresponding_events(self):
        """
        DESCRIPTION: Increase prices for any events in Next Event Module in Card /List View in Backoffice TI tool and verify the corresponding events
        EXPECTED: Prices are instantly updated in real time
        """
        pass

    def test_017_decrease_prices_for_any_events_in_next_event_module_in_card_list_view_in_backoffice_ti_tool_and_verify_the_corresponding_events(self):
        """
        DESCRIPTION: Decrease prices for any events in Next Event Module in Card /List View in Backoffice TI tool and verify the corresponding events
        EXPECTED: Prices are instantly updated in real time
        """
        pass
