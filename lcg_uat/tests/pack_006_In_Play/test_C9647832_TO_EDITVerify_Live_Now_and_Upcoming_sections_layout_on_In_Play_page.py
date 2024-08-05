import pytest
from tests.base_test import vtest
from tests.pack_006_In_Play.In_Play_page.Sports_Menu_Ribbon.BaseSportsMenuRibbonTest import BaseSportsMenuRibbonTest
from voltron.environments import constants as vec
from voltron.utils.helpers import get_inplay_sports_ribbon
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.reg167_fix
@vtest
class Test_C9647832_TO_EDITVerify_Live_Now_and_Upcoming_sections_layout_on_In_Play_page(BaseSportsMenuRibbonTest):
    """
    TR_ID: C9647832
    NAME: [TO EDIT]Verify 'Live Now' and 'Upcoming' sections layout on 'In-Play' page
    DESCRIPTION: This test case verifiesÊ'Live Now' and 'Upcoming' sections layout on 'In-Play' page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    """
    keep_browser_open = True
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER
    upcoming_switcher = vec.inplay.UPCOMING_SWITCHER

    def get_counter(self, section_name):
        """
        :param section_name: section/switcher name
        :return: counter: counter with total number of in-play events for specific sport
        """
        if self.device_type != 'desktop':
            if section_name == self.live_now_switcher:
                has_counter = self.site.inplay.tab_content.has_live_now_counter()
                counter = self.site.inplay.tab_content.live_now_counter
            else:
                has_counter = self.site.inplay.tab_content.has_upcoming_counter()
                counter = self.site.inplay.tab_content.upcoming_counter
        else:
            switcher_tab = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict[section_name]
            has_counter = switcher_tab.has_counter()
            counter = switcher_tab.counter
        if counter != 0:
            self.assertTrue(has_counter, msg='Counter with total number of in-play events is not displayed')
        return counter

    def verify_type_accordions(self, inplay_data, inplay_module_items):
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
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='Homepage')
        if self.device_type == 'mobile':
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

    def test_001_verify_live_now_section_layout_on_in_play_page(self):
        """
        DESCRIPTION: Verify 'Live Now' section layout on 'In-Play' page
        EXPECTED: 'Live Now' section consists of the next items:
        EXPECTED: * 'LIVE NOW' (XX) - a title with the number of available live events
        EXPECTED: * 'Type' accordions
        EXPECTED: * Fixture Header
        EXPECTED: * Event Card
        EXPECTED: * 'UPCOMING' (XX) - a title with the number of available upcoming events
        """
        sports_categories = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports_categories.keys(), msg='Categories are not displayed')
        active_tab = list(sports_categories.values())[1]
        self.assertTrue(active_tab.is_selected(), msg=f'"{active_tab.name}" is not active by default')
        if self.device_type == 'mobile':
            live_now = self.site.inplay.tab_content.live_now
            upcoming = self.site.inplay.tab_content.upcoming
            self.assertTrue(live_now.is_displayed(), msg='"LIVE_NOW" is not visible')
            self.assertTrue(upcoming.is_displayed(), msg='"UPCOMING" is not visible')
        else:
            sections = list(self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.keys())
            expected_sections = [self.live_now_switcher, self.upcoming_switcher]
            self.assertEqual(sections, expected_sections, msg=f'Actual sections: "{sections}" are not same as'
                                                              f'Expected sections: "{expected_sections}"')

        counter = self.get_counter(self.live_now_switcher)
        wait_for_result(lambda: get_inplay_sports_ribbon() is not {}, name="waiting for web socket connection",
                        timeout=5)
        parameters = get_inplay_sports_ribbon()
        ws_counter = parameters[0]['liveEventCount']
        if self.device_type=='desktop':
            self.softAssert(self.assertEqual, counter, ws_counter,
                            msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                                f'**liveStreamEventCount** attribute in WS')

        counter = self.get_counter(self.upcoming_switcher)
        parameters = get_inplay_sports_ribbon()
        ws_counter = parameters[0]['upcomingEventCount']
        self.softAssert(self.assertEqual, counter, ws_counter,
                        msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                            f'**upcomingLiveStreamEventCount** attribute in WS')

        if self.device_type == 'mobile':
            sections = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Type accordians are not available')

        self.__class__.section_name, self.__class__.section = list(sections.items())[0]
        if self.section_name is not None:
            if not self.section.is_expanded():
                self.section.expand()
            events = self.section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No event cards available on "{self.section_name}"')

        # Fixture Header are covered in Step# 5

    def test_002_verify_type_accordions_within_the_live_now_section(self):
        """
        DESCRIPTION: Verify 'Type' accordions within the 'Live Now' section
        EXPECTED: * 'Type' accordions contains 'Type' name, 'Cash Out' label and 'See All' link with chevron
        EXPECTED: * The number of expanded accordions is set in CMS
        """
        inplay_module_items = self.get_inplay_sport_menu_items()
        self.assertTrue(inplay_module_items, msg='Can not find any module items')

        inplay_data = self.wait_for_inplay_sports_ribbon_tabs()
        self.assertTrue(inplay_data, msg='Failed to get inplay data')
        self.verify_type_accordions(inplay_data, inplay_module_items)

        if self.device_type == 'mobile':
            sections = self.site.inplay.tab_content.live_now.items_as_ordered_dict
            section_name, section=list(sections.items())[0]
            self.assertTrue(section.group_header.has_see_all_link(), msg='No "See All" link')

    def test_003_verify_cash_out_label_displaying(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label displaying
        EXPECTED: 'CASH OUT' label is shown next to Type name if at least one of the event has cashoutAvail="Y)
        """
        if self.device_type == 'mobile':
            sections = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Type accordians are not available')

        section_name, section = list(sections.items())[0]
        if section.group_header.icons_count > 1:
            self.assertTrue(section.group_header.has_cash_out_mark(),
                            msg=f'League section "{section.group_header.title_text}" has no cash out icon')

    def test_004_verify_type_accordions_order(self):
        """
        DESCRIPTION: Verify 'Type' accordions order
        EXPECTED: Type accordions are ordered by:
        EXPECTED: 1.  Class 'displayOrder' in ascending where minus ordinals are displayed first;
        EXPECTED: 2.  Type 'displayOrder' in ascending
        """
        # Covered in Step# 2

    def test_005_verify_fixture_header_displaying(self):
        """
        DESCRIPTION: Verify Fixture Header displaying
        EXPECTED: 'Home'/'Draw'/'Away' or 1'/'2' options are displayed and aligned by the right side
        """
        if self.device_type == 'mobile':
            sections = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Type accordians are not available')
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        for sport_name, sport in sports.items():
            if sport.is_selected():
                selected_sport = sport_name

        section_name, section = list(sections.items())[0]
        Live_sports = ["TENNIS", "CRICKET", "TABLE TENNIS", "VOLLEYBALL"]

        if selected_sport.upper() == "FOOTBALL":
            self.assertEqual(section.fixture_header.header1, vec.sb.HOME,
                             msg=f'Actual fixture header "{section.fixture_header.header1}" does not '
                                 f'equal  expected "{vec.sb.HOME}"')
            self.assertEqual(section.fixture_header.header2, vec.sb.DRAW,
                             msg=f'Actual fixture header "{section.fixture_header.header2}" does not '
                                 f'equal  expected "{vec.sb.DRAW}"')
            self.assertEqual(section.fixture_header.header3, vec.sb.AWAY,
                             msg=f'Actual fixture header "{section.fixture_header.header3}" does not '
                                 f'equal  expected "{vec.sb.AWAY}"')
        elif selected_sport.upper() in Live_sports:
            self.assertEqual(section.fixture_header.header1, "1",
                             msg=f'Actual fixture header "{section.fixture_header.header1}" does not '
                                 f'equal  expected "1"')
            self.assertEqual(section.fixture_header.header3, "2",
                             msg=f'Actual fixture header "{section.fixture_header.header3}" does not '
                                 f'equal  expected "2"')
