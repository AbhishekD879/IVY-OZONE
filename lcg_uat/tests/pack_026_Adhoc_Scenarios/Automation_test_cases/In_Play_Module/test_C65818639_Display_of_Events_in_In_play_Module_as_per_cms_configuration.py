import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from crlat_cms_client.utils.exceptions import CMSException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.slow
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.adhoc_suite
@pytest.mark.homepage_featured
@vtest
class Test_C65818639_Display_of_Events_in_In_play_Module_as_per_cms_configuration(Common):
    """
    TR_ID: C65818639
    NAME: Display of Events in In-play Module  as per cms configuration
    DESCRIPTION: This test case verifies events displaying in 'In-Play' module on 'Featured' tab based on CMS configs
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: 'In-Play' module should be enabled in CMS &gt; Sports Configs &gt; Structure &gt; In-Play module
    PRECONDITIONS: 'In-Play' module should be 'Active' in CMS &gt; Sports Pages &gt; Homepage &gt; In-Play module
    PRECONDITIONS: To check data received in featured-sports MS open Dev Tools &gt; Network &gt; WS &gt; featured-sports
    PRECONDITIONS: Next configurations are set up in CMS &gt; Sports Pages &gt; Homepage &gt; In Play module &gt; Add Sport &gt; Set number of events for Sport:
    PRECONDITIONS: Several Sports are added (Sport1, Sport2, Sport3, etc.)
    PRECONDITIONS: 'In Play Event Count' is set to e.g. 10
    PRECONDITIONS: Several Sports with &gt;10 live events available in OB (e.g. Football, Tennis, Horse Racing, Greyhounds etc)
    """
    keep_browser_open = True
    sport_1, sport_2, sport_3 = None, None, None
    in_play_event_number = 3

    def in_play_sports_frontend(self):
        self.navigate_to_page('/in-play')
        inplay_sport = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        sport_live = {}
        sport_count = 0
        for sport in inplay_sport:
            sport_count += 1
            if sport.upper() == "WATCH LIVE":
                continue
            self.site.inplay.inplay_sport_menu.click_item(item_name=sport)
            wait_for_haul(5)
            event_count = self.site.inplay.tab_content.live_now_counter
            if event_count >= 3:
                sport_live[sport] = event_count
            if len(sport_live) >= 3:
                break
            if sport_count >= 10:
                break
        inplay_sports = list(sport_live.keys())
        return inplay_sports

    def get_inplay_module_config(self):
        """
        This method gets "In-Play" module configuration from WS response
        :return: "inplayConfig" section
        """
        inplay_module = self.cms_config.get_sport_module(module_type='INPLAY')
        module_id = inplay_module[0].get('id')
        parameters = self.cms_config.get_sport_module_details(_id=module_id)
        return parameters['inplayConfig']

    def get_inplay_event_count(self):
        """
        This method gets "In-Play" module "maxEventCount" value from WS response
        :return: "maxEventCount" value
        """
        parameters = self.get_inplay_module_config()
        return parameters['maxEventCount']

    def get_sport_inplay_event_count(self, sport_name):
        """
        This method gets "In-Play" module "eventCount" value for specified Sport number from WS response
        :param sport_name:
        :param sport_number: numeric value starting from 0
        :return: "eventCount" value
        """
        parameters = self.get_inplay_module_config()
        sport_number = None
        all_sports = parameters['homeInplaySports']
        for index in range(len(all_sports)):
            if all_sports[index].get('sportName', "").upper() == sport_name.upper():
                sport_number = index
                break
        if sport_number is None:
            raise CMSException(f'Sport name "{sport_name}" is not available!')
        return {'inplay_event_count': parameters['homeInplaySports'][sport_number]['eventCount'], 'index': sport_number}

    def verify_changes_saved_for_sport(self, sport_name: str, event_count: int):
        """
        This method compares "eventCount" value for specified Sport number with predefined "eventCount" value
        :param sport_name:
        :param sport_number: numeric value starting from 0
        :param event_count: numeric value starting from 0
        :return: True of False
        """
        actual_event_count = self.get_sport_inplay_event_count(sport_name=sport_name).get('inplay_event_count')
        self.assertEqual(actual_event_count, event_count,
                         msg=f'Actual number of sport events: {actual_event_count} '
                             f'is not as expected: {event_count}')

    def verify_number_of_displayed_events_for_sport(self, sport_name: str, event_count: int, display=True):
        """
        This method compares number of events in specified Sport name with predefined "eventCount" value
        :param display:
        :param sport_name: name of sport
        :param event_count: numeric value starting from 0
        :return:
        """
        wait_for_haul(5)
        self.device.refresh_page()
        in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='"In-Play" module has no live events')
        if display:
            sport_name_key = next(
                (sportName for sportName in in_play_event_groups if sport_name.upper() == sportName.upper()), None)
            self.assertIsNotNone(sport_name_key, f'Sport Name : {sport_name} is not found in inplay module')
            sport_name = sport_name_key
            if event_count > 0:
                wait_for_haul(5)
                self.device.refresh_page()
                self.site.home.tab_content.in_play_module.scroll_to()
                in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
                sport_events = in_play_event_groups[sport_name].items_as_ordered_dict
                self.assertTrue(sport_events, msg=f'Sport: "{sport_name}" has no live events')
                for i in range(4):
                    self.site.home.tab_content.in_play_module.scroll_to()
                    in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
                    sport_events = in_play_event_groups[sport_name].items_as_ordered_dict
                    self.assertTrue(sport_events, msg=f'Sport: "{sport_name}" has no live events')
                    if len(sport_events) != event_count:
                        # events are taking time to reflect
                        self.device.refresh_page()
                        wait_for_haul(10)
                self.assertEqual(len(sport_events), event_count,
                                 msg=f'Actual number of events: {len(sport_events)} for "{sport_name}" '
                                     f'is not as expected: {event_count}')
            else:
                self.assertNotIn(sport_name, list(in_play_event_groups.keys()),
                                 msg=f'"{sport_name}" group should not displayed')
        else:
            list_of_inplay_sports = []
            for in_play_event_group in in_play_event_groups:
                list_of_inplay_sports.append(in_play_event_group.upper())
            self.assertNotIn(sport_name.upper, list_of_inplay_sports,
                             msg=f'{sport_name} sport is displayed in front end')

    @classmethod
    def custom_tearDown(cls):
        """
        DESCRIPTION: Revert CMS values to initial values
        """
        cms_config = cls.get_cms_config()
        cms_config.update_inplay_event_count(event_count=cls.in_play_event_count)
        cms_config.update_inplay_sport_event_count(sport_number=cls.sport_1_before.get('index'),
                                                   event_count=cls.sport_1_before.get('inplay_event_count'))
        cms_config.update_inplay_sport_event_count(sport_number=cls.sport_2_before.get('index'),
                                                   event_count=cls.sport_2_before.get('inplay_event_count'))
        cms_config.update_inplay_sport_event_count(sport_number=cls.sport_3_before.get('index'),
                                                   event_count=cls.sport_3_before.get('inplay_event_count'))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Oxygen app & Set up 'In-Play' module with live events
        EXPECTED: 1. The homepage is opened and 'Featured' tab is selected
        EXPECTED: 2. 'In-Play' module with live events is displayed in 'Featured' tab
        """
        self.__class__.inplay_sports = None
        if self.cms_config.get_sport_module(module_type='INPLAY')[0]['disabled']:
            raise CMSException('"Inplay Module" module is disabled on Homepage')

        # check "In-Play" module enabled in CMS and load App
        inplay_module = self.get_initial_data_system_configuration().get('Inplay Module', {})
        if not inplay_module:
            inplay_module = self.cms_config.get_system_configuration_item('Inplay Module')
        if not inplay_module.get('enabled'):
            raise CMSException('"In-Play" module is disabled in CMS')

        # get sports from CMS
        inplay_module_data = self.cms_config.get_inplay_module_items(segment_name='Universal')
        self.__class__.cms_inplay_sports = list(
            map(lambda sport_name: sport_name["sportName"].upper(),
                inplay_module_data))
        self.site.wait_content_state(state_name='HomePage', timeout=5)

        if tests.settings.backend_env != 'prod':
            # Create test events for Sport 1, Sport 2, Sport 3
            for i in range(0, 3):
                self.ob_config.add_autotest_premier_league_football_event(is_live=True)
                self.ob_config.add_handball_event_to_croatian_premijer_liga(is_live=True)
                self.ob_config.add_baseball_event_to_autotest_league(is_live=True)
            self.inplay_sports = ["football", "handball", "baseball"]

        if tests.settings.backend_env == 'prod':
            self.inplay_sports = self.in_play_sports_frontend()
            self.assertTrue(self.inplay_sports, msg="No Sport having 3 inplay events")
            if len(self.inplay_sports) < 3:
                raise SiteServeException(
                    f"no of live events for the sports is not enough for the test required sport count is 3 available "
                    f"sport count is {len(self.inplay_sports)}")
            for sport in self.inplay_sports:
                if sport.upper() not in self.cms_inplay_sports:
                    raise CMSException(
                        f'expected  item "{sport}" not found in cms configured items {self.cms_inplay_sports}')

            # The cms configuration is reflecting if we done it through code once resolved can use it

            # sport_to_create_beta = [] for sport in self.inplay_sports: if sport.upper() not in sport_names:
            # sport_to_create_beta.append(sport) for sport_name in sport_to_create_beta: if sport_name.upper() ==
            # "BASKETBALL" or sport_name.upper() == "FOOTBALL" or sport_name.upper() == "TENNIS": tier = "TIER_1"
            # else: tier = "TIER_2" self.cms_config.create_inplay_sport_module(sport_name="Baseball", tier=tier,
            # categoryid= self.ob_config.baseball_config.category_id)
        # else: self.__class__.inplay_sports = ["football", "handball", "baseball"] sport_to_create_lower_env = []
        # for sport_name in self.inplay_sports: if sport_name.upper() not in sport_names:
        # sport_to_create_lower_env.append(sport_name) for sport_name in sport_to_create_lower_env: if
        # sport_name.upper() == "BASKETBALL" or sport_name.upper() == "FOOTBALL" or sport_name.upper() == "TENNIS":
        # tier = "TIER_1" else: tier = "TIER_2" self.cms_config.create_inplay_sport_module(sport_name=sport_name,
        # tier=tier)

        # Setting sports order in CMS
        drag_panel_ids = []
        for title in self.inplay_sports:
            for item in inplay_module_data:
                if item['sportName'].upper() == title.upper():
                    drag_panel_ids.append(item['id'])
                    break
            else:
                raise CMSException(f'expected  sport "{title}" not found')

        order = [item['id'] for item in inplay_module_data]
        i = 0
        for drag_panel_id in drag_panel_ids:
            order.remove(drag_panel_id)
            order.insert(i, drag_panel_id)
            self.cms_config.change_order_of_home_inpaly_module_items(new_order=order, moving_item=drag_panel_id)
            i += 1

        # Taking starting event count from CMS
        self.__class__.in_play_event_count = self.get_inplay_event_count()
        self.__class__.sport_1_before = self.get_sport_inplay_event_count(sport_name=self.inplay_sports[0])
        self.__class__.sport_2_before = self.get_sport_inplay_event_count(sport_name=self.inplay_sports[1])
        self.__class__.sport_3_before = self.get_sport_inplay_event_count(sport_name=self.inplay_sports[2])
        self.navigate_to_page('/')
        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab, home_featured_tab_name,
                         msg=f'Current tab: "{current_tab}", is not as expected: "{home_featured_tab_name}"')

        # home page in play widget data
        in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='"In-Play" module has no live events')

        # Get Sport 1, Sport 2, Sport 3 from CMS
        for item in range(0, 3):
            self.cms_config.update_inplay_sport_module(sport_name=self.inplay_sports[item], event_count=1)
            self.verify_changes_saved_for_sport(sport_name=self.inplay_sports[item], event_count=1)
        self.__class__.sport_1, self.__class__.sport_2, self.__class__.sport_3 = \
            self.inplay_sports[0], self.inplay_sports[1], self.inplay_sports[2]
        # to reflect the cms changes
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        # Set 'In Play Event Count' to 3
        self.cms_config.update_inplay_event_count(event_count=self.in_play_event_number)
        # validating the changes done in cms
        self.assertEqual(self.get_inplay_event_count(), self.in_play_event_number,
                         msg=f'Actual "In-Play" event count: {self.get_inplay_event_count()} 'f'is not as expected: {self.in_play_event_number}')

    def test_001_in_cms_ampgt_sports_pages_ampgt_homepage_ampgt_in_play_moduleset_sport_1__eg_10_and_save_changes(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set Sport 1 = e.g. 10 and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        # updating sport event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_1, event_count=self.in_play_event_number)
        self.verify_changes_saved_for_sport(sport_name=self.sport_1, event_count=self.in_play_event_number)

    def test_002_verify_event_displaying_in_in_play_module(self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module
        EXPECTED: 10 events are displayed for Sport 1
        EXPECTED: '10' value is taken from CMS (step 1 -&amp;gt; value set for Sport 1)
        """
        number_of_events = self.get_sport_inplay_event_count(sport_name=self.sport_1).get('inplay_event_count')
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=number_of_events)

    def test_003_in_cms_ampgt_sports_pages_ampgt_homepage_ampgt_in_play_moduleset_sport_1__eg_15_higher_value_than_in_in_play_event_count_and_save_changes(
            self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set Sport 1 = e.g. 15 (higher value than in 'In-Play Event Count') and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        # updating sport event count more than total event count
        max_number_of_inplay_events = self.get_inplay_event_count() + 1
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_1, event_count=max_number_of_inplay_events)
        self.verify_changes_saved_for_sport(sport_name=self.sport_1, event_count=max_number_of_inplay_events)

    def test_004_verify_event_displaying_in_in_play_module(self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module
        EXPECTED: 10 events are displayed for Sport 1
        EXPECTED: '10' value is taken from CMS (step 1 -&amp;gt; value set for 'In-Play Event Count' &amp;lt; Sport 1)
        """
        # This step is covered in step 2

    def test_005_in_cms_ampgt_sports_pages_ampgt_homepage_ampgt_in_play_modulesetsport_1__eg_6sport_2__eg_2sport_3__eg_2sport_4__eg_2and_save_changes(
            self):
        """
        DESCRIPTION: In CMS &amp;gt; Sports Pages &amp;gt; Homepage &amp;gt; 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: Sport 1 = e.g. 6
        DESCRIPTION: Sport 2 = e.g. 2
        DESCRIPTION: Sport 3 = e.g. 2
        DESCRIPTION: Sport 4 = e.g. 2
        DESCRIPTION: and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        # for sport1
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_1, event_count=2)
        self.verify_changes_saved_for_sport(sport_name=self.sport_1, event_count=2)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=2)

        # for sport2
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_2, event_count=1)
        self.verify_changes_saved_for_sport(sport_name=self.sport_2, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_2, event_count=1)

        # for sport3
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_3, event_count=1)
        self.verify_changes_saved_for_sport(sport_name=self.sport_3, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_3, event_count=1, display=False)

    def test_006_verify_event_displaying_in_in_play_module_if_we_receive_the_next_number_of_events_per_sport_from_obsport_1__6sport_2__2sport_3__2sport_4__2(
            self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module if we receive the next number of events per Sport from OB:
        DESCRIPTION: Sport 1 = 6
        DESCRIPTION: Sport 2 = 2
        DESCRIPTION: Sport 3 = 2
        DESCRIPTION: Sport 4 = 2
        EXPECTED: General number of events that are displaying on 'In-Play' module is 10 according to the value taken in CMS (step 1 &amp;gt; value set for 'In-Play Event Count')
        EXPECTED: 6 events are displayed for Sport 1
        EXPECTED: 2 events are displayed for Sport 2
        EXPECTED: 2 events are displayed for Sport 3
        EXPECTED: 0 events are displayed for Sport 4 (because the Sum of values set for Sport 1 + Sport 2 + Sport 3 = 'In-Play Event Count')
        """
        # This step is covered in step 5

    def test_007_in_cms_ampgt_sports_pages_ampgt_homepage_ampgt_in_play_modulesetsport_1__eg_2sport_2__eg_2sport_3__eg_2sport_4__eg_8and_save_changes(
            self):
        """
        DESCRIPTION: In CMS &amp;gt; Sports Pages &amp;gt; Homepage &amp;gt; 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: Sport 1 = e.g. 2
        DESCRIPTION: Sport 2 = e.g. 2
        DESCRIPTION: Sport 3 = e.g. 2
        DESCRIPTION: Sport 4 = e.g. 8
        DESCRIPTION: and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        # updating sport1 event count
        self.cms_config.update_inplay_event_count(event_count=4)
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_1, event_count=1)
        self.verify_changes_saved_for_sport(sport_name=self.sport_1, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=1)

        # updating sport2 event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_2, event_count=1)
        self.verify_changes_saved_for_sport(sport_name=self.sport_2, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_2, event_count=1)

        # updating sport event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_3, event_count=2)
        self.verify_changes_saved_for_sport(sport_name=self.sport_3, event_count=2)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_3, event_count=2)

    def test_008_verify_event_displaying_in_in_play_module_if_we_receive_the_next_number_of_events_per_sport_from_obsport_1__2sport_2__2sport_3__2sport_4__8(
            self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module if we receive the next number of events per Sport from OB:
        DESCRIPTION: Sport 1 = 2
        DESCRIPTION: Sport 2 = 2
        DESCRIPTION: Sport 3 = 2
        DESCRIPTION: Sport 4 = 8
        EXPECTED: General number of events that are displaying on 'In-Play' module is 10 according to the value taken in CMS (step 1 &amp;gt; value set for 'In-Play Event Count')
        EXPECTED: 2 events are displayed for Sport 1
        EXPECTED: 2 events are displayed for Sport 2
        EXPECTED: 2 events are displayed for Sport 3
        EXPECTED: 4 events are displayed for Sport 4 (because the Sum of values set fo Sport 1 + Sport 2 + Sport 3 + Sport 4 =  'In-Play Event Count')
        """
        # updating sport1 event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_1, event_count=2)
        self.verify_changes_saved_for_sport(sport_name=self.sport_1, event_count=2)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=2)

        # updating sport2 event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_2, event_count=1)
        self.verify_changes_saved_for_sport(sport_name=self.sport_2, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_2, event_count=1)

        # updating sport3 event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_3, event_count=1)
        self.verify_changes_saved_for_sport(sport_name=self.sport_3, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_3, event_count=1)

    def test_009_in_cms_ampgt_sports_pages_ampgt_homepage_ampgt_in_play_modulesetsport_1__eg_6sport_2__eg_0sport_3__eg_1sport_4__eg_1and_save_changes(
            self):
        """
        DESCRIPTION: In CMS &amp;gt; Sports Pages &amp;gt; Homepage &amp;gt; 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: Sport 1 = e.g. 6
        DESCRIPTION: Sport 2 = e.g. 0
        DESCRIPTION: Sport 3 = e.g. 1
        DESCRIPTION: Sport 4 = e.g. 1
        DESCRIPTION: and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        # updating sport1 event count
        self.cms_config.update_inplay_event_count(event_count=9)
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_1, event_count=3)
        self.verify_changes_saved_for_sport(sport_name=self.sport_1, event_count=3)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=3)

        # updating sport2 event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_2, event_count=3)
        self.verify_changes_saved_for_sport(sport_name=self.sport_2, event_count=3)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_2, event_count=3)

        # updating sport3 event count
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_3, event_count=3)
        self.verify_changes_saved_for_sport(sport_name=self.sport_3, event_count=3)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_3, event_count=3)

    def test_010_verify_event_displaying_in_in_play_module_if_we_receive_the_next_number_of_events_per_sport_from_obsport_1__6sport_2__0sport_3__1sport_4__1(
            self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module if we receive the next number of events per Sport from OB:
        DESCRIPTION: Sport 1 = 6
        DESCRIPTION: Sport 2 = 0
        DESCRIPTION: Sport 3 = 1
        DESCRIPTION: Sport 4 = 1
        EXPECTED: General number of events that are displaying on 'In-Play' module is 10 according to the value taken in CMS (step 1 &amp;gt; value set for 'In-Play Event Count')
        EXPECTED: 6 events are displayed for Sport 1
        EXPECTED: 0 events are displayed for Sport 2 but Sport 3 with 1 event is displayed instead as the next Sport by display order with available live events
        EXPECTED: 1 event is displayed for Sport 4 that replaces Sport 3
        EXPECTED: 1 event is displayed for Sport 5 that replaces Sport 4 (because the Sum of values set fo Sport 1 + Sport 3 + Sport 4 + Sport 5 = 'In-Play Event Count')
        """
        # This step is covered in step 9
