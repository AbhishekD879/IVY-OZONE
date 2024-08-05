import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28973_Verify_Next_Races_widget(Common):
    """
    TR_ID: C28973
    NAME: Verify Next Races widget
    DESCRIPTION: This test case verifies Next Races widget displaying in application
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. User is logged in to CMS
    PRECONDITIONS: 2. Enable the 'Next Races' widget in CMS > widgets > next races
    PRECONDITIONS: 3. For changing the number of selection for displaying in 'Next Races' widget in CMS > system configuration > structure > NextRaces > set the number in 'numberOfSelections' field
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: **Steps:**
    """
    keep_browser_open = True

    def test_001_verify_next_races_widget_displaying_if_there_are_no_available_events_to_display(self):
        """
        DESCRIPTION: Verify 'Next Races' widget displaying if there are no available events to display
        EXPECTED: 'Next Races' widget is NOT displayed in application
        """
        pass

    def test_002__in_cms_value_is_not_set_in_numberofselections_field_back_to_the_app_verify_next_races_widget_displaying_verify_the_number_of_selections(self):
        """
        DESCRIPTION: * In CMS value is NOT set in 'numberOfSelections' field.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Verify 'Next Races' widget displaying.
        DESCRIPTION: * Verify the number of selections.
        EXPECTED: Next Races widget is displayed with next elements:
        EXPECTED: * 'Next Races' header
        EXPECTED: * Event section with top 3 selections for each event
        EXPECTED: * 'View Full Race Card' link for each event
        """
        pass

    def test_003__in_cms_set_the_value_in_numberofselections_field_back_to_the_app_verify_next_races_widget_displaying_verify_the_number_of_selections(self):
        """
        DESCRIPTION: * In CMS set the value in 'numberOfSelections' field.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Verify 'Next Races' widget displaying.
        DESCRIPTION: * Verify the number of selections.
        EXPECTED: Next Races widget is displayed with next elements:
        EXPECTED: * 'Next Races' header
        EXPECTED: * Event section with set number of selections for each event (Set in CMS)
        EXPECTED: * 'View Full Race Card' link for each event
        """
        pass

    def test_004_clicktap_on_selection_from_the_widget(self):
        """
        DESCRIPTION: Click/Tap on selection from the widget
        EXPECTED: *   Selection is successfully added to Betslip
        EXPECTED: *   Selection is marked as added in Next Races widget
        """
        pass

    def test_005_place_a_bet_for_added_selection(self):
        """
        DESCRIPTION: Place a bet for added selection
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Selection is unmarked in Next Races widget
        """
        pass

    def test_006_click_ontap_view_full_race_card_link(self):
        """
        DESCRIPTION: Click on/Tap 'View Full Race Card' link
        EXPECTED: User is redirected to Event Details page
        """
        pass

    def test_007_verify_widget_events_list_updating_after_event_from_the_list_is_already_startedfinished(self):
        """
        DESCRIPTION: Verify Widget Events list updating after event from the list is already started/finished
        EXPECTED: Started/Finished event is not displayed in the widget anymore
        """
        pass

    def test_008_swipe_widget_to_view_all_list_of_available_events(self):
        """
        DESCRIPTION: Swipe widget to view all list of available events
        EXPECTED: All events can be viewed successfully
        """
        pass

    def test_009_verify_widget_view_in_landscape_and_portrait_orientation_on_tablet_device(self):
        """
        DESCRIPTION: Verify widget view in landscape and portrait orientation on tablet device
        EXPECTED: Widget is displayed and re-sized appropriately to selected screen mode
        """
        pass

    def test_010_verify_event_with_silks_available_on_the_next_races_widget(self):
        """
        DESCRIPTION: Verify event with silks available on the "Next Races" widget
        EXPECTED: * Correct silks are displayed for mapped selections
        EXPECTED: * Generic silks are displayed for missed selections
        """
        pass

    def test_011_verify_event_with_absolutely_no_silks_are_available_for_all_runners_within_a_single_race(self):
        """
        DESCRIPTION: Verify event with absolutely no silks are available for all runners within a single race
        EXPECTED: * Generic silks are NOT displayed
        EXPECTED: * Only runner numbers are displayed
        """
        pass
