import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_006_In_Play.In_Play_page.Sports_Menu_Ribbon.BaseSportsMenuRibbonTest import BaseSportsMenuRibbonTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C28409_Verify_Sport_Tabs_order_in_Sports_Menu_Ribbon_on_In_play_page(BaseSportsMenuRibbonTest):
    """
    TR_ID: C28409
    NAME: Verify Sport Tabs order in Sports Menu Ribbon on 'In-play' page
    DESCRIPTION: This test case verifies order of Sport Tabs in Sports Menu Ribbon on 'In-play' page
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Category, where X.XX - the latest OpenBet release
    PRECONDITIONS: Load Oxygen app
    """
    keep_browser_open = True

    def verify_sports_orders(self, inplay_data, inplay_module_items):
        live_sports = {}
        upcoming_sports = {}
        watch_live = []
        for sport_segment in inplay_data:
            if sport_segment['imageTitle'] == 'All Sports 2' or 'All Sports':
                # In ws imageTitle for Watch live tab = All Sports 2 or All Sports for prod
                if self.site.wait_content_state('In-Play', timeout=1, raise_exceptions=False):
                    watch_live = [vec.sb.WATCH_LIVE_LABEL]
                    continue
            elif sport_segment['hasLiveNow']:
                live_sports[sport_segment['imageTitle'].upper()] = sport_segment['displayOrder']
            else:
                upcoming_sports[sport_segment['imageTitle'].upper()] = sport_segment['displayOrder']
        live_sports = sorted(live_sports, key=live_sports.get, reverse=False)
        upcoming_sports = sorted(upcoming_sports, key=upcoming_sports.get, reverse=False)
        expected_sports_order = watch_live + live_sports + upcoming_sports
        self.assertTrue(set(expected_sports_order).issubset(inplay_module_items.keys()),
                        msg=f'Incorrect categories sorting. Actual categories '
                        f'list "{inplay_module_items.keys()}" does not match "{expected_sports_order}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
        """
        if tests.settings.backend_env == 'prod':
            pass
        else:
            start_time_upcoming = self.get_date_time_formatted_string(hours=10)
            self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, start_time=start_time_upcoming)
            self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True)
            self.ob_config.add_basketball_event_to_autotest_league(is_live=True)
            self.ob_config.add_baseball_event_to_autotest_league(is_live=True)

    def test_001_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(
            self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: *   'In-Play' page is opened
        EXPECTED: *   First <Sport> tab is opened by default (e.g. Football)
        """
        if self.device_type == 'desktop':
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='"Main Navigation" menu has no tabs at all')
            inplay_tab = menu_items['IN-PLAY']
            self.assertTrue(inplay_tab, msg='No "In-Play" tab in "Main Navigation" menu')
            inplay_tab.click()
            self.site.wait_content_state(state_name='InPlay')
            in_play_tabs = self.get_inplay_sport_menu_items()
            self.assertTrue(in_play_tabs, msg='No tabs found on "In-Play" tab found')
            expected_selected_tab_name = list(in_play_tabs)[1]
            expected_selected_tab = in_play_tabs[expected_selected_tab_name]
            self.assertTrue(expected_selected_tab.is_selected(),
                            msg=f'"{expected_selected_tab_name}" tab is not opened by default')
        else:
            self.site.open_sport(name='IN-PLAY')
            self.site.wait_content_state(state_name='InPlay')

    def test_002_verify_sport_tabs_order(self):
        """
        DESCRIPTION: Verify sport tabs order
        EXPECTED: Tabs are displayed in the following order:
        EXPECTED: *  'Watch Live' tab first
        EXPECTED: *  'Live Now' sports categories are displayed first horizontally based on the Category 'displayOrder' in ascending order
        EXPECTED: *  'Upcoming' categories are displayed after this horizontally based on the Category 'displayOrder' in ascending order
        EXPECTED: *  If the displayOrder is the same in BOTH cases then they are displayed in A-Z order.
        """
        inplay_module_items = self.get_inplay_sport_menu_items()

        self.assertTrue(inplay_module_items, msg='Can not find any module items')

        first_tab_name = list(inplay_module_items)[0]
        self.assertEqual(first_tab_name, vec.sb.WATCH_LIVE_LABEL,
                         msg=f'"{first_tab_name}" tab is first, but "{vec.sb.WATCH_LIVE_LABEL}" tab should')

        inplay_data = self.wait_for_inplay_sports_ribbon_tabs()
        self.assertTrue(inplay_data, msg='Failed to get inplay data')
        self.verify_sports_orders(inplay_data, inplay_module_items)

    def test_003_verify_selected_sport_icon(self):
        """
        DESCRIPTION: Verify selected <Sport> icon
        EXPECTED: <Sport> icon is underscored
        """
        inplay_module_items = self.get_inplay_sport_menu_items()
        expected_selected_tab_name = list(inplay_module_items)[1]
        selected_tab = inplay_module_items[expected_selected_tab_name]
        self.assertTrue(selected_tab.is_selected(), msg=f'"{expected_selected_tab_name}" icon is not underscored')

    def test_004_for_desktop_navigate_to_in_play__live_stream_section_on_homepage_and_verify_sport_tabs_order(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and verify Sport tabs order
        EXPECTED: Tabs are displayed in the following order:
        EXPECTED: * Sports categories are displayed based on the Category 'displayOrder' in ascending order
        EXPECTED: * If displayOrder is the same then they are displayed in A-Z order.
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            home_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(home_module_items, msg='Can not find any module items')

            inplay_data = self.wait_for_inplay_sports_ribbon_tabs_on_home_page()
            self.assertTrue(inplay_data, msg='Failed to get inplay module')
            self.verify_sports_orders(inplay_data, home_module_items)
