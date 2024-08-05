import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.uat
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.p2
@pytest.mark.medium
@vtest
class Test_C44870170_Verify_User_navigation_for_In_Play_tab(Common):
    """
    TR_ID: C44870170
    NAME: Verify User navigation for In-Play tab
    DESCRIPTION: User is on the
    DESCRIPTION: mobile: Homepage > In-play
    DESCRIPTION: Desktop: Homepage > In-play
    """
    keep_browser_open = True

    def test_001_load_httpsbeta_sportscoralcouk_app(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/ App
        EXPECTED: App is loaded and user is on Home page
        """
        self.site.wait_content_state('Homepage')

    def test_002_select_in_play_tab_from_home_page_menu(self, tab_name='IN-PLAY AND LIVE STREAM'):
        """
        DESCRIPTION: Select In-Play tab from Home page menu
        EXPECTED: Mobile & Tablet : In-Play page is loaded with 'Live Now' section is displayed with top 4 competitions are expanded in the list followed by other LIVE sports and 'UPCOMING' events at the bottom.
        EXPECTED: Desktop : Page is displayed with "In-play" & "Live Stream"
        EXPECTED: Events from first sport on the In-Play Carousal are listed with top 4 competitions expanded.
        """
        comp_count = []
        if self.device_type in ['mobile', 'tablet']:
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict['IN-PLAY'].click()
            sports = self.site.home.tab_content.live_now.items_as_ordered_dict
            for sport_name, sport in sports.items():
                if sport_name == list(sports)[0]:
                    self.assertTrue(sport.is_expanded(),
                                    msg=f'first sport "{sport_name}" is not expanded by default')
                    for comp_name, comp in list(sport.items_as_ordered_dict.items()):
                        if len(comp_count) < 4:
                            comp_count.append(comp)
                            self.assertTrue(comp.is_expanded(), msg=f'First 4 events under competitions "{comp_name}" are not expanded by default')
                self.assertTrue(sport.is_displayed(), msg=f'other LIVE sport "{sport}" is not displayed')
            upcoming_events = self.site.inplay.tab_content.items_as_ordered_dict
            if self.brand == 'ladbrokes':
                self.assertTrue(upcoming_events[vec.inplay.UPCOMING_EVENTS].is_displayed(),
                                msg=f'"{vec.inplay.UPCOMING_EVENTS}" are not displayed at the bottom')
            else:
                self.assertTrue(upcoming_events[vec.inplay.UPCOMING_EVENTS_SECTION].is_displayed(),
                                msg=f'"{vec.inplay.UPCOMING_EVENTS_SECTION}" are not displayed at the bottom')
        else:
            self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.items_as_ordered_dict['IN-PLAY'].click()
            sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            for sport_name, sport in sports.items():
                if sport_name == list(sports)[0]:
                    self.assertTrue(sport.is_selected(),
                                    msg=f'first sport "{sport_name}" is not expanded by default')
                    competitions = self.site.home.get_module_content(module_name=tab_name).accordions_list.items_as_ordered_dict
                    for comp_name, comp in list(competitions.items()):
                        if len(comp_count) < 4:
                            comp_count.append(comp)
                            self.assertTrue(comp.is_expanded(), msg=f'First 4 events under competition "{comp_name}" are not expanded by default')

    def test_003_on_the_in_play_tab_for_mobiletablet_click_on_see_all_sport_on_the_right_of_live_now(self):
        """
        DESCRIPTION: On the In-Play tab for Mobile/Tablet: Click on 'SEE ALL <sport>' on the right of LIVE NOW
        EXPECTED: All the live events for the corresponding sport / competition are expanded.
        """
        if self.device_type in ['mobile', 'tablet']:
            see_all = self.site.home.tab_content.live_now.live_now_header.see_all
            has_see_all_button = self.site.home.tab_content.live_now.live_now_header.has_see_all_button()
            if has_see_all_button:
                self.site.contents.scroll_to_we(see_all)
                see_all.click()
                comp_count = []
                competitions = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
                for each_competition, comp_item in competitions.items():
                    if len(comp_count) < 4:
                        comp_count.append(each_competition)
                        self.assertTrue(comp_item.is_expanded(), msg=f'competition "{each_competition}" is not expanded')
                        for each_event, event_value in comp_item.items_as_ordered_dict.items():
                            self.assertTrue(event_value.is_displayed(), msg=f'event "{each_event}" is not displayed')

    def test_004_on_the_in_play_for_desktop__click_on_each_sport_icon_from_the_carousel(self):
        """
        DESCRIPTION: On the In-play for Desktop : Click on each sport icon from the carousel.
        EXPECTED: All the live events for the corresponding sport / competition are displayed with In-play & Live stream options.
        """
        if self.device_type in ['desktop']:
            sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            for sport in sports.values():
                sport.scroll_to_we()
                sport.click()
                inplay_livestream_options = self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.items_as_ordered_dict
                for option_name, option in inplay_livestream_options.items():
                    self.assertTrue(option.is_displayed(), msg=f'Actual button: "{option_name}" is not displayed')
