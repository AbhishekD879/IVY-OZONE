import time
import tests
import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_sports_by_section
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.adhoc_suite
@vtest
class Test_C65946731_Verify_Inplay_Tab_visibility_for_Tier_1_and_Tier_2_sports(Common):
    """
    TR_ID: C65946731
    NAME: Verify Inplay Tab visibility for Tier 1 and Tier 2 sports
    DESCRIPTION: This Test case verifies the inplay Tab visibility in Desktop
    PRECONDITIONS: Tier1 and Tier2 sports should be
    PRECONDITIONS: configured in CMS
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    expected_tier_1_sports = ['FOOTBALL','TENNIS']
    expected_tier_2_sports = ['TABLE TENNIS', 'CRICKET', 'ESPORTS', 'BASEBALL', 'DARTS', 'SNOOKER', 'VOLLEYBALL',
                              'ICE HOCKEY', 'HANDBALL']
    enable_bs_performance_log = True
    def verify_inplay(self):
        self.site.sports_page.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
        active_tab = self.site.sports_page.tabs_menu.current
        self.assertEqual(active_tab, vec.inplay.BY_IN_PLAY.upper(),
                         msg=f'In-Play tab is not active, active is "{active_tab}"')

    def get_inplay_sub_tabs(self, tab=None):
        switchers_on_in_play = self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict
        inplay_sub_tab = next((in_tab for tab_name, in_tab in switchers_on_in_play.items() if tab_name == tab), None)
        self.assertTrue(inplay_sub_tab,msg=f'{tab} is not available for the current sport')
        return inplay_sub_tab

    def get_live_now_sections(self, type:str = None):
        time.sleep(5)
        logs = get_inplay_sports_by_section(type=type)
        if not logs:
            raise SiteServeException(f'No events Present in {type}')
        live_now_types = logs.get('eventsByTypeName')
        expected_section_names = [type['typeSectionTitleOneSport'].upper() for type in live_now_types]
        return expected_section_names

    def verify_live_now_and_upcoming_sections(self):

        # ************* Verifying live now tab and sections ****************** #
        live_now_tab = self.get_inplay_sub_tabs(tab='LIVE NOW')
        self.assertTrue(live_now_tab.is_selected())
        # **************** Verifying LIVE NOW events in WS call and FE ************* #
        expected_livenow_sections = self.get_live_now_sections(type='LIVE_EVENT')
        if not expected_livenow_sections:
            raise SiteServeException('No Live events are available')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections,
                        msg=f'Expected sections:{expected_livenow_sections} is not present in FE:{sections} in sport')
        actual_livenow_sections = list(sections.keys())
        result = set(sorted(actual_livenow_sections)).issubset(set(sorted(expected_livenow_sections)))
        self.assertTrue(result,
                        msg=f'Actual sections from FE: {sorted(actual_livenow_sections)} is not in from FE:{sorted(expected_livenow_sections)}')
        len_section = 5 if len(sections)>=5 else len(sections)
        for section_name, section in list(sections.items())[:len_section]:
            if not section.is_expanded():
                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'"{section_name}" is not expanded')
            else:
                self.assertTrue(section.is_expanded(), msg=f'"{section_name}" is not expanded')
        # ************** Verifying UPCOMING tab data ***************** #
        upcoming_tab = self.get_inplay_sub_tabs(tab='UPCOMING')
        upcoming_tab.click()
        self.site.wait_content_state_changed(timeout=10)
        inplay_upcoming_tab = self.get_inplay_sub_tabs(tab='UPCOMING')
        self.assertTrue(inplay_upcoming_tab.is_selected())
        # **************** Verifying UPCOMING events in WS call and FE ************* #
        expected_upcoming_sections = self.get_live_now_sections(type='UPCOMING_EVENT')
        if not expected_upcoming_sections:
            raise SiteServeException('No Upcoming events are available')
        upcoming_sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(upcoming_sections,msg=f'Expected sections:{expected_upcoming_sections} is not present in FE:{upcoming_sections} in sport')
        actual_upcoming_sections = list(upcoming_sections.keys())
        result = set(sorted(actual_upcoming_sections)).issubset(set(sorted(expected_upcoming_sections)))
        self.assertTrue(result,
                        msg=f'Actual sections from FE: {sorted(actual_upcoming_sections)} is not in from FE:{sorted(expected_upcoming_sections)}')
        len_section = 5 if len(upcoming_sections) >= 5 else len(upcoming_sections)
        for section_name, section in list(upcoming_sections.items())[:len_section]:
            if not section.is_expanded():
                section.expand()
                self.assertTrue(section.is_expanded(timeout=3), msg=f'"{section_name}" is not expanded')
            else:
                self.assertTrue(section.is_expanded(timeout=3), msg=f'"{section_name}" is not expanded')

    def verify_updating_score_and_odds(self):
        live_now_tab = self.get_inplay_sub_tabs(tab='LIVE NOW')
        live_now_tab.click()
        # Check if the current live sport is in the list of sports to check
        live_sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        if not live_sections:
            raise VoltronException(f"No Live Available in sports")
        for section_name, section in list(live_sections.items())[:3]:
            odds_change = False
            score_changed = False
            if not section.is_expanded():
                section.expand()
            # Maximum wait time in seconds
            max_wait_time = 30
            # Interval to check for changes in seconds
            check_interval = 5
            if not odds_change:
                # Retrieve the odds before the change
                odds_before_change = list(section.items_as_ordered_dict.items())[0][
                    1].template.first_player_bet_button.name
            if not score_changed:
                # Retrieve the score board keys before the change
                sgp_before_change = list(section.items_as_ordered_dict.items())[0][
                    1].template.score_table.items_as_ordered_dict.keys()
            if not odds_change:
                odds_after_change = list(section.items_as_ordered_dict.items())[0][
                    1].template.first_player_bet_button.name
            if not score_changed:
                sgp_after_change = list(section.items_as_ordered_dict.items())[0][
                    1].template.score_table.items_as_ordered_dict.keys()
            elapsed_time = 0
            while elapsed_time < max_wait_time:
                # Simulate waiting for a short duration (5 seconds)
                wait_for_haul(check_interval)
                elapsed_time += check_interval
                if not odds_change:
                    # Simulate retrieving the odds and score board keys after the change
                    odds_after_change = list(section.items_as_ordered_dict.items())[0][
                        1].template.first_player_bet_button.name
                if not score_changed:
                    sgp_after_change = list(section.items_as_ordered_dict.items())[0][
                        1].template.score_table.items_as_ordered_dict.keys()
                # Check if odds have changed
                if odds_before_change != odds_after_change:
                    self._logger.info("Odds changed!")
                    odds_change = True
                # Check if score board keys have changed
                if sgp_before_change != sgp_after_change:
                    self._logger.info("Score board keys changed!")
                    score_changed = True
                # Check if odds have changed
                if odds_change and score_changed:
                    break
            if odds_change and score_changed:
                break
        else:
            self.assertNotEqual(odds_before_change, odds_after_change,
                                msg='Odds did not change after waiting for few times')
            # Check if the score board keys have changed
            self.assertNotEqual(sgp_before_change, sgp_after_change,
                                msg='Score board did not changed after waiting for some times ')

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application
        EXPECTED: Application should be launched successfully
        """
        self.navigate_to_page('in-play')
        # ************************** Getting In Play Tier 2 Sports **************************************
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        tier_1_in_play_sports = []
        for sport_name, sport in sports.items():
            sport.scroll_to()
            if sport_name.upper() in self.expected_tier_1_sports and sport.counter > 0:
                tier_1_in_play_sports.append(sport_name)
        tier_2_in_play_sports = []
        for sport_name, sport in sports.items():
            sport.scroll_to()
            if sport_name.upper() in self.expected_tier_2_sports and sport.counter > 0:
                tier_2_in_play_sports.append(sport_name)
        if len(tier_1_in_play_sports) == 0:
            raise VoltronException(f'Tier 1 sports {self.expected_tier_1_sports} are not having live events')
        if len(tier_2_in_play_sports) == 0:
            raise VoltronException(f'Tier 2 sports {self.expected_tier_2_sports} are not having live events')
        self.__class__.tire1_sport = next((sport for sport in tier_1_in_play_sports if sport.upper() == "TENNIS"), tier_1_in_play_sports[0])
        self.__class__.tire2_sport = next((sport for sport in tier_2_in_play_sports if sport.upper() == "TABLE TENNIS"), tier_2_in_play_sports[0])

    def test_002_navigate_to_tier_1_sport_eg_football(self):
        """
        DESCRIPTION: Navigate to tier 1 sport e.g. football
        EXPECTED: Matches tab will load by default
        """
        self.navigate_to_page(f'sport/{self.tire1_sport}')
        self.site.wait_content_state_changed(timeout=10)

    def test_003_switch_to_inplay_tab(self):
        """
        DESCRIPTION: Switch to Inplay tab
        EXPECTED: Inplay tab should load successfully
        """
        self.verify_inplay()

    def test_004_verify_live_and_upcoming_tabs_data(self):
        """
        DESCRIPTION: Verify Live and upcoming tabs data
        EXPECTED: If live events are available then Live Tab should display all available inplay events Upcoming tab should display with preplay events.
        """
        self.verify_live_now_and_upcoming_sections()

    def test_005_verify_score_and_price_updates_in_live_tab(self):
        """
        DESCRIPTION: Verify score and price updates in Live Tab
        EXPECTED: Price and Score updates should happen correctly
        """
        self.verify_updating_score_and_odds()

    def test_006_navigate_to_tier_2_sport_eg_table_tennis(self):
        """
        DESCRIPTION: Navigate to tier 2 sport e.g. Table Tennis
        EXPECTED: Matches tab will load by default
        """
        self.navigate_to_page(f'sport/{self.tire2_sport}')
        self.site.wait_content_state_changed(timeout=10)

    def test_007_switch_to_inplay_tab(self):
        """
        DESCRIPTION: Switch to Inplay tab
        EXPECTED: Inplay tab should load successfully
        """
        self.verify_inplay()

    def test_008_verify_live_and_upcoming_tabs_data(self):
        """
        DESCRIPTION: Verify Live and upcoming tabs data
        EXPECTED: If live events are available then Live Tab should display all available inplay events Upcoming tab should display with preplay events.
        """
        self.verify_live_now_and_upcoming_sections()

    def test_009_verify_score_and_price_updates_in_live_tab(self):
        """
        DESCRIPTION: Verify score and price updates in Live Tab
        EXPECTED: Verify score and price updates in Live Tab
        """
        self.verify_updating_score_and_odds()

    def test_010_repeat_above_steps_for_all_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Repeat above steps for all tier 1 and tier 2 sports
        EXPECTED: Results should be same
        """
        pass
