import re
import pytest
import tests
from voltron.utils.helpers import normalize_name
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_updated_total_inplay_events_number, get_in_play_module_from_ws
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.football
@pytest.mark.mobile_only
@vtest
class Test_C9697584_See_all_counter_updating_on_In_Play_module_on_SLP(BaseSportTest):
    """
    TR_ID: C9697584
    VOL_ID: C10564960
    NAME: 'See all' counter updating on 'In-Play' module on SLP
    DESCRIPTION: This test case verifies 'See all' counter updating when undisplaying/displaying back live events on 'In-Play' module on SLP
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: * 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: * 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: * 'In-play' module is set to 'Active'
    PRECONDITIONS: * 'Inplay event count' is set to any digit e.g. 10
    PRECONDITIONS: 2) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: 3) To check value, displayed in counter open Dev Tools->Network->WS > featured-sports > InplayModule response > 'totalEvents' attribute
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    not_autotest_event_used = True
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.not_autotest_event_used:
            ob_config = cls.get_ob_config()
            ob_config.change_event_state(event_id=cls.eventID, displayed=True, active=True)

    def check_in_play_counter(self, actual_number_of_in_play_events: int) -> None:
        """
        This method compares two In-Play counter values - one is taken from UI and another from websocket
        """
        expected_total_events_number = int(get_updated_total_inplay_events_number(delimiter='42/16,'))
        self.assertEqual(actual_number_of_in_play_events, expected_total_events_number,
                         msg=f'In-Play events counter "{actual_number_of_in_play_events}" is not the same as '
                             f'expected "{expected_total_events_number}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the app and navigate to <Sport> Landing page under test e.g. Football
        DESCRIPTION: Open 'Matches' tab
        DESCRIPTION: Find existing sport event within In-Play module and get it name from SiteServe
        DESCRIPTION: If there no any sport events within In-Play module then create new one
        """
        inplay_module = self.cms_config.get_sport_module(sport_id=self.ob_config.backend.ti.football.category_id,
                                                         module_type='INPLAY')
        if inplay_module[0]['disabled']:
            raise CmsClientException('"In play module" module is disabled for Football category')
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        result = self.site.football.tabs_menu.click_button(self.expected_sport_tabs.matches)
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.matches}" tab was not opened')
        try:
            in_play_module = get_in_play_module_from_ws(delimiter='42/16,')
            self.assertTrue(in_play_module, msg='There is no In-play module in ws')
            in_play_module_data = in_play_module['data']
            flatten_ids = next((sport_segment['eventsIds'] for sport_segment in in_play_module_data if sport_segment['categoryName'] == 'Football'), None)
            self._logger.info(f'*** Found event ids in In-Play module: {flatten_ids}')
        except KeyError:
            flatten_ids = None

        if flatten_ids:
            self.__class__.eventID = flatten_ids[0]
            event_details = self.ss_req.ss_event(event_id=self.eventID, query_builder=self.ss_query_builder)
            self.__class__.event_name = normalize_name(event_details[0]['event']['name'])
            self.__class__.event_league = event_details[0]['event']['typeName'] if not self.brand == 'ladbrokes' else event_details[0]['event']['typeName'].upper()
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.not_autotest_event_used = False
            self.__class__.eventID = event_params.event_id
            self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
            self.__class__.event_league = tests.settings.football_autotest_league if not self.brand == 'ladbrokes' else tests.settings.football_autotest_league.upper()

    def test_001_trigger_completion_expiration_of_in_play_event_of_sport_under_test_eg_football(self):
        """
        DESCRIPTION: Trigger completion/expiration of in-play event of <sport> under test e.g. Football
        DESCRIPTION: NOTE: Event completion/expiration means that event is not present on SiteServer anymore (attribute 'displayed="N"' is set for event )
        EXPECTED: * Completed/expired event is removed from front-end automatically
        EXPECTED: * Counter next to 'See all' link is updated automatically
        EXPECTED: * Updated value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        in_play_event_groups = self.site.football.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='In-Play module has no any event groups')
        self.assertIn(self.event_league, in_play_event_groups,
                      msg=f'"{self.event_league}" league is not shown among available: "{in_play_event_groups.keys()}"')
        fb_events_group = in_play_event_groups[self.event_league]
        in_play_fb_events = fb_events_group.items_as_ordered_dict
        event_count = len(in_play_fb_events)
        self.assertIn(self.event_name, in_play_fb_events.keys(),
                      msg=f'"{self.event_name}" event is not shown among other in-play events: '
                          f'"{in_play_fb_events.keys()}"')
        self.__class__.see_all_link = self.site.football.tab_content.in_play_module.see_all_link
        self.assertTrue(self.see_all_link.is_displayed(),
                        msg='"See all" link is not located in the header of "In-Play" module')
        initial_number_of_in_play_events = int(re.search(r'\d+', self.see_all_link.name).group())
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        result = wait_for_result(
            lambda: int(re.search(r'\d+', self.see_all_link.name).group()) == initial_number_of_in_play_events - 1,
            name='Counter next to "See all" link to update automatically',
            timeout=45
        )
        self.assertTrue(result, msg='Counter next to "See all" link has not changed after event completion')
        self.__class__.updated_number_of_in_play_events = int(re.search(r'\d+', self.see_all_link.name).group())
        self.check_in_play_counter(actual_number_of_in_play_events=self.updated_number_of_in_play_events)
        fb_events_group = self.site.football.tab_content.in_play_module.items_as_ordered_dict.get(self.event_league)

        if event_count > 1:
            self.assertTrue(fb_events_group, msg=f"Event group '{self.event_league}' was not found")
            result = wait_for_result(lambda: self.event_name in list(fb_events_group.items_as_ordered_dict.keys()),
                                     expected_result=False,
                                     name=f'"{self.event_name}" to disappear from In_Play module')
            self.assertFalse(result, msg=f'"{self.event_name}" event still shown within In_Play module')
        else:
            self.assertTrue(fb_events_group is None, msg=f"Event group '{self.event_league}' was found")

    def test_002_trigger_starting_of_event_in_play_event_of_sport_under_test_eg_football(self):
        """
        DESCRIPTION: Trigger starting of event in-play event of <sport> under test e.g. Football
        EXPECTED: * Started event appears on front-end (after refresh)
        EXPECTED: * Counter next to 'See all' link is updated automatically (without refresh)
        EXPECTED: * Updated value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        result = wait_for_result(
            lambda: int(re.search(r'\d+', self.see_all_link.name).group()) == self.updated_number_of_in_play_events + 1,
            name='Counter next to "See all" link to update automatically',
            timeout=45
        )
        self.assertTrue(result, msg='Counter next to "See all" link has not changed after event starting')
        number_of_in_play_events = int(re.search(r'\d+', self.see_all_link.name).group())
        self.check_in_play_counter(actual_number_of_in_play_events=number_of_in_play_events)

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        in_play_event_groups = self.site.football.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='In-Play module has no any event groups')
        self.assertIn(self.event_league, in_play_event_groups,
                      msg=f'"{self.event_league}" league is not shown among available: "{in_play_event_groups.keys()}"')
        fb_events_group = in_play_event_groups[self.event_league]
        result = wait_for_result(lambda: self.event_name in list(fb_events_group.items_as_ordered_dict.keys()),
                                 name=f'"{self.event_name}" event to appear in In_Play module')
        self.assertTrue(result, msg=f'"{self.event_name}" event is not shown within In_Play module')
