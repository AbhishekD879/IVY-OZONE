import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1440852_Verify_navigational_arrows_and_scrolling_for_certain_sections_widgets_across_the_app_for_Desktop(Common):
    """
    TR_ID: C1440852
    NAME: Verify navigational arrows and scrolling for certain sections/widgets across the app for Desktop
    DESCRIPTION: This test case verifies navigational arrows and scrolling behavior for certain sections/widgets across the application for Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen application on Desktop
        EXPECTED: Homepage is loaded successfully
        """
        pass

    def test_002_verify_displaying_of_next_races_section_when_only_1_event_is_available(self):
        """
        DESCRIPTION: Verify displaying of 'Next Races' section when only 1 event is available
        EXPECTED: * 'Next Races' section is positioned below the In-Play section on the homepage
        EXPECTED: * Event card is displayed within 'Next Races' section
        """
        pass

    def test_003_hover_the_mouse_over_the_next_races_section(self):
        """
        DESCRIPTION: Hover the mouse over the 'Next Races' section
        EXPECTED: Navigation arrows don't appear on both sides of the section
        """
        pass

    def test_004_verify_displaying_of_next_races_section_when_containing_event_cards_are_not_fitting_on_selected_screen_size_more_than_4_for_example(self):
        """
        DESCRIPTION: Verify displaying of 'Next Races' section when containing event cards are not fitting on selected screen size (more than 4 for example)
        EXPECTED: * 'Next Races' section is positioned below the In-Play section on the homepage
        EXPECTED: * Event cards are displayed within 'Next Races' section
        """
        pass

    def test_005_hover_the_mouse_over_the_next_races_section(self):
        """
        DESCRIPTION: Hover the mouse over the 'Next Races' section
        EXPECTED: Clickable Navigation right arrow appears
        """
        pass

    def test_006_click_the_right_navigation_arrow(self):
        """
        DESCRIPTION: Click the right Navigation arrow
        EXPECTED: Current visible race cards will be replaced by following next races (displaying 4 by 4 cards for example).
        """
        pass

    def test_007_click_the_left_navigation_arrow(self):
        """
        DESCRIPTION: Click the left Navigation arrow
        EXPECTED: Initially displayed race cards are shown
        """
        pass

    def test_008_repeat_steps_4_7_for_next_races_module_in_featured_section_on_the_homepage(self):
        """
        DESCRIPTION: Repeat steps 4-7 for 'Next Races' module in 'Featured' section on the homepage
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_4_7_for_enhanced_multiples_carousel_on_the_homepage(self):
        """
        DESCRIPTION: Repeat steps 4-7 for Enhanced Multiples carousel on the homepage
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_4_7_for_enhanced_multiples_carousel_on_sports_landing_pages(self):
        """
        DESCRIPTION: Repeat steps 4-7 for Enhanced Multiples carousel on Sports landing pages
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_4_7_for_enhanced_multiples_carousel_on_event_details_page_edp(self):
        """
        DESCRIPTION: Repeat steps 4-7 for Enhanced Multiples carousel on Event Details Page (EDP)
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_4_7_for_in_play_widget_on_sports_landing_pages_when_screen_size_moves_widget_into_one_column_column_2_plus_3__main_content(self):
        """
        DESCRIPTION: Repeat steps 4-7 for 'In-play' widget on Sports landing pages (when screen size moves widget into one column: Column 2 + 3 = Main content)
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_4_7_for_next_races_widget_on_races_landing_pages_when_screen_size_moves_the_widget_into_separate_third_column_column_2_and_3__main_content(self):
        """
        DESCRIPTION: Repeat steps 4-7 for 'Next Races' widget on Races landing pages (when screen size moves the widget into separate third column: Column 2 and 3 = Main content)
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_4_7_for_next_races_widget_on_races_landing_pages_when_screen_size_moves_widget_into_one_column_column_2_and_3__main_content(self):
        """
        DESCRIPTION: Repeat steps 4-7 for 'Next Races' widget on Races landing pages (when screen size moves widget into one column: Column 2 and 3 = Main content)
        EXPECTED: 
        """
        pass
