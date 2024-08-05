import pytest
import re
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import normalize_name, get_inplay_sports_by_section, get_inplay_ls_structure, get_inplay_structure
from time import sleep
from voltron.utils.exceptions.precondition_not_met_exception import PreconditionNotMetException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C28428_Verify_data_ordering_in_Live_Now_section_on_In_Play_pages(Common):
    """
    TR_ID: C28428
    NAME: Verify data ordering in  'Live Now' section on 'In-Play' pages
    DESCRIPTION: This test case verifies data ordering in  'Live Now' section on 'In-Play' pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify category/class/type ordering check received data using Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::XX::LIVE_EVENT" - where XX - Sport/Category Id
    PRECONDITIONS: ![](index.php?/attachments/get/40682)
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def verify_sport_existence(self):
        sleep(2)
        self.__class__.total_sports = []
        sports = get_inplay_ls_structure()['liveStream']['eventsBySports']
        no_of_sports = 2 if len(sports) > 2 else len(sports)
        for i in range(no_of_sports):
            self.total_sports.append(sports[i]['categoryName'].upper())

    def get_expected_inplay_sports_order(self, watchlive=True):
        if watchlive:
            inplay_module = get_inplay_ls_structure()
            inplay_data = inplay_module['liveStream']['eventsBySports']
        else:
            inplay_module = get_inplay_structure()
            inplay_data = inplay_module['livenow']['eventsBySports']
        if not inplay_data:
            raise PreconditionNotMetException("No live events available in any sport")
        inplay_sports = []  # Like Football, Baseball, Tennis etc
        # Sorting sports
        self.__class__.sport_url = inplay_data[0]['sportUri']
        for sport_segment in inplay_data:
            inplay_sports.append((sport_segment['categoryName'].upper(), sport_segment['displayOrder']))
        inplay_sports = sorted(inplay_sports, key=lambda x: x[1])
        return dict(inplay_sports)

    def get_expected_inplay_type_order(self, type, inplay_sport=False):
        self.__class__.inplay_sports_classes = {}  # Like English Premier League, English Football Cup, Greece Football Cup etc
        # Sorting classes within each sport
        inplay_module1 = get_inplay_sports_by_section(type=type)
        # for inplay_sport in inplay_module:
        self.__class__.sports_classes = inplay_module1['eventsByTypeName']
        ip_sports_classes = []
        for sport_class in self.sports_classes:
            ip_sports_classes.append((sport_class, sport_class['classDisplayOrder'], sport_class['typeDisplayOrder']))
        ip_sports_classes = sorted(ip_sports_classes, key=lambda x: (x[1], x[2]))
        sports_classes = 2 if len(ip_sports_classes) > 2 else len(ip_sports_classes)
        for item in range(sports_classes):
            if self.device_type == 'mobile':
                self.inplay_sports_classes[(ip_sports_classes[item][0]['typeName']).upper()] = ip_sports_classes[item][0]['eventsIds']
            else:
                if not inplay_sport:
                    self.inplay_sports_classes[(ip_sports_classes[item][0]['typeSectionTitleAllSports']).upper()] = ip_sports_classes[item][0]['eventsIds']
                else:
                    self.inplay_sports_classes[(ip_sports_classes[item][0]['typeSectionTitleOneSport']).upper()] = ip_sports_classes[item][0]['eventsIds']
        return self.inplay_sports_classes

    def get_expected_inplay_events_order(self, type_name):
        """
        Looks through WS response and figures out what event order is expected. Applicable for InplayModule only.
        :return: list of event names
        """
        inplay_sports_events = []  # Like England Premier League events
        # for sport_type in self.sports_classes:
        ip_sports_events = []
        for event in self.inplay_sports_classes[type_name]:
            event = self.ss_req.ss_event_to_outcome_for_event(event_id=event)[0]['event']
            if re.search(r'\d+-\d+', event['name']):
                score = re.search(r'\d+-\d+', event['name']).group()
                ip_sports_events.append(
                    (event['startTime'], event['displayOrder'], normalize_name(event['name'].replace(score, 'v'))))
            else:
                ip_sports_events.append((event['startTime'], event['displayOrder'], normalize_name(event['name'])))
        inplay_sports_events += [event[2] for event in sorted(ip_sports_events, key=lambda x: (x[0], x[1], x[2]))]
        length = 2 if len(inplay_sports_events) > 2 else len(inplay_sports_events)
        return inplay_sports_events[:length]

    def home_and_watchlive(self, watchlive=True):
        expected_sport_group = self.get_expected_inplay_sports_order(watchlive)
        actual_sport_group = []
        if self.device_type in ['mobile', 'tablet']:
            if watchlive:
                grouping_buttons = self.site.inplay.tab_content.live_now
            else:
                grouping_buttons = self.site.home.tab_content.live_now
            if not grouping_buttons:
                raise PreconditionNotMetException('"Live" events are not available in watch live tab')
            inplay_list_upcoming = list(grouping_buttons.items_as_ordered_dict.keys())
            no_of_sports = 2 if len(inplay_list_upcoming) > 2 else len(inplay_list_upcoming)
            for i in range(no_of_sports):
                actual_sport_group.append(inplay_list_upcoming[i].split('\n')[0])
                sport = list(grouping_buttons.items_as_ordered_dict.values())[i]
                if i == 1:
                    sport.click()
                sleep(3)
                if watchlive:
                    expected_sport_type = self.get_expected_inplay_type_order(type='STREAM_EVENT')
                else:
                    expected_sport_type = self.get_expected_inplay_type_order(type='LIVE_EVENT')
                actual_sport_type = [x.upper() for x in sport.items_as_ordered_dict.keys()]
                self.assertEqual(actual_sport_type[:2], list(expected_sport_type.keys())[:2], msg=f'Actual sport Types:"{actual_sport_type[:2]}" are not equal to'
                                 f'Expected sport type :"{list(expected_sport_type.keys())[:2]}"')
                # index = 0
                # item = list(sport.items_as_ordered_dict.values())[index]
                # actual_events_under_type = item.items_names[:2]
                expected_events_under_type = self.get_expected_inplay_events_order(type_name=actual_sport_type[0])
                # self.assertEqual(actual_events_under_type, expected_events_under_type, msg=f'Actual sports event list:"{actual_events_under_type}" is not equal to'
                #                                                                            f'Expected sports event list:"{expected_events_under_type}"')
                expected_events_under_type.clear()
            self.assertEqual(actual_sport_group, list(expected_sport_group.keys())[:2], msg=f'Actual sports:"{actual_sport_group}" is not equal to'
                             f'Expected sports: "{list(expected_sport_group.keys())[:2]}"')
        else:
            expected_sports = self.get_expected_inplay_sports_order()
            inplay_list_upcoming = {}
            actual_sport_type = {}
            self.verify_sport_existence()
            types = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            for type_name, type in types.items():
                if type_name in self.total_sports:
                    inplay_list_upcoming[type_name] = type.items_as_ordered_dict
                elif len(list(inplay_list_upcoming.keys())) == len(self.total_sports):
                    break
                else:
                    actual_sport_type[type_name] = type
            if watchlive:
                expected_sport_type = self.get_expected_inplay_type_order(type='STREAM_EVENT')
            else:
                expected_sport_type = self.get_expected_inplay_type_order(type='LIVE_EVENT')
            sport_type_actual = list(inplay_list_upcoming.values())[0]
            actual_types = [x.upper() for x in sport_type_actual.keys()][:2]
            self.assertEqual(actual_types, list(expected_sport_type.keys()),
                             msg=f'Expected sport type: "{actual_types}" is not in the actual sport type:"{list(expected_sport_type.keys())}"'
                                 'Events are not grouped by typeID within <Type> expanded accordions/odds headers')

            index = 0
            for item_name, item in expected_sport_type.items():
                expected_events_under_type = self.get_expected_inplay_events_order(type_name=item_name)
                actual_type = list(list(inplay_list_upcoming.values())[0].values())[index]
                actual_events_under_type = list(actual_type.items_as_ordered_dict.keys())[:2]
                self.assertEqual(actual_events_under_type, expected_events_under_type,
                                 msg=f'Expected event:"{actual_events_under_type}" is not in Actual events: "{expected_events_under_type}"'
                                     'Events are not grouped by typeID within <Type> expanded accordions/odds headers')
                index = index + 1
            expected_events_under_type.clear()
            self.assertEqual(list(inplay_list_upcoming.keys())[:2], list(expected_sports.keys())[:2], msg=f'Actual sports list:"{list(inplay_list_upcoming.keys())[:2]}" is not equal to'
                                                                                                          f'Expected sports list:"{list(expected_sports.keys())[:2]}"')

    def sport_and_inplay(self):
        if self.device_type not in ['mobile', 'tablet']:
            grouping_buttons = self.site.inplay.tab_content
            self.assertTrue(grouping_buttons,
                            msg=f'"Live" events are not available in inplay tab for sport ""')
            actual_sport_type = [x.upper().split('\n')[0] for x in grouping_buttons.accordions_list.items_as_ordered_dict.keys()]
        else:
            sleep(2)
            grouping_buttons = self.site.inplay.tab_content.live_now
            self.assertTrue(grouping_buttons, msg=f'"Live" events are not available in inplay tab for sport "')
            actual_sport_type = [x.upper().split('\n')[0] for x in grouping_buttons.items_as_ordered_dict.keys()]
        expected_sport_type = self.get_expected_inplay_type_order(type='LIVE_EVENT', inplay_sport=True)
        self.assertEqual(list(expected_sport_type.keys()), actual_sport_type[:2],
                         msg=f'Expected sport type: "{expected_sport_type}" is not in the actual sport type:"{actual_sport_type[:2]}"'
                             'Events are not grouped by typeID within <Type> expanded accordions/odds headers')
        no_of_types = 2 if len(actual_sport_type) > 2 else len(actual_sport_type)
        for i in range(no_of_types):
            if self.device_type not in ['mobile', 'tablet']:
                sport = list(grouping_buttons.accordions_list.items_as_ordered_dict.values())[i]
            else:
                sport = list(grouping_buttons.items_as_ordered_dict.values())[i]
            sleep(3)
            actual_events_under_type = sport.items_names[:2]
            expected_events_under_type = self.get_expected_inplay_events_order(type_name=actual_sport_type[i])
            self.assertEqual(expected_events_under_type, actual_events_under_type,
                             msg=f'Expected event:"{expected_events_under_type}" is not in Actual events: "{actual_events_under_type}"'
                                 'Events are not grouped by typeID within <Type> expanded accordions/odds headers')

    def test_001_verify_category_title_on_the_first_level_accordion_within_live_now_section(self):
        """
        DESCRIPTION: Verify <Category> title on the first level accordion within 'Live Now' section
        EXPECTED: 'Sport' name is displayed at the <Category> accordion within 'Live Now' section
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_premier_league_football_event(is_live=True, perform_stream=True)
            self.ob_config.add_football_event_to_england_premier_league(is_live=True, perform_stream=True)
            self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True, perform_stream=True)
            self.ob_config.add_tennis_event_to_davis_cup(is_live=True, perform_stream=True)
        self.navigate_to_page('/in-play/watchlive')
        self.site.wait_content_state_changed(timeout=30)
        self.home_and_watchlive()

    def test_002_verify_category_accordions_order(self):
        """
        DESCRIPTION: Verify <Category> accordions order
        EXPECTED: <Category> accordions are ordered by:
        EXPECTED: * Category 'displayOrder' in ascending where minus ordinals are displayed first
        """
        # covered in step 1

    def test_003_verify_type_title_on_accordionsodds_headers_within_live_now_section(self):
        """
        DESCRIPTION: Verify <Type> title on accordions/odds headers within 'Live Now' section
        EXPECTED: **Mobile/Tablet**
        EXPECTED: * 'Type' name is displayed at the <Type> accordions/odds headers
        EXPECTED: **Desktop**
        EXPECTED: * 'Type' name if the section is named Category Name + Type Name on Pre-Match pages
        EXPECTED: * 'Class' - 'Type' name if the section is named Class Name (sport name should not be displayed) + Type Name on Pre-Match pages
        """
        # covered in step 1

    def test_004_verify_type_accordionsodds_headers_order(self):
        """
        DESCRIPTION: Verify <Type> accordions/odds headers order
        EXPECTED: <Type> accordions/odds headers are ordered by:
        EXPECTED: * Class 'displayOrder' in ascending where minus ordinals are displayed first
        EXPECTED: * Type 'displayOrder' in ascending where minus ordinals are displayed first
        """
        # covered in step 1

    def test_005_verify_events_order_within_the_type_accordionsodds_headers(self):
        """
        DESCRIPTION: Verify events order within the <Type> accordions/odds headers
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * 'startTime' - chronological order in the first instance
        EXPECTED: * Event 'displayOrder' in ascending
        EXPECTED: * Alphabetical order
        """
        # covered in step 1

    def test_006_repeat_steps_1_5_on_home_page__in_play_tab_mobiletablet(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        EXPECTED:
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('/home/in-play')
            self.site.wait_content_state_changed(timeout=10)
            self.site.home.tabs_menu.click_button('IN-PLAY')
            self.site.wait_content_state_changed(timeout=10)
            self.home_and_watchlive(watchlive=False)

    def test_007_repeat_steps_3_5_on_sports_landing_page__in_play_tab_in_play_page__sport_tab_home_page_for_in_play__live_stream_section_for_both_switchers_desktop(self):
        """
        DESCRIPTION: Repeat steps 3-5 on:
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * 'In-Play' page > 'Sport' tab
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers **Desktop**
        """
        self.navigate_to_page(self.sport_url + '/live')
        self.site.wait_content_state_changed(timeout=30)
        self.sport_and_inplay()

        self.navigate_to_page(self.sport_url.replace("sport", "in-play"))
        self.site.wait_content_state_changed(timeout=30)
        self.sport_and_inplay()