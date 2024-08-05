import itertools
import re

import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.helpers import get_updated_total_inplay_events_number
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.featured
@pytest.mark.in_play
@pytest.mark.football
@pytest.mark.mobile_only
@vtest
class Test_C9697585_See_all_counter_updating_on_In_Play_module_on_Homepage_Featured_tab(BaseSportTest):
    """
    TR_ID: C9697585
    VOL_ID: C10564991
    NAME: 'See all' counter updating on 'In-Play' module on Homepage 'Featured' tab
    DESCRIPTION: This test case verifies 'See all' counter updating when undisplaying/displaying back live events on 'In-Play' module on Homepage 'Featured' tab
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: - 'In-Play' module is enabled in CMS > System Configuration > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module is set to 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 2 Sports with Live event are added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    PRECONDITIONS: 2) In-play events should be present for selected sports
    PRECONDITIONS: 3) To check value, displayed in counter open Dev Tools->Network->WS > featured-sports > InplayModule response > 'totalEvents' attribute
    PRECONDITIONS: Load the app > Homepage > 'Featured' tab
    PRECONDITIONS: 'In-Play' module with live events is displayed on 'Featured' tab
    """
    keep_browser_open = True

    def check_in_play_counter(self, actual_number_of_in_play_events: int) -> None:
        """
        This method compares two In-Play counter values - one is taken from UI and another from websocket
        """
        expected_total_events_number = int(get_updated_total_inplay_events_number())
        self.assertEqual(actual_number_of_in_play_events, expected_total_events_number,
                         msg=f'In-Play events counter "{actual_number_of_in_play_events}" is not the same as '
                             f'expected "{expected_total_events_number}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find existing sport event within In-Play module and get it name from SiteServe
        DESCRIPTION: If there no any sport events within In-Play module then create new one
        """
        self.site.wait_content_state(state_name='HomePage', timeout=5)
        try:
            in_play_module = get_in_play_module_from_ws()
            self.assertTrue(in_play_module, msg='There is no In-play module in ws')
            in_play_module_data = in_play_module['data']
            fb_event_ids = [sport_segment['eventsIds'] for sport_segment in in_play_module_data if sport_segment['categoryName'] == 'Football']
            flatten_ids = list(itertools.chain.from_iterable(fb_event_ids))
        except KeyError:
            flatten_ids = None

        if flatten_ids:
            self.__class__.event_id = flatten_ids[0]
            event_details = self.ss_req.ss_event(event_id=self.event_id, query_builder=self.ss_query_builder)
            self.__class__.event_name = normalize_name(event_details[0]['event']['name'])
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.event_id = event_params.event_id
            self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2

    def test_001_trigger_completion_expiration_of_in_play_event_of_any_sport_under_test_eg_football(self):
        """
        DESCRIPTION: Trigger completion/expiration of in-play event of any <sport> under test e.g. Football
        DESCRIPTION: NOTE: Event completion/expiration means that event is not present on SiteServer anymore (attribute 'displayed="N"' is set for event )
        EXPECTED: * Completed/expired event is removed from front-end automatically
        EXPECTED: * Counter next to 'See all' link is updated automatically
        EXPECTED: * Updated value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        self.__class__.sport = 'Football' if not self.brand == 'ladbrokes' else 'FOOTBALL'
        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab, home_featured_tab_name,
                         msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                             f'expected: "{home_featured_tab_name}"')
        in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='In-Play module has no any event groups')
        self.assertIn(self.sport, in_play_event_groups,
                      msg=f'"{self.sport}" events are not shown among available: "{in_play_event_groups.keys()}"')
        fb_events_group = in_play_event_groups[self.sport]
        in_play_fb_events = fb_events_group.items_as_ordered_dict
        self.assertIn(self.event_name, in_play_fb_events.keys(),
                      msg=f'"{self.event_name}" event is not shown among other in-play events: '
                          f'"{in_play_fb_events.keys()}"')

        self.__class__.see_all_link = self.site.home.tab_content.in_play_module.see_all_link
        self.assertTrue(self.see_all_link.is_displayed(),
                        msg='"See all" link is not located in the header of "In-Play" module')
        initial_number_of_in_play_events = int(re.search(r'\d+', self.see_all_link.name).group())

        self.ob_config.change_event_state(event_id=self.event_id, displayed=False, active=False)

        result = wait_for_result(
            lambda: int(re.search(r'\d+', self.site.home.tab_content.in_play_module.see_all_link.name).group()) == initial_number_of_in_play_events - 1,
            name='Counter next to "See all" link to update automatically',
            timeout=45
        )
        self.assertTrue(result, msg='Counter next to "See all" link has not changed after event completion')
        self.__class__.updated_number_of_in_play_events = \
            int(re.search(r'\d+', self.site.home.tab_content.in_play_module.see_all_link.name).group())
        self.check_in_play_counter(actual_number_of_in_play_events=self.updated_number_of_in_play_events)

        result = wait_for_result(lambda: self.event_name in fb_events_group.items_as_ordered_dict.keys(),
                                 expected_result=False,
                                 name=f'"{self.event_name}" to disappear from In_Play module')
        self.assertFalse(result, msg=f'"{self.event_name}" event still shown within In_Play module')

    def test_002_trigger_starting_of_event_in_play_event_of_any_sport_under_test_eg_football(self):
        """
        DESCRIPTION: Trigger starting of event in-play event of any <sport> under test e.g. Football
        EXPECTED: * Started event appears on front-end (after refresh)
        EXPECTED: * Counter next to 'See all' link is updated automatically (without refresh)
        EXPECTED: * Updated value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        self.ob_config.change_event_state(event_id=self.event_id, displayed=True, active=True)

        result = wait_for_result(
            lambda: int(re.search(r'\d+', self.site.home.tab_content.in_play_module.see_all_link.name).group()) == self.updated_number_of_in_play_events + 1,
            name='Counter next to "See all" link to update automatically',
            timeout=45
        )
        self.assertTrue(result, msg='Counter next to "See all" link has not changed after event starting')
        number_of_in_play_events = int(re.search(r'\d+', self.site.home.tab_content.in_play_module.see_all_link.name).group())
        self.check_in_play_counter(actual_number_of_in_play_events=number_of_in_play_events)

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        in_play_event_groups = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(in_play_event_groups, msg='In-Play module has no any event groups')
        self.assertIn(self.sport, in_play_event_groups,
                      msg=f'"{self.sport}" events are not shown among available: "{in_play_event_groups.keys()}"')
        fb_events_group = in_play_event_groups[self.sport]

        result = wait_for_result(lambda: self.event_name in fb_events_group.items_as_ordered_dict.keys(),
                                 name=f'"{self.event_name}" event to appear in In_Play module')
        self.assertTrue(result, msg=f'"{self.event_name}" event is not shown within In_Play module')
