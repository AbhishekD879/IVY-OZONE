import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.desktop_specific
@pytest.mark.adhoc_suite
@pytest.mark.other
@vtest
class Test_C65949634_Verify_the_in_play_module_from_header_sub_menu_in_desktop(Common):
    """
    TR_ID: C65949634
    NAME: Verify the in-play module from header sub menu in desktop.
    DESCRIPTION: This test case is to validate the in-play module from header sub menu in desktop.
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Login with valid credentials
    PRECONDITIONS: 3.Navigate to Menus - Header SubMenus - Inplay should be in enabled state.
    PRECONDITIONS: Note: inplay module should be shown to the user with or  without login.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration:
        PRECONDITIONS: 1.User should have access to oxygen CMS
        PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
        PRECONDITIONS: 2. Login with valid credentials
        PRECONDITIONS: 3.Navigate to Menus - Header SubMenus - Inplay should be in enabled state.
        PRECONDITIONS: Note: inplay module should be shown to the user with or  without login.
        """
        header_submenus = self.cms_config.get_header_submenus()
        in_play_configurations_response = next(
            (header_details for header_details in header_submenus if header_details.get('linkTitle').upper() == 'IN-PLAY'), None)
        if not in_play_configurations_response:
            raise CmsClientException('In PLay is not available')

    def test_001_launch_the__ladbrokescoral_application(self):
        """
        DESCRIPTION: launch the  Ladbrokes/Coral application.
        EXPECTED: Application should be  Launched successfully.
        """
        self.site.go_to_home_page()

    def test_002_click_on_in_play_tab_from_the_header_submenu(self):
        """
        DESCRIPTION: Click on "In-play" tab from the Header submenu.
        EXPECTED: 1.User should be navigated to the in-play page.
        EXPECTED: 2.Sports Menu Ribbon is shown with all sport categories where In-Play events are available along with 'Watch live'.
        EXPECTED: 3.First &lt;Sport&gt; tab is opened by default.
        EXPECTED: 4.Two tabs are visible: 'Live Now' and 'Upcoming'
        """
        all_sub_headers = self.site.header.sport_menu.items_as_ordered_dict
        sub_header_in_play = next((sport for sport_name, sport in all_sub_headers.items() if
                                   sport_name.upper() == 'IN-PLAY'),
                                  None)
        self.assertIsNotNone(sub_header_in_play, 'IN-PLAY is not displayed in sub header...')
        sub_header_in_play.click()
        self.assertTrue(self.site.inplay.has_inplay_sport_menu(), 'In Play Sport Menu is Not displayed!!')
        sports_on_in_play_sports_menu = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports_on_in_play_sports_menu, 'Sports Menu Items are Unavailable!!')
        watch_live_status = next((True for sport_name in sports_on_in_play_sports_menu if sport_name.upper() == "WATCH LIVE"), False)
        self.assertTrue(watch_live_status, '"WATCH LIVE" is Not Present in Sports Menu Items!!')
        tabs = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
        live_now_tab_name, self.__class__.live_now_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                                tab_name.upper() == 'LIVE NOW'),
                                               [None, None])
        self.assertIsNotNone(live_now_tab_name, '"LIVE NOW" is not present')
        upcoming_tab_name, self.__class__.upcoming_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                                tab_name.upper() == 'UPCOMING'),
                                               [None, None])
        self.assertIsNotNone(upcoming_tab_name, '"UPCOMING" is not present')


        self.live_now_tab.click()
        if self.live_now_tab.counter == 0:
            self.assertTrue(self.site.inplay.tab_content.has_no_events_label(),
                            f'Events Are Not Available But "NO EVENTS FOUND" message is Not Displayed')
        else:
            accordions_status = self.site.inplay.tab_content.accordions_list.has_items
            self.assertTrue(accordions_status, f'Accordions Are Not Found Even Events Available')

        self.upcoming_tab.click()
        if self.upcoming_tab.counter == 0:
            self.assertTrue(self.site.inplay.tab_content.has_no_events_label(),
                            f'Events Are Not Available But "NO EVENTS FOUND" message is Not Displayed')
        else:
            accordions_status = self.site.inplay.tab_content.accordions_list.has_items
            self.assertTrue(accordions_status, f'Accordions Are Not Found Even Events Available')

    def test_003_verify_live_now_and_upcoming_tabs(self):
        """
        DESCRIPTION: Verify 'Live now' and 'Upcoming' tabs.
        EXPECTED: 1.In 'Live now' tab all the events that are in in-play should be displayed.
        EXPECTED: Note:- 'There are currently no Live events available' message should be shown, if there are no live events.
        EXPECTED: 2.In 'Upcoming' tab all the vents that are about to start should be displayed according to the start time.
        """
        # covered in above step

    def test_004_click_on_any_of_the_event_under_specific_sport(self):
        """
        DESCRIPTION: Click on any of the event under specific sport.
        EXPECTED: 1.On clicking user must be navigated to the respective
        EXPECTED: Event details page.
        EXPECTED: 2.Now click on back button user must be navigated back to the in-play page.
        """
        tab = next((tab for tab in [self.live_now_tab, self.upcoming_tab] if tab.counter != 0), None)
        if tab == None:
            self.softAssert(self.assertTrue, tab, f'No One Events To Check "test_004_click_on_any_of_the_event_under_specific_sport"')
        tab.click()
        first_section_name, first_section = self.site.inplay.tab_content.accordions_list.first_item
        event_name, event = first_section.first_item
        url_before_navigating_to_edp = self.device.get_current_url()
        event.click()
        self.site.wait_content_state_changed()
        event_name_on_edp = self.site.sport_event_details.header_line.page_title.text.upper()
        self.assertEqual(event_name_on_edp, event_name.upper(),
                         f'Actual Event Detail Page : "{event_name_on_edp}" Expected Event Detail Page : "{event_name}"')
        self.site.back_button.click()
        self.site.wait_content_state_changed()
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, url_before_navigating_to_edp, f' is not navigated to previous page after clicking back button in EDP')

    def test_005_click_on_watch_live_selection(self):
        """
        DESCRIPTION: Click on 'Watch Live' selection
        EXPECTED: User must be navigated to 'Watch live' tab and all the events that have Live video streaming should be available.
        """
        self.navigate_to_page('in-play')
        sports_on_in_play_sports_menu = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        watch_live = next(
            (sport for sport_name, sport in sports_on_in_play_sports_menu.items() if sport_name.upper() == "WATCH LIVE"), False)
        watch_live.click()

    def test_006_click_on_view_all_ltsportgtinplay_events_link_undereach_sport_in_watch_live(self):
        """
        DESCRIPTION: Click on 'View all &lt;Sport&gt;inplay events' link under
        DESCRIPTION: each sport in 'Watch live'
        EXPECTED: On clicking View all inplay events link user must be
        EXPECTED: navigated to the specific sport inplay tab in same inplay page.
        """
        sports = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        for sport_name, sport in sports.items():
            sport.expand()
            if self.brand == 'ladbrokes':
                self.assertTrue(sport.has_view_all_in_play_sport_events_button(), f'"view all <Sport Name> in play events button" is not displayed for {sport_name}')
            for type_name, type in sport.items_as_ordered_dict.items():
                type.expand()
                for event_name, event in type.items_as_ordered_dict.items():
                    self.assertTrue(event.template.has_watch_live_icon(),
                                    f'watch live label is not available even though event in streaming')
