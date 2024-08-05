import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import get_expected_inplay_events_order
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.in_play
@pytest.mark.american_football
@pytest.mark.cms
@vtest
class Test_C8146749_Count_of_live_events_displayed_on_In_Play_module_on_SLP_based_on_CMS_config(BaseSportTest):
    """
    TR_ID: C8146749
    VOL_ID: C10621022
    NAME: Count of live events displayed on 'In-Play' module on SLP based on CMS config
    DESCRIPTION: This test case verifies that number of live events, displayed within 'In-Play' module on SLP, is based on CMS config
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: - 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: - 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: - 'In-play' module is set to 'Active'
    PRECONDITIONS: - 'Inplay event count' is set to e.g. 5
    PRECONDITIONS: 2) Sport (e.g. Football) with available live events within several types created in OB e.g.:
    PRECONDITIONS: * Championship (e.g."typeDisplayOrder": 1), events available: 4
    PRECONDITIONS: * Premier League (e.g. "typeDisplayOrder": 2), events available: 3
    PRECONDITIONS: * League Two (e.g. "typeDisplayOrder": 3), events available: 3
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    keep_browser_open = True
    league_name = tests.settings.football_autotest_competition_league
    max_number_of_events = 5

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        cms_config.update_inplay_event_count(sport_category=1, event_count=cls.max_number_of_events)

    def wait_all_events_displayed(self, compare=True) -> bool:
        """
        Wait max In Play module count changed
        :param compare: flag for comparing values
        :return: True or False
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.__class__.events_count = 0
        in_play_module = self.site.american_football.tab_content.in_play_module
        self.assertTrue(in_play_module.is_displayed(), msg='In play module does not display')
        inplay_module_items = in_play_module.items_as_ordered_dict
        self.assertTrue(inplay_module_items, msg='There are not leagues on In Play module')
        for league in inplay_module_items.values():
            self.events_count += len(league.items_as_ordered_dict.keys())
        if compare:
            return self.events_count > self.num_of_events_to_display
        else:
            return self.events_count == self.num_of_events_to_display

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In-play events should be present for selected sport e.g. American Football:
        PRECONDITIONS: Championship (e.g."typeDisplayOrder": 1), events available: 4
        PRECONDITIONS: Premier League (e.g. "typeDisplayOrder": 2), events available: 3
        PRECONDITIONS: League Two (e.g. "typeDisplayOrder": 3), events available: 3
        PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
        PRECONDITIONS: Open 'Matches' tab
        """
        inplay_module_config = self.get_initial_data_system_configuration().get('Inplay Module', {})
        if not inplay_module_config:
            inplay_module_config = self.cms_config.get_system_configuration_item('Inplay Module')
        if not inplay_module_config.get('enabled'):
            raise CmsClientException('"Inplay Module" module is disabled in system config')

        self.__class__.category_id = self.ob_config.backend.ti.american_football.category_id
        inplay_module = self.cms_config.get_sport_module(sport_id=self.category_id,
                                                         module_type='INPLAY')
        if inplay_module[0]['disabled']:
            raise CmsClientException(f'"In play module" module is disabled for category {self.ob_config.backend.ti.american_football.category_id}')

        for _ in range(4):
            self.ob_config.add_american_football_event_to_ncaa_bowls(is_live=True)
        for _ in range(3):
            self.ob_config.add_american_football_event_to_nfl(is_live=True)
            self.ob_config.add_american_football_event_to_autotest_league(is_live=True)
        self.cms_config.update_inplay_event_count(sport_category=self.category_id, event_count=self.max_number_of_events)
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state('american-football')
        inplay_module = self.cms_config.get_sport_module(sport_id=self.category_id, module_type='INPLAY')
        id_ = inplay_module[0].get('id')
        sport_details = self.cms_config.get_sport_module_details(_id=id_)
        self.__class__.num_of_events_to_display = sport_details['inplayConfig'].get('maxEventCount')
        self.assertEqual(self.num_of_events_to_display, self.max_number_of_events,
                         msg=f'Cannot update max In Play module count. Actual is: {self.num_of_events_to_display}, '
                             f'expected is:{self.max_number_of_events} ')

    def test_001_verify_total_count_of_live_events_displayed_within_in_play_module(self):
        """
        DESCRIPTION: Verify total count of live events displayed within 'In-Play' module
        EXPECTED: 5 in-play events are displayed (corresponds to number, set in 'Inplay event count' field in CMS)
        """
        result = wait_for_result(lambda: get_in_play_module_from_ws(delimiter='42/1,', timeout=0),
                                 name='InPlay module to Appear in WS',
                                 timeout=60,
                                 poll_interval=2)
        if not result:
            raise ThirdPartyDataException('In Play module not present in WS')

        result = wait_for_result(lambda: self.wait_all_events_displayed(compare=False),
                                 timeout=10,
                                 name='All available live events are not displayed',
                                 poll_interval=3)
        self.assertTrue(result, msg=f'{self.events_count} in-play events are displayed, '
                                    f'should be {self.num_of_events_to_display}')

    def test_002_verify_events_grouping(self):
        """
        DESCRIPTION: Verify events grouping
        EXPECTED: * Events are grouped by OB Class/TypeID and sorted by Class 'displayOrder' and type 'DisplayOrder' in ascending
        """
        displayed_events = []
        self.__class__.inplay_module_items = \
            self.site.american_football.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(self.inplay_module_items, msg='Can not find any module items')
        for _, league in self.inplay_module_items.items():
            displayed_events += list(league.items_as_ordered_dict.keys())

        expected_events = get_expected_inplay_events_order(delimiter='42/1,')
        self.assertListEqual(displayed_events, expected_events,
                             msg=f'Incorrect events order. Actual is: {displayed_events}. Expected is:{expected_events}')

    def test_003_verify_events_displayed_within_in_play_module_based_on_set_up_from_pre_conditions(self):
        """
        DESCRIPTION: Verify events displayed within 'In-Play' module (based on set up from pre-conditions)
        EXPECTED: * 4 events of 'Championship' type are displayed
        EXPECTED: * 1 event of 'Premier League' type is displayed
        EXPECTED: * 0 events of 'League Two' type
        """
        ncaa_league = self.inplay_module_items.get(vec.siteserve.NCCA_BOWLS)
        self.assertTrue(ncaa_league, msg=f'"{vec.siteserve.NCCA_BOWLS}" league is not present on "{self.inplay_module_items.keys()}"')
        first_type_events = len(ncaa_league.items_as_ordered_dict)
        self.assertTrue(first_type_events >= 4,
                        msg=f'Incorrect events count are displayed within In-Play module. Expected is: "4" '
                            f'actual: "{first_type_events}"')

        second_type_events = self.inplay_module_items.get('NFL')
        third_type_events = self.inplay_module_items.get(self.league_name)
        if first_type_events == 4:
            self.assertEqual(len(second_type_events.items_as_ordered_dict), 1,
                             msg=f'Incorrect event count is displayed. Actual: '
                                 f'{len(second_type_events.items_as_ordered_dict)}, expected: 1')
            self.assertIsNone(third_type_events, msg='Events for third type is present')

    def test_004_in_cms_set_inplay_event_count_to_20_in_application_refresh_the_page_and_verify_count_of_live_events_displayed(self):
        """
        DESCRIPTION: * In CMS set 'Inplay event count' to 20
        DESCRIPTION: * In application refresh the page and verify count of live events displayed
        EXPECTED: All available live events are displayed i.e. 10 (based on set up from pre-conditions)
        """
        self.cms_config.update_inplay_event_count(sport_category=1, event_count=20)
        result = wait_for_result(
            lambda: self.wait_all_events_displayed,
            timeout=10, name='All available live events are not displayed', poll_interval=3)
        self.assertTrue(result,
                        msg=f'{self.events_count} in-play events count should be bigger '
                            f'than {self.max_number_of_events}')
