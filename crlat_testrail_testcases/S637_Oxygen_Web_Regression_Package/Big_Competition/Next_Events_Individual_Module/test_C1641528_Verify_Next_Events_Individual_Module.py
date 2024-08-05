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
class Test_C1641528_Verify_Next_Events_Individual_Module(Common):
    """
    TR_ID: C1641528
    NAME: Verify Next Events Individual Module
    DESCRIPTION: This test case verifies Next Events Individual Module
    PRECONDITIONS: Link Open Bet TI:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Credentials:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Have Big Competition created in CMS
    PRECONDITIONS: Have Next Events Individual Module configured on current 'Big Competition'
    """
    keep_browser_open = True

    def test_001_load_oxygen_page_and_log_into_app(self):
        """
        DESCRIPTION: Load Oxygen page and log into app
        EXPECTED: Oxygen page is loaded
        EXPECTED: User successfully log into app
        """
        pass

    def test_002_navigate_to_all_sports__big_competition(self):
        """
        DESCRIPTION: Navigate to All Sports > "Big Competition"
        EXPECTED: 
        """
        pass

    def test_003_observe_next_events_individual_module(self):
        """
        DESCRIPTION: Observe 'Next Events Individual' module
        EXPECTED: Observe that:
        EXPECTED: * Events present belong to respective added events in CMS
        EXPECTED: * If there is only one event present it should take full width (mobile view)
        EXPECTED: * Card/List view is according to configuration set in CMS
        EXPECTED: * Card View/List View clickable icon to change view on 'Next Events' accordion
        EXPECTED: * Only primary market is shown
        """
        pass

    def test_004_set_max_display_to_n_events_to_displayset_next_events_individual_module_to_card_view_if_not_set_already_and_scroll_to_the_right_until_last_events_are_shown(self):
        """
        DESCRIPTION: Set Max Display to 'n' events to display
        DESCRIPTION: Set 'Next Events Individual' module to 'Card View' (if not set already) and scroll to the right until last events are shown
        EXPECTED: If there are more than e.g. 5 events (number of events that are set in CMS) present then there should be a CTA button: 'SHOW NEXT 'n' UPCOMING MATCHES'
        """
        pass

    def test_005_press_show_next_n_upcoming_matches_button(self):
        """
        DESCRIPTION: Press ''SHOW NEXT 'n' UPCOMING MATCHES'' button
        EXPECTED: Next 'n' events should be displayed
        """
        pass

    def test_006_select_any_event_from_card_view_list_and_verify_it_structure(self):
        """
        DESCRIPTION: Select any event from 'Card View' list and verify it structure
        EXPECTED: Next items are displayed for each event:
        EXPECTED: * 'Add to favorites' star
        EXPECTED: * Team abbreviations with flags/logo
        EXPECTED: * Start date and time
        EXPECTED: * Clickable link with the number of all available markets
        EXPECTED: * Price/Odds buttons and Name for each selection
        """
        pass

    def test_007_set_max_display_to_n_events_to_displayset_next_events_module_to_list_view_if_not_set_already_and_scroll_down_until_last_events_are_shown(self):
        """
        DESCRIPTION: Set Max Display to 'n' events to display
        DESCRIPTION: Set 'Next Events' module to 'List View' (if not set already) and scroll down until last events are shown
        EXPECTED: If there are more than e.g. 5 events (number of events that are set in CMS) present then there should be a CTA button: 'SHOW NEXT 'n' UPCOMING MATCHES'
        """
        pass

    def test_008_press_show_next_n_upcoming_matches_link(self):
        """
        DESCRIPTION: Press ''SHOW NEXT 'n' UPCOMING MATCHES'' link
        EXPECTED: Next 'n' events should be displayed
        """
        pass

    def test_009_select_any_event_from_the_list(self):
        """
        DESCRIPTION: Select any event from the list
        EXPECTED: Observe that events contain:
        EXPECTED: * 'Add to favorites' star
        EXPECTED: * Start date and time
        EXPECTED: * Clickable link with the number of all available markets
        EXPECTED: * Price/Odds buttons for each selection
        """
        pass

    def test_010_tap_on_add_to_favorites_icon_and_verify_if_the_event_is_present_in_the_favorites_list(self):
        """
        DESCRIPTION: Tap on 'Add to favorites' icon and verify if the event is present in the favorites list
        EXPECTED: * 'Add to favorites' icon becomes yellow
        EXPECTED: * The event is present in the favorites list
        """
        pass

    def test_011_tap_on_event_area_from_list_viewcard_view(self):
        """
        DESCRIPTION: Tap on event area from 'List View'/'Card view'
        EXPECTED: * All area should be clickable
        EXPECTED: * User is redirected to event page
        """
        pass

    def test_012_one_by_one_tap_on_each_selection_and_place_bet(self):
        """
        DESCRIPTION: One by one tap on each selection and place bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_013_go_to_backoffice_see_preconditions_and_set_sstrated__true_attributewait_until_one_event_starts(self):
        """
        DESCRIPTION: Go to backoffice (see preconditions) and set 'sStrated = true' attribute
        DESCRIPTION: Wait until one event starts
        EXPECTED: * Event is removed from Next Events Individual module and displayed between 'Big Competition' tab and 'Next Events' module
        EXPECTED: * It is located at the right of any other live event already present
        EXPECTED: * It should be displayed in Hero view (Card view)
        EXPECTED: * Only primary market is shown
        EXPECTED: * If it is the only live event then it should take full width (mobile view)
        """
        pass
