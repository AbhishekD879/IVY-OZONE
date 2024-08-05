import re

import pytest
import tests
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.base_test import vtest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C2322262_Verify_Live_Updates_suspension_for_PlacepotQuadpotJackpotScoop6_pool_types_on_HR_EDP(BaseUKTote):
    """
    TR_ID: C2322262
    NAME: Verify Live Updates (suspension) for Placepot/Quadpot/Jackpot/Scoop6 pool types on HR EDP
    DESCRIPTION: This test case verifies Live Updates (suspension) for Placepot/Quadpot/Jackpot/Scoop6 pool types on HR EDP
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [UK Tote: Implement HR Exacta pool type] [1]
    DESCRIPTION: [UK Tote: Implement HR Trifecta pool type] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28444
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-28445
    PRECONDITIONS: * The HR event should have available:
    PRECONDITIONS: -Placepot pool type
    PRECONDITIONS: -Quadpot pool type
    PRECONDITIONS: -Jackpot pool type
    PRECONDITIONS: -Scoop6 pool type
    PRECONDITIONS: * User should have a HR EDP with Placepot pool type open (Leg1)
    """
    keep_browser_open = True
    active_events = {}
    pools = {}

    def verify_pool_types_presence(self, type_name, **kwargs):
        """
        Verify if pool type is present and add to pools dictionary
        """
        try:
            self.pools[type_name] = self.get_uk_tote_event(**kwargs)
        except SiteServeException:
            pass

    def test_001_suspend_current_event_in_ti(self, type_name=None, event=None):
        """
        DESCRIPTION: Suspend current event in TI
        EXPECTED: * All Leg1 check boxes become disabled in real time
        EXPECTED: * All check boxes in other Leg's remain active
        """
        type_name, event = (type_name, event) if type_name and event \
            else (vec.uk_tote.UK_TOTE_TABS.placepot, self.get_uk_tote_event(uk_tote_placepot=True))

        self.__class__.event_id = event.event_id
        self.__class__.market_id = event.market_id
        self.__class__.event_type = event.event_typename.strip()
        self.__class__.event_time = event.event_time
        self.__class__.selection_ids = event.selection_ids

        s = SiteServeRequests(env=tests.settings.backend_env,
                              class_id=self.ob_config.backend.ti.horse_racing.horse_racing_live.class_id,
                              category_id=self.ob_config.backend.ti.horse_racing.category_id,
                              brand=self.brand)

        events_filter = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A'))

        pools = s.ss_events_to_outcome_for_markets(market_ids=[self.market_id], query_builder=events_filter)
        self.assertTrue(pools, msg='There are no outcomes of events')

        for item in pools[0]['event']['children'][0]['market']['children']:
            self.active_events[item['outcome']['name'].strip('|')] = item['outcome']['id']
        self.assertTrue(self.active_events, msg=f'Active events are not found in Siteserve response "{pools}"')

        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='"%s" tab is not opened' % vec.racing.RACING_EDP_MARKET_TABS.totepool)

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, self.__class__.section = list(sections.items())[0]
        placepot_opened = self.section.grouping_buttons.click_button(type_name)
        self.assertTrue(placepot_opened, msg=f'"{type_name}" tab is not opened')

        pool_legs = self.section.pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(pool_legs, msg='There are no available pool legs')

        for leg_name, leg in pool_legs.items():
            pool = self.section.pool
            second_event_time_ui = (re.search(r'\d*:\d*', pool.race_title)).group()
            self.__class__.outcomes_diff_event, self.__class__.leg_diff = pool.items_as_ordered_dict, leg_name
            if second_event_time_ui != self.event_time:
                for selection_name, selection in self.outcomes_diff_event.items():
                    if not selection.checkbox.is_enabled():
                        pool.grouping_buttons.click_button(button_name=leg_name)
                        break
                    else:
                        self.__class__.second_active_selection = selection_name
                        break
                break
            else:
                pool.grouping_buttons.click_button(button_name=leg_name)
        self.assertTrue(self.second_active_selection, msg='Cannot find other active pool')
        self.ob_config.change_event_state(event_id=self.event_id, displayed=True, active=False)

        pool_legs_susp = self.section.pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(pool_legs_susp, msg='There are no available pool legs')

        outcomes_diff_event = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes_diff_event, msg='No pools outcomes found')
        active_event = outcomes_diff_event.get(self.second_active_selection)
        self.assertTrue(active_event, msg=f'"{self.second_active_selection}" not found')
        self.assertTrue(active_event.checkbox.is_enabled(timeout=10),
                        msg=f'Active check box in other Leg: "{self.leg_diff}" is suspended')

        for leg_name_susp, leg_susp in pool_legs_susp.items():
            pool = self.section.pool
            event_time_ui = (re.search(r'\d*:\d*', self.section.pool.race_title)).group()
            if event_time_ui == self.event_time:
                outcomes = pool.items_as_ordered_dict
                self.assertTrue(outcomes, msg=f'No outcomes found for pool')
                for selection_name, selection in outcomes.items():
                    self.assertFalse(selection.checkbox.is_enabled(expected_result=False, timeout=20),
                                     msg=f'Check box is active for "{selection_name}"')
                break
            else:
                self.__class__.main_leg = leg_name_susp
                pool.grouping_buttons.click_button(button_name=leg_name_susp)

    def test_002_make_the_event_active_again_in_ti(self):
        """
        DESCRIPTION: Make the event active again in TI
        EXPECTED: All Leg1 check boxes become active in real time
        """
        self.ob_config.change_event_state(event_id=self.event_id, displayed=True, active=True)
        outcomes = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found for pool leg')
        for selection_name, selection in outcomes.items():
            if selection_name in self.active_events.keys():
                self.assertTrue(selection.checkbox.is_enabled(timeout=20),
                                msg=f'Check box was not un suspended for "{selection_name}"')

    def test_003_suspend_market_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend market from current event in TI
        EXPECTED: * All Leg1 check boxes become disabled in real time
        EXPECTED: * All check boxes in other Leg's remain active
        """
        self.ob_config.change_market_state(event_id=self.event_id, market_id=self.market_id, displayed=True)

        outcomes = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes found for pool')
        for selection_name, selection in outcomes.items():
            self.assertFalse(selection.checkbox.is_enabled(expected_result=False, timeout=20),
                             msg=f'Check box is active for "{selection_name}"')
        self.section.pool.grouping_buttons.click_button(button_name=self.leg_diff)
        outcomes_diff_event = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes_diff_event[self.second_active_selection].checkbox.is_enabled(timeout=15),
                        msg=f'Active check box in other Leg: "{self.leg_diff}" is suspended')
        self.section.pool.grouping_buttons.click_button(button_name=self.main_leg)

    def test_004_make_the_market_active_again_in_ti(self):
        """
        DESCRIPTION: Make the market active again in TI
        EXPECTED: All Exacta check boxes become active in real time
        """
        self.ob_config.change_market_state(
            event_id=self.event_id, market_id=self.market_id, displayed=True, active=True)

        outcomes = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found for pool leg')
        for selection_name, selection in outcomes.items():
            if selection_name in self.active_events.keys():
                self.assertTrue(selection.checkbox.is_enabled(timeout=20),
                                msg=f'Check box is not un-suspended for "{selection_name}"')

    def test_005_suspend_one_or_more_selections_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend one or more selections from current event in TI
        EXPECTED: * Particular suspended Leg1 check boxes become disabled in real time
        EXPECTED: * All check boxes in Leg1 remain active
        EXPECTED: * All check boxes in other Leg's remain active
        """
        for sel_id in self.selection_ids:
            if sel_id in self.active_events.values():
                self.ob_config.change_selection_state(selection_id=sel_id, displayed=True)
                for name, selection_id in self.active_events.items():
                    if selection_id == sel_id:
                        self.__class__.susp_selection_name, self.__class__.susp_selection_id = name, selection_id
                break

        outcomes = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found for pool leg')

        for selection_name, selection in outcomes.items():
            if selection_name == self.susp_selection_name:
                self.assertFalse(selection.checkbox.is_enabled(expected_result=False, timeout=20),
                                 msg=f'Check box was not un suspended for "{selection_name}"')
            else:
                self.assertTrue(selection.checkbox.is_enabled(timeout=10),
                                msg=f'Check box was not un suspended for "{selection_name}"')
        self.section.pool.grouping_buttons.click_button(button_name=self.leg_diff)
        outcomes_diff_event = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes_diff_event[self.second_active_selection].checkbox.is_enabled(timeout=20),
                        msg=f'Active check box in other Leg: "{self.leg_diff}" is suspended')
        self.section.pool.grouping_buttons.click_button(button_name=self.main_leg)

    def test_006_make_the_selections_active_again_in_ti(self):
        """
        DESCRIPTION: Make the selection(s) active again in TI
        EXPECTED: Particular suspended Exacta check boxes become active again in real time
        """
        self.ob_config.change_selection_state(selection_id=self.susp_selection_id, displayed=True, active=True)
        outcomes = self.section.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found for pool leg')
        self.assertTrue(outcomes[self.susp_selection_name].checkbox.is_enabled(timeout=20),
                        msg=f'Check box is not un-suspended for "{self.susp_selection_name}"')

    def test_007_repeat_steps_1_6_for_quadpot_pool_type_jackpot_pool_type_scoop6_pool_type(self):
        """
        DESCRIPTION: Repeat steps 1-6 for:
        DESCRIPTION: * Quadpot pool type
        DESCRIPTION: * Jackpot pool type
        DESCRIPTION: * Scoop6 pool type
        EXPECTED:
        """
        self.verify_pool_types_presence(vec.uk_tote.UK_TOTE_TABS.quadpot, uk_tote_quadpot=True)
        self.verify_pool_types_presence(vec.uk_tote.UK_TOTE_TABS.jackpot, uk_tote_jackpot=True)
        self.verify_pool_types_presence(vec.uk_tote.UK_TOTE_TABS.scoop6, uk_tote_scoop6=True)
        for type_name, event in self.pools.items():
            self.test_001_suspend_current_event_in_ti(type_name=type_name, event=event)
            self.test_002_make_the_event_active_again_in_ti()
            self.test_003_suspend_market_from_current_event_in_ti()
            self.test_004_make_the_market_active_again_in_ti()
            self.test_005_suspend_one_or_more_selections_from_current_event_in_ti()
            self.test_006_make_the_selections_active_again_in_ti()
