import pytest
import re
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from crlat_cms_client.utils.exceptions import CMSException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_cms_reflection
from voltron.utils.helpers import get_updated_total_inplay_events_number


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.tennis_specific
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65949652_Verify_inplay_module_in_Tennis_matches_tab(Common):
    """
    TR_ID: C65949652
    NAME: Verify inplay module in Tennis matches tab.
    DESCRIPTION: This testcase inplay module in tennis matches tab.
    PRECONDITIONS: 
    """
    keep_browser_open = True
    inplay_count_cms = 0
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Matches tab can be configured from CMS->
        PRECONDITIONS: sports menu->sportscategory->Tennis->matches tab->enable/disable.
        PRECONDITIONS: 2.Get modules which are available in matches tab. Modules are cofigured from CMS.
        PRECONDITIONS: 3.Verify 'IN-PLAY' Module in matches
        """
        sport_id = self.ob_config.tennis_config.category_id
        tab_status = self.cms_config.get_sport_tab_status(sport_id=sport_id,
                                                          tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        if not tab_status:
            raise CMSException(
                f'{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches}" tab is not enabled in cms')

        modules = self.cms_config.get_sport_module(sport_id=sport_id, module_type=None)
        for module in modules:
            if not module['disabled'] and module['moduleType'] == 'INPLAY':
                self.inplay_count_cms = self.cms_config.get_max_number_of_inplay_event(sport_category=sport_id)
                break

        if not self.inplay_count_cms:
            raise CMSException('"IN-PLAY" Module is not enabled in cms for Tennis sport')

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: User should be able to launch the application successfully.
        """
        self.site.wait_content_state('Homepage')

    def test_002_click_on_tennis_sport(self):
        """
        DESCRIPTION: Click on tennis sport.
        EXPECTED: User should be able to navigate tennis landing page.
        """
        self.site.home.menu_carousel.click_item(vec.siteserve.TENNIS_TAB)
        self.site.wait_content_state(state_name='Tennis')

    def test_003_verify_matches_tab(self):
        """
        DESCRIPTION: Verify matches tab.
        EXPECTED: User should be able to see matches tab.
        """
        # Check if Matches Tab Is Selected By Default
        current_tab = self.site.sports_page.tabs_menu.current.upper()
        self.assertEqual(current_tab, vec.sb.TABS_NAME_MATCHES.upper(), msg=f"Current Active tab is {current_tab}, "
                                                                     f"Expected tab is {vec.sb.TABS_NAME_MATCHES.upper()}")

    def test_004_verify_inplay_module(self):
        """
        DESCRIPTION: Verify inplay module.
        EXPECTED: User should be able to see inplay module above the matches tab.
        """
        inplay_module_fe = self.site.sports_page.tab_content.in_play_module
        self.assertTrue(inplay_module_fe.is_displayed(), msg='"IN-PLAY" module is not displayed in tennis sport')

    def test_005_verify_count_in_inplay_header(self):
        """
        DESCRIPTION: Verify count in inplay header
        EXPECTED: Count should be displayed as SEE ALL(N)&amp;gt; where n is the number of live events
        """
        # SEE ALL displayed
        result = wait_for_cms_reflection(lambda: get_updated_total_inplay_events_number(delimiter='42'),
                                ref=self, timeout=120, expected_result=True)
        self.assertTrue(result, msg= 'inplay event count is not get from ws call')
        see_all_link = self.site.sports_page.tab_content.in_play_module.see_all_link
        self.assertTrue(see_all_link.is_displayed(),
                        msg='"See all" link is not located in the header of "In-Play" module')

        # SEE ALL count
        expected_see_all_count = int(get_updated_total_inplay_events_number(delimiter='42'))
        wait_for_haul(2)
        see_all_count_fe = int(re.search(r'\d+', see_all_link.name).group())
        self.assertEqual(see_all_count_fe, expected_see_all_count, msg=f'Actual see all count is {see_all_count_fe}, '
                                                                f'expected see all count is {expected_see_all_count}' )

    def test_006_verify_price_and_score_updates(self):
        """
        DESCRIPTION: Verify price and score updates
        EXPECTED: Price and score updates should happen correctly
        """
        inplay = self.site.sports_page.tab_content.in_play_module
        if not inplay:
            raise VoltronException(f"IN_PLAY module is not available")
        sections = list(inplay.items_as_ordered_dict.values())
        events = {}
        for section in sections:
            for event_name, event_obj in section.items_as_ordered_dict.items():
                events[event_name] = event_obj
                if len(events) == 3:
                    break
            if len(events) == 3:
                break
        check_interval = 5
        elapsed_time = 0
        max_wait_time = 120

        # Before odds and scores update
        event_scores_before = {}
        event_odds_before = {}
        # After odds and scores update
        After_event_scores = {}
        After_event_odds = {}
        odds_change_and_score_changed = False
        for name, event in events.items():
            # Retrieve the odds before the change
            event_odds_before[name] = [event.template.items_as_ordered_dict.keys()]
            event_scores_before[name] = [event.template.score_table.items_as_ordered_dict.keys()]

        while elapsed_time < max_wait_time:
            # Simulate waiting for a short duration (5 seconds)
            wait_for_haul(check_interval)
            elapsed_time += check_interval
            for name, event in events.items():
                After_event_odds[name] = [event.template.items_as_ordered_dict.keys()]
                After_event_scores[name] = [event.template.score_table.items_as_ordered_dict.keys()]
                if event_odds_before[name] != After_event_odds[name] and event_scores_before[name] != \
                        After_event_scores[name]:
                    self._logger.info("Odds changed! and scores changed!")
                    odds_change_and_score_changed = True
                    break
            if odds_change_and_score_changed:
                break
        if not odds_change_and_score_changed:
            raise VoltronException(f"scores are not changed")

    def test_007_verify_event_card_body_in_live_now_and_upcomings_sections(self):
        """
        DESCRIPTION: Verify Event Card body in live now and upcomings sections
        EXPECTED: Event Card body should show with
        EXPECTED: * fixture headers (home,draw,away)
        EXPECTED: * event1 v event 2
        EXPECTED: * Odd buttons
        EXPECTED: * Score display in live now section
        EXPECTED: * Live/watch live labels
        EXPECTED: * More markets link
        """
        inplay = self.site.sports_page.tab_content.in_play_module
        section =list(inplay.items_as_ordered_dict.values())[0]
        in_play_event = list(section.items_as_ordered_dict.items())[0][1].template

        # Displayed event name
        event_name = in_play_event.event_name_we
        self.assertTrue(event_name.is_displayed(), msg=f'{event_name} Event name not displayed')

        # Displayed odds buttons
        odds = in_play_event.items_as_ordered_dict
        self.assertTrue(odds, msg=f'odds buttons is not displayed')

        # live label displayed
        live_label = in_play_event.is_live_now_event
        self.assertTrue(live_label, msg=f'Live label is not displayed')

        # Displayed set number
        set_number = in_play_event.set_number
        self.assertTrue(set_number, msg=f'"{set_number}" is not displayed')

        # Displayed more link
        more_link = in_play_event.more_markets_link
        self.assertTrue(more_link.is_displayed(), msg='More market link is not displayed')

