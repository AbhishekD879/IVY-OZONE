import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cms
@pytest.mark.in_play
@pytest.mark.mobile_only
@pytest.mark.featured
@vtest
class Test_C9215152_Displaying_of_events_in_In_Play_module_on_Featured_tab_based_on_CMS_configs(BaseSportTest):
    """
    TR_ID: C9215152
    VOL_ID: C11244389
    NAME: Displaying of events in 'In-Play' module on 'Featured' tab based on CMS configs
    DESCRIPTION: This test case verifies events displaying in 'In-Play' module on 'Featured' tab based on CMS configs
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    PRECONDITIONS: - Next configurations are set up in CMS > Sports Pages > Homepage > In Play module > Add Sport > Set number of events for Sport:
    PRECONDITIONS: * Several Sports are added (Sport1, Sport2, Sport3, etc.)
    PRECONDITIONS: * 'In Play Event Count' is set to custom value
    PRECONDITIONS: * Several Sports with not less than 1 live event available in OB (e.g. Football, 'Basketball', 'Baseball' etc.)
    """
    keep_browser_open = True
    sport_1, sport_2, sport_3 = None, None, None
    in_play_event_number = 3
    in_play_sports = []

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

    def get_sport_event_count(self, sport_number: int):
        """
        This method gets "In-Play" module "eventCount" value for specified Sport number from WS response
        :param sport_number: numeric value starting from 0
        :return: "eventCount" value
        """
        if sport_number > 0:
            sport_number -= 1
        parameters = self.get_inplay_module_config()
        return parameters['homeInplaySports'][sport_number]['eventCount']

    def verify_changes_saved_for_sport(self, sport_number: int, event_count: int):
        """
        This method compares "eventCount" value for specified Sport number with predefined "eventCount" value
        :param sport_number: numeric value starting from 0
        :param event_count: numeric value starting from 0
        :return: True of False
        """
        actual_event_count = self.get_sport_event_count(sport_number=sport_number)
        self.assertEqual(actual_event_count, event_count,
                         msg=f'Actual number of sport events: {actual_event_count} '
                         f'is not as expected: {event_count}')

    def verify_number_of_displayed_events_for_sport(self, sport_name: str, event_count: int):
        """
        This method compares number of events in specified Sport name with predefined "eventCount" value
        :param sport_name: name of sport
        :param event_count: numeric value starting from 0
        :return:
        """
        in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='"In-Play" module has no live events')

        if event_count > 0:
            sport_events = in_play_event_groups[sport_name].items_as_ordered_dict
            self.assertTrue(sport_events, msg=f'Sport: "{sport_name}" has no live events')
            self.assertEqual(len(sport_events), event_count,
                             msg=f'Actual number of events: {len(sport_events)} for "{sport_name}" '
                             f'is not as expected: {event_count}')
        else:
            self.assertNotIn(sport_name, in_play_event_groups.keys(),
                             msg=f'"{sport_name}" group should not displayed')

    def get_event_count_update_from_ws(self, sport_name: str):
        """
        This method gets "eventCount" value for specified sport from WS response
        :param sport_name: name of sport
        :return: "eventCount" value
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.brand == 'ladbrokes':
            sport_name = sport_name.title()

        in_play_module_data = get_in_play_module_from_ws().get('data')
        self.assertTrue(in_play_module_data, msg='Failed to get "In-Play" module response')

        for entry in in_play_module_data:
            if entry['categoryName'] == sport_name:
                return entry['eventCount']

    def verify_update_on_featured_module_for_sport(self, sport_name: str, event_count: int):
        """
        This method waits for WS response with "eventCount" value and compares it with predefined "eventCount" value
        :param sport_name: name of sport
        :param event_count: numeric value starting from 0
        :return: True or False
        """
        result = wait_for_result(lambda: self.get_event_count_update_from_ws(sport_name=sport_name) == event_count,
                                 poll_interval=5, timeout=15,
                                 name='Waiting for event counter update in WS')
        self.assertTrue(result, msg=f'No response received for sport: {sport_name}')

    @classmethod
    def custom_tearDown(cls):
        """
        DESCRIPTION: Revert CMS values to initial values
        """
        cms_config = cls.get_cms_config()
        cms_config.update_inplay_event_count(event_count=cls.in_play_event_count)
        cms_config.update_inplay_sport_event_count(sport_number=1, event_count=cls.sport_1_event_count)
        cms_config.update_inplay_sport_event_count(sport_number=2, event_count=cls.sport_2_event_count)
        cms_config.update_inplay_sport_event_count(sport_number=3, event_count=cls.sport_3_event_count)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Oxygen app & Set up 'In-Play' module with live events
        EXPECTED: 1. The homepage is opened and 'Featured' tab is selected
        EXPECTED: 2. 'In-Play' module with live events is displayed in 'Featured' tab
        """

        if self.cms_config.get_sport_module(module_type='INPLAY')[0]['disabled']:
            raise CmsClientException('"Inplay Module" module is disabled on Homepage')

        # Taking starting values from CMS
        self.__class__.in_play_event_count = self.get_inplay_event_count()
        self.__class__.sport_1_event_count = self.get_sport_event_count(sport_number=1)
        self.__class__.sport_2_event_count = self.get_sport_event_count(sport_number=2)
        self.__class__.sport_3_event_count = self.get_sport_event_count(sport_number=3)

        # Create test events for Sport 1, Sport 2, Sport 3
        for i in range(0, 3):
            self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        for i in range(0, 2):
            self.ob_config.add_handball_event_to_croatian_premijer_liga(is_live=True)
        self.ob_config.add_baseball_event_to_autotest_league(is_live=True)
        self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True)

        # check "In-Play" module enabled in CMS and load App
        inplay_module = self.get_initial_data_system_configuration().get('Inplay Module', {})
        if not inplay_module:
            inplay_module = self.cms_config.get_system_configuration_item('Inplay Module')
        if not inplay_module.get('enabled'):
            raise CmsClientException('"In-Play" module is disabled in CMS')

        self.site.wait_content_state(state_name='HomePage', timeout=5)

        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab, home_featured_tab_name,
                         msg=f'Current tab: "{current_tab}", is not as expected: "{home_featured_tab_name}"')

        in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='"In-Play" module has no live events')

        # Get Sport 1, Sport 2, Sport 3 from CMS
        for item in range(1, 4):
            self.cms_config.update_inplay_sport_event_count(sport_number=item, event_count=1)
            self.verify_changes_saved_for_sport(sport_number=item, event_count=1)

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        in_play_module_data = get_in_play_module_from_ws()['data']
        self.assertTrue(in_play_module_data, msg='Failed to get "In-Play" module response')

        for entry in in_play_module_data:
            self.in_play_sports.append(entry['categoryName'])
        self.assertTrue(self.in_play_sports, msg='Can not find any module items')

        if not self.brand == 'ladbrokes':
            self.__class__.sport_1, self.__class__.sport_2, self.__class__.sport_3 = \
                self.in_play_sports[0], self.in_play_sports[1], self.in_play_sports[2]
        else:
            self.__class__.sport_1, self.__class__.sport_2, self.__class__.sport_3 = \
                self.in_play_sports[0].upper(), self.in_play_sports[1].upper(), self.in_play_sports[2].upper()

        # Set 'In Play Event Count' to 3
        self.cms_config.update_inplay_event_count(event_count=self.in_play_event_number)
        self.assertEqual(self.get_inplay_event_count(), self.in_play_event_number,
                         msg=f'Actual "In-Play" event count: {self.get_inplay_event_count()} '
                         f'is not as expected: {self.in_play_event_number}')

    def test_001_in_cms_set_sport_1_to_in_play_event_count_and_save_changes(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set Sport 1 to the same value as in 'In-Play Event Count' and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        self.cms_config.update_inplay_sport_event_count(sport_number=1, event_count=self.in_play_event_number)
        self.verify_changes_saved_for_sport(sport_number=1, event_count=self.in_play_event_number)

    def test_002_verify_event_displaying_in_in_play_module(self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module
        EXPECTED: * 3 events are displayed for Sport 1
        EXPECTED: * '3' value is taken from CMS (step 1 -> value set for Sport 1)
        """
        number_of_events = self.get_sport_event_count(sport_number=1)

        self.verify_update_on_featured_module_for_sport(sport_name=self.sport_1, event_count=number_of_events)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=number_of_events)

    def test_003_in_cms_set_sport_1_to_higher_value_and_save_changes(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set Sport 1 to higher value than in 'In-Play Event Count' and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        number_of_events = self.get_inplay_event_count() + 1

        self.cms_config.update_inplay_sport_event_count(sport_number=1, event_count=number_of_events)
        self.verify_changes_saved_for_sport(sport_number=1, event_count=number_of_events)

    def test_004_verify_event_displaying_in_in_play_module(self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module
        EXPECTED: * 3 events are displayed for Sport 1
        EXPECTED: * '3' value is taken from CMS
        """
        number_of_events = self.get_inplay_event_count()

        self.verify_update_on_featured_module_for_sport(sport_name=self.sport_1, event_count=number_of_events)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=number_of_events)

    def test_005_in_cms_set_sport_1_to_2_sport_2_to_1_sport_3_to_1_and_save_changes(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: - Sport 1 = 2
        DESCRIPTION: - Sport 2 = 1
        DESCRIPTION: - Sport 3 = 1
        EXPECTED: Changes for In-Play module are saved
        """
        self.cms_config.update_inplay_sport_event_count(sport_number=1, event_count=2)
        self.verify_changes_saved_for_sport(sport_number=1, event_count=2)

        self.cms_config.update_inplay_sport_event_count(sport_number=2, event_count=1)
        self.verify_changes_saved_for_sport(sport_number=2, event_count=1)

        self.cms_config.update_inplay_sport_event_count(sport_number=3, event_count=1)
        self.verify_changes_saved_for_sport(sport_number=3, event_count=1)

    def test_006_verify_event_displaying_in_in_play_module(self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module if we receive the next number of events per Sport from OB:
        DESCRIPTION: - Sport 1 = 2
        DESCRIPTION: - Sport 2 = 1
        DESCRIPTION: - Sport 3 = 1
        EXPECTED: * General number of events that are displaying on 'In-Play' module is equal to the value taken in CMS
        EXPECTED: * 2 events are displayed for Sport 1
        EXPECTED: * 1 event is displayed for Sport 2
        EXPECTED: * 0 events are displayed for Sport 3
        """
        self.verify_update_on_featured_module_for_sport(sport_name=self.sport_1, event_count=2)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=2)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_2, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_3, event_count=0)

    def test_007_in_cms_set_sport_1_to_1_sport_2_to_1_sport_3_to_2_and_save_changes(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: - Sport 1 = 1
        DESCRIPTION: - Sport 2 = 1
        DESCRIPTION: - Sport 3 = 2
        DESCRIPTION: and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        self.cms_config.update_inplay_sport_event_count(sport_number=1, event_count=1)
        self.verify_changes_saved_for_sport(sport_number=1, event_count=1)

        self.cms_config.update_inplay_sport_event_count(sport_number=2, event_count=1)
        self.verify_changes_saved_for_sport(sport_number=2, event_count=1)

        self.cms_config.update_inplay_sport_event_count(sport_number=3, event_count=2)
        self.verify_changes_saved_for_sport(sport_number=3, event_count=2)

    def test_008_verify_event_displaying_in_in_play_module(self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module if we receive the next number of events per Sport from OB:
        DESCRIPTION: - Sport 1 = 1
        DESCRIPTION: - Sport 2 = 1
        DESCRIPTION: - Sport 3 = 2
        EXPECTED: * General number of events that are displaying on 'In-Play' module is equal to the value taken in CMS
        EXPECTED: * 1 event is displayed for Sport 1
        EXPECTED: * 1 event is displayed for Sport 2
        EXPECTED: * 1 event is displayed for Sport 3
        """
        self.verify_update_on_featured_module_for_sport(sport_name=self.sport_1, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_2, event_count=1)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_3, event_count=1)

    def test_009_in_cms_set_sport_1_to_3_sport_2_to_1_sport_3_to_1_and_save_changes(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: - Sport 1 = 3
        DESCRIPTION: - Sport 2 = 1
        DESCRIPTION: - Sport 3 = 1
        DESCRIPTION: and save changes
        EXPECTED: Changes for In-Play module are saved
        """
        self.cms_config.update_inplay_sport_event_count(sport_number=1, event_count=3)
        self.verify_changes_saved_for_sport(sport_number=1, event_count=3)

        self.cms_config.update_inplay_sport_event_count(sport_number=2, event_count=1)
        self.verify_changes_saved_for_sport(sport_number=2, event_count=1)

        self.cms_config.update_inplay_sport_event_count(sport_number=3, event_count=1)
        self.verify_changes_saved_for_sport(sport_number=3, event_count=1)

    def test_010_verify_event_displaying_in_in_play_module(self):
        """
        DESCRIPTION: Verify event displaying in 'In-Play' module if we receive the next number of events per Sport from OB:
        DESCRIPTION: - Sport 1 = 3
        DESCRIPTION: - Sport 2 = 1
        DESCRIPTION: - Sport 3 = 1
        EXPECTED: * General number of events that are displaying on 'In-Play' module is equal to the value taken in CMS
        EXPECTED: * 3 events are displayed for Sport 1
        EXPECTED: * 0 events are displayed for Sport 2
        EXPECTED: * 0 events are displayed for Sport 3
        """
        self.verify_update_on_featured_module_for_sport(sport_name=self.sport_1, event_count=3)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_1, event_count=3)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_2, event_count=0)
        self.verify_number_of_displayed_events_for_sport(sport_name=self.sport_3, event_count=0)
