import pytest
import re
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import normalize_name, get_inplay_sports_by_section, get_inplay_ls_structure
from time import sleep
from voltron.utils.exceptions.precondition_not_met_exception import PreconditionNotMetException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C28429_Verify_live_events_grouping_on_In_Play_pages(Common):
    """
    TR_ID: C28429
    NAME: Verify live events grouping on 'In-Play' pages
    DESCRIPTION: This test case verifies live events grouping on 'In-Play' pages
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
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40725)
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def verify_sport_existence(self):
        sleep(2)
        self.__class__.total_sports = []
        sports = get_inplay_ls_structure()['liveStream']['eventsBySports']
        no_of_sports = 2 if len(sports) > 2 else len(sports)
        for i in range(no_of_sports):
            self.total_sports.append(sports[i]['categoryCode'])

    def verify_event_filtering(self, watchlive=True):
        if watchlive:
            inplay_module = get_inplay_sports_by_section(type='STREAM_EVENT')
        else:
            inplay_module = get_inplay_sports_by_section(type='LIVE_EVENT')
        if not inplay_module:
            raise PreconditionNotMetException('No inplay events present in any sport')
        self.__class__.inplay_sports = {}  # Like Football, Baseball, Tennis etc
        inplay_sports_classes = {}  # Like English Premier League, English Football Cup, Greece Football Cup etc

        # Sorting sports using sports ID
        # for sport_segment in inplay_data:
        self.inplay_sports[inplay_module['categoryCode']] = inplay_module['categoryId']
        self.__class__.sport_url = inplay_module['sportUri']
        self.inplay_sports = {k.replace("_", " "): v for k, v in sorted(self.inplay_sports.items(), key=lambda item: item[1])}

        # Sorting classes within each sport
        # for inplay_sport in inplay_sports:
        sports_classes = inplay_module['eventsByTypeName']
        ip_sports_classes = []
        for sport_class in sports_classes:
            ip_sports_classes.append((sport_class, sport_class['classDisplayOrder'], sport_class['typeDisplayOrder']))
        ip_sports_classes = sorted(ip_sports_classes, key=lambda x: (x[1], x[2]))
        sports_classes = 2 if len(ip_sports_classes) > 2 else len(ip_sports_classes)
        for item in range(sports_classes):
            if self.device_type == 'mobile':
                inplay_sports_classes[(ip_sports_classes[item][0]['typeName']).upper()] = ip_sports_classes[item][0]['eventsIds']
            elif self.device_type == 'desktop' and watchlive:
                inplay_sports_classes[(ip_sports_classes[item][0]['typeSectionTitleAllSports']).upper()] = ip_sports_classes[item][0]['eventsIds']
            else:
                inplay_sports_classes[(ip_sports_classes[item][0]['typeSectionTitleOneSport']).upper()] = ip_sports_classes[item][0]['eventsIds']
        return inplay_sports_classes

    def home_and_watchlive(self, watchlive=True):
        actual_sport_group = []
        if self.device_type in ['mobile', 'tablet']:
            if watchlive:
                grouping_buttons = self.site.inplay.tab_content.live_now
            else:
                grouping_buttons = self.site.home.tab_content.live_now
            self.assertTrue(grouping_buttons, msg='"Upcoming" events are not available in watch live tab')
            inplay_list_upcoming = list(grouping_buttons.items_as_ordered_dict.keys())
            no_of_sports = 2 if len(inplay_list_upcoming) > 2 else len(inplay_list_upcoming)
            for i in range(no_of_sports):
                actual_sport_group.append(inplay_list_upcoming[i])
                sport = list(grouping_buttons.items_as_ordered_dict.values())[i]
                if i == 1:
                    sport.click()
                sleep(3)
                if watchlive:
                    expected_sport_type = self.verify_event_filtering()
                else:
                    expected_sport_type = self.verify_event_filtering(watchlive=False)
                actual_sport_type = [x.upper() for x in sport.items_as_ordered_dict.keys()]
                for item in list(expected_sport_type.keys()):
                    self.assertIn(item.strip(), actual_sport_type, msg=f'Expected sport type: "{item.strip()}" is not in the '
                                                               f'actual sport type:"{actual_sport_type}"')
                index = 0
                item = list(sport.items_as_ordered_dict.values())[index]
                actual_events_under_type = item.items_names
                expected_events_under_type = []
                events_list = list(expected_sport_type.values())[index]if len(list(expected_sport_type.values())[index]) <= 1 else list(expected_sport_type.values())[index][0:2]
                for event in events_list:
                    event = self.ss_req.ss_event_to_outcome_for_event(event_id=event)[0]['event']
                    if re.search(r'\d+-\d+', event['name']):
                        score = re.search(r'\d+-\d+', event['name']).group()
                        expected_events_under_type.append(normalize_name(event['name'].replace(score, 'v')))
                    else:
                        expected_events_under_type.append(normalize_name(event['name']))
                for item in expected_events_under_type:
                    try:
                        self.assertIn(item, actual_events_under_type,
                                      msg=f'Expected event:"{item}" is not in Actual events: "{actual_events_under_type}"'
                                          'Events are not grouped by typeID within <Type> expanded accordions/odds headers')
                    except Exception:
                        continue
                expected_events_under_type.clear()
            for item in actual_sport_group:
                item_name=item.split("\n")[0]
                self.assertIn(item_name, list(self.inplay_sports.keys()), msg=f'Actual sports list:"{item_name}" is not in'
                              f'Expected sports list:"{list(self.inplay_sports.keys())}"')
        else:
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
                expected_sport_type = self.verify_event_filtering()
            else:
                expected_sport_type = self.verify_event_filtering(watchlive=False)
            sport_type_actual = list(inplay_list_upcoming.values())[0]
            actual_types = [x.upper() for x in sport_type_actual.keys()]
            for item in expected_sport_type:
                self.assertIn(item, actual_types,
                              msg=f'Expected sport type: "{item}" is not in the actual sport type:"{actual_types}"'
                                  'Events are not grouped by typeID within <Type> expanded accordions/odds headers')
            index = 0
            for item_name, item in expected_sport_type.items():
                expected_events_under_type = []
                actual_type = list(list(inplay_list_upcoming.values())[0].values())[index]
                actual_events_under_type = actual_type.items_as_ordered_dict
                events = item[0:2] if len(item) > 2 else item
                for event in events:
                    event = self.ss_req.ss_event_to_outcome_for_event(event_id=event)[0]['event']
                    if re.search(r'\d+-\d+', event['name']):
                        score = re.search(r'\d+-\d+', event['name']).group()
                        expected_events_under_type.append(normalize_name(event['name'].replace(score, 'v')))
                    else:
                        expected_events_under_type.append(normalize_name(event['name']))
                try:
                    for item in expected_events_under_type:
                        self.assertIn(item, actual_events_under_type,
                                      msg=f'Expected event:"{item}" is not in Actual events: "{actual_events_under_type}"'
                                          'Events are not grouped by typeID within <Type> expanded accordions/odds headers')
                except Exception:
                    continue
                index = index + 1
            expected_events_under_type.clear()
            for item in list(inplay_list_upcoming.keys()):
                self.assertIn(item, self.total_sports, msg=f'Actual sports list:"{item}" is not equal to'
                              f'Expected sports list:"{self.total_sports}"')

    def sport_and_inplay(self):
        if self.device_type not in ['mobile', 'tablet']:
            grouping_buttons = self.site.inplay.tab_content
            self.assertTrue(grouping_buttons,
                            msg=f'"Upcoming" events are not available in inplay tab for sport "{self.sport_url}"')
            actual_sport_type = [x.upper() for x in grouping_buttons.accordions_list.items_as_ordered_dict.keys()]
        else:
            sleep(2)
            grouping_buttons = self.site.inplay.tab_content.live_now
            self.assertTrue(grouping_buttons, msg=f'"Upcoming" events are not available in inplay tab for sport "{self.sport_url}"')
            actual_sport_type = [x.upper() for x in grouping_buttons.items_as_ordered_dict.keys()]
        expected_sport_type = self.verify_event_filtering(watchlive=False)
        actual_sport_types = []
        for i in actual_sport_type:
            actual_sport_types.append(i.split("\n")[0])
        for item in expected_sport_type:
            self.assertIn(item, actual_sport_types,
                          msg=f'Expected sport type: "{item}" is not in the actual sport type:"{actual_sport_types}"'
                              'Events are not grouped by typeID within <Type> expanded accordions/odds headers')

        no_of_types = 2 if len(actual_sport_type) > 2 else len(actual_sport_type)
        for i in range(no_of_types):
            if self.device_type not in ['mobile', 'tablet']:
                sport = list(grouping_buttons.accordions_list.items_as_ordered_dict.values())[i]
            else:
                sport = list(grouping_buttons.items_as_ordered_dict.values())[i]
            sleep(3)
            actual_events_under_type = sport.items_names
            expected_events_under_type = []
            events_list = list(expected_sport_type.values())[i] if len(list(expected_sport_type.values())[i]) <= 1 else list(expected_sport_type.values())[i][0:2]
            for event in events_list:
                event = self.ss_req.ss_event_to_outcome_for_event(event_id=event)[0]['event']
                if re.search(r'\d+-\d+', event['name']):
                    score = re.search(r'\d+-\d+', event['name']).group()
                    expected_events_under_type.append(normalize_name(event['name'].replace(score, 'v')))
                else:
                    expected_events_under_type.append(normalize_name(event['name']))
            try:
                for item in expected_events_under_type:
                    self.assertIn(item, actual_events_under_type,
                                  msg=f'Expected event:"{item}" is not in Actual events: "{actual_events_under_type}"'
                                      'Events are not grouped by typeID within <Type> expanded accordions/odds headers')
            except Exception:
                continue

    def test_001_verify_grouping_by_categories_in_live_now_section(self):
        """
        DESCRIPTION: Verify grouping by Categories in 'Live Now' section
        EXPECTED: * The <Category> accordions are displayed
        EXPECTED: * Types are grouped by 'categoryID' > 'classID' within expanded <Category> accordion
        """
        self.navigate_to_page('/in-play/watchlive')
        self.site.wait_content_state_changed(timeout=30)
        self.home_and_watchlive()

    def test_002_verify_live_events_grouping_by_types(self):
        """
        DESCRIPTION: Verify live events grouping by Types
        EXPECTED: * The <Type> accordions/odds headers are displayed
        EXPECTED: * Events are grouped by 'typeID' within <Type> expanded accordions/odds headers
        """
        # covered in step1

    def test_003_repeat_steps_1_2_on_home_page__in_play_tab_mobiletablet(self):
        """
        DESCRIPTION: Repeat steps 1-2 on:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('/home/in-play')
            self.site.wait_content_state_changed(timeout=10)
            self.site.home.tabs_menu.click_button('IN-PLAY')
            self.site.wait_content_state_changed(timeout=10)
            self.home_and_watchlive(watchlive=False)

    def test_004_repeat_step_2_on_sports_landing_page__in_play_tab_in_play_page__sport_tab_home_page_for_in_play__live_stream_section_for_both_switchers_desktop(self):
        """
        DESCRIPTION: Repeat step 2 on:
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
