import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870322_Verify_all_other_in_play_sports_tabs_and_each_tab_competition_types(Common):
    """
    TR_ID: C44870322
    NAME: Verify all other in-play sports tabs and each tab competition types
    DESCRIPTION: This test case verify inplay sports available in In-Play tab
    """
    keep_browser_open = True

    def verify_live_now_and_upcoming_tabs(self):
        if self.device_type in ['mobile', 'tablet']:
            live_now = self.site.inplay.tab_content.live_now
            upcoming = self.site.inplay.tab_content.upcoming
            self.assertTrue(live_now.is_displayed(), msg='"LIVE_NOW" is not visible')
            self.assertTrue(upcoming.is_displayed(), msg='"UPCOMING" is not visible')
        else:
            sections = list(self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.keys())
            expected_sections = [vec.Inplay.LIVE_NOW_SWITCHER, vec.Inplay.UPCOMING_SWITCHER]
            self.assertEqual(sections, expected_sections, msg=f'Actual sections: "{sections}" are not same as'
                                                              f'Expected sections: "{expected_sections}"')

    def verify_competitions_collapsible_expandable(self, tournaments):
        for section in tournaments:
            if section.is_expanded():
                section.collapse()
                self.assertFalse(section.is_expanded(), msg='section is not collapsed')
                section.expand()
                self.assertTrue(section.is_expanded(), msg='section is not expanded')
            else:
                section.expand()
                self.assertTrue(section.is_expanded(), msg='section is not expanded')
                section.collapse()
                self.assertFalse(section.is_expanded(), msg='section is not collapsed')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')

    def test_002_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'In-Play' Landing Page is opened
        EXPECTED: Sports Menu Ribbon is shown with Categories where In-Play events are available
        EXPECTED: First <Sport> tab is opened by default
        EXPECTED: Two filter switchers are visible: 'Live Now' and 'Upcoming'
        """
        if self.device_type in ['mobile', 'tablet']:
            if self.brand == 'bma':
                self.site.home.menu_carousel.click_item(vec.siteserve.IN_PLAY_TAB)
            else:
                self.site.home.menu_carousel.click_item(vec.SB.IN_PLAY)
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.siteserve.IN_PLAY_TAB]
            in_play_tab.click()
        self.site.wait_content_state(state_name='in-play')
        self.__class__.sports_categories = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(self.sports_categories.keys(), msg='Categories are not displayed')
        active_tab = list(self.sports_categories.values())[1]
        self.assertTrue(active_tab.is_selected(), msg=f'"{active_tab.name}" is not active by default')
        self.verify_live_now_and_upcoming_tabs()

    def test_003_verify_live_now__upcoming_filter_switchers_are_visible_for_all_other_in_play_sports_tab_and_each_tab_competition_types_are_expandablecollapsible(self):
        """
        DESCRIPTION: Verify 'Live Now & Upcoming' filter switchers are visible for all other In-play sports tab and each tab competition types are expandable/collapsible.
        EXPECTED: 'Live Now & Upcoming' filter switchers are visible for all other In-play sports tab and each tab competition types are expandable/collapsible.
        """
        for sport_name, sport in list(self.sports_categories.items())[1:3]:
            self.site.inplay.inplay_sport_menu.click_item(sport_name)
            self.verify_live_now_and_upcoming_tabs()
            tournaments = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values()
            if tournaments:
                self.verify_competitions_collapsible_expandable(tournaments)
            else:
                self._logger.debug('*** No events found in "Live Now" tab ***')
            if self.device_type in ['mobile', 'tablet']:
                if self.brand == 'bma':
                    upcoming_events = self.site.inplay.tab_content.items_as_ordered_dict.get(vec.Inplay.UPCOMING_EVENTS_SECTION)
                else:
                    upcoming_events = self.site.inplay.tab_content.items_as_ordered_dict.get(vec.Inplay.UPCOMING_EVENTS)
                tournaments = upcoming_events.items_as_ordered_dict.values()
            else:
                self.site.inplay.tab_content.grouping_buttons.click_button('UPCOMING')
                tournaments = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values()
            if tournaments:
                self.verify_competitions_collapsible_expandable(tournaments)
            else:
                self._logger.debug('*** No events found in "UPCOMING" tab ***')
