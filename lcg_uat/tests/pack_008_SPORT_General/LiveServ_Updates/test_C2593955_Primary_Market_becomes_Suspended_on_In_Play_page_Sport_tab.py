import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import get_inplay_sports_ribbon
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot perform liveserv updated on prod endpoints
# @pytest.mark.hl
@pytest.mark.in_play
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.timeout(900)
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C2593955_Primary_Market_becomes_Suspended_on_In_Play_page_Sport_tab(BaseSportTest):
    """
    TR_ID: C2593955
    NAME: Primary Market becomes Suspended on In-Play page <Sport> tab
    """
    keep_browser_open = True
    live_now_type = vec.inplay.LIVE_NOW_SWITCHER
    upcoming_type = vec.inplay.UPCOMING_SWITCHER

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Live/Upcoming events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.live_event_id = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.live_event_id,
                                                               query_builder=self.ss_query_builder)
        self.__class__.live_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.live_event_name}"')

        self.__class__.live_market_id = self.ob_config.market_ids[self.live_event_id][market_short_name]

        event_params = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True)
        self.__class__.upcoming_event_id = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.live_event_id,
                                                               query_builder=self.ss_query_builder)
        self.__class__.upcoming_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.live_event_name}"')
        self.__class__.upcoming_market_id = self.ob_config.market_ids[self.upcoming_event_id][market_short_name]

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_page_sport_tab=True)

    def test_001_navigate_to_in_play_landing_page(self):
        """
        DESCRIPTION: Navigate to 'In-Play' landing page
        EXPECTED: 'In-Play' page opened
        """
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')

    def test_002_select_sport_from_sports_ribbon(self):
        """
        DESCRIPTION: Select '<Sport>' from sports ribbon
        """
        result = wait_for_result(lambda: int(self.ob_config.football_config.category_id) in [category
                                 .get('categoryId') for category in get_inplay_sports_ribbon()],
                                 name='Football to appear in Inplay sports ribbon',
                                 timeout=60,
                                 poll_interval=2)
        if not result:
            raise ThirdPartyDataException('Football category is not present in WS')
        self.site.inplay.inplay_sport_menu.click_item(vec.siteserve.FOOTBALL_TAB)

    def test_003_choose_tab_sorting_type(self, sorting_type=live_now_type):
        """
        DESCRIPTION: Choose tab sorting type
        EXPECTED: **For desktop view:**
        EXPECTED: Click on **'Live Now'** tab sorting type
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(sorting_type.upper())
        self.__class__.event_name = self.live_event_name if 'LIVE' in sorting_type.upper() else self.upcoming_event_name
        self.__class__.eventID = self.live_event_id if 'LIVE' in sorting_type.upper() else self.upcoming_event_id
        self.__class__.marketID = self.live_market_id if 'LIVE' in sorting_type.upper() else self.upcoming_market_id

    def test_004_find_an_event_with_price_odds_buttons_displaying_prices(self, sorting_type=live_now_type):
        """
        DESCRIPTION: Find an event with Price/Odds buttons displaying prices
        """
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name, inplay_section=sorting_type)
        self.assertTrue(event, msg=f'Event "{self.event_name}" disappears from section: "{self.section_name}"')

    def test_005_trigger_primary_market_suspension(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION:  * marketStatusCode="S" for '<Primary market>' market type
        DESCRIPTION:  * and at the same time have In-Play page <Sport> tab opened to watch for updates
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)

    def test_006_verify_outcomes_for_the_event(self, sorting_type=live_now_type):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled on
        EXPECTED: Football In-Play page but still displaying the prices
        """
        self.verify_price_buttons_state(section_name=self.section_name,
                                        event_id=self.eventID,
                                        expected_result=False,
                                        inplay_section=sorting_type,
                                        level='market')

    def test_007_trigger_primary_market_activation(self, sorting_type=live_now_type):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: marketStatusCode="A" for '<Primary market>' market type
        DESCRIPTION: and at the same time have In-Play page <Sport> tab opened to watch for updates
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.verify_price_buttons_state(section_name=self.section_name,
                                        event_id=self.eventID,
                                        inplay_section=sorting_type,
                                        level='market')

    def test_008_collapse_section_where_this_event_belongs_to(self, sorting_type=live_now_type):
        """
        DESCRIPTION: Collapse section where this event belongs to
        """
        if self.device_type == 'desktop':
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.inplay.tab_content.live_now.items_as_ordered_dict if 'LIVE' in sorting_type.upper() \
                else self.site.inplay.tab_content.upcoming.items_as_ordered_dict
        self.assertTrue(sections, msg='No one league section found on Football page')
        self.assertIn(self.section_name, list(sections.keys()), msg=f'No {self.section_name} in {sections.keys()}')
        sections[self.section_name].collapse()

    def test_009_trigger_primary_market_suspension(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: marketStatusCode="S" for 'Primary market' market type
        """
        self.test_005_trigger_primary_market_suspension()

    def test_010_expand_section_with_the_event_and_verify_its_outcomes(self, is_enabled=False, sorting_type=live_now_type):
        """
        DESCRIPTION: Expand section with the event and verify its outcomes
        EXPECTED: All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled on
        EXPECTED: Football In-Play page but still displaying the prices
        """
        self.verify_price_buttons_state(section_name=self.section_name,
                                        event_id=self.eventID,
                                        expected_result=is_enabled,
                                        inplay_section=sorting_type,
                                        level='market',
                                        timeout=40)

    def test_011_collapse_section(self):
        """
        DESCRIPTION: Collapse section
        """
        self.test_008_collapse_section_where_this_event_belongs_to()

    def test_012_trigger_primary_market_activation(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: marketStatusCode="A" for '<Primary market>' market type
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)

    def test_013_expand_section_and_verify_outcomes_for_the_event(self, sorting_type=live_now_type):
        """
        DESCRIPTION: Expand section and verify outcomes for the event
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        self.test_010_expand_section_with_the_event_and_verify_its_outcomes(is_enabled=True, sorting_type=sorting_type)

    def test_014_close_in_play_page_sport_tab(self):
        """
        DESCRIPTION: Close 'In-Play' page <Sport> tab
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state(state_name='Tennis')

    def test_015_trigger_primary_market_suspension(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: marketStatusCode="S" for 'Primary market' market type
        """
        self.test_005_trigger_primary_market_suspension()

    def test_016_open_in_play_page_sport_tab_and_verify_event_outcomes(self, sorting_type=live_now_type, is_enabled=False):
        """
        DESCRIPTION: Open 'In-Play' page <Sport> tab, find the event and verify its outcomes
        EXPECTED: All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled on
        EXPECTED: Football In-Play page but still displaying the prices
        """
        self.test_001_navigate_to_in_play_landing_page()
        self.test_002_select_sport_from_sports_ribbon()
        self.test_003_choose_tab_sorting_type(sorting_type=sorting_type)

        self.verify_price_buttons_state(section_name=self.section_name,
                                        event_id=self.eventID,
                                        expected_result=is_enabled,
                                        inplay_section=sorting_type,
                                        level='market')

    def test_017_close_in_play_page_sport_tab(self):
        """
        DESCRIPTION: Close 'In-Play' page <Sport> tab
        """
        self.test_014_close_in_play_page_sport_tab()

    def test_018_trigger_primary_market_activation(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: marketStatusCode="A" for '<Primary market>' market type
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)

    def test_019_open_in_play_page_sport_tab_and_verify_event_outcomes(self, sorting_type=live_now_type):
        """
        DESCRIPTION: Open 'In-Play' page <Sport> tab, find the event and verify its outcomes
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        self.test_016_open_in_play_page_sport_tab_and_verify_event_outcomes(sorting_type=sorting_type, is_enabled=True)

    def test_020_choose_upcoming_sorting_type(self):
        """
        DESCRIPTION: Choose **'Upcoming' **sorting type
        EXPECTED: **For desktop view:**
        EXPECTED: Click on **'Upcoming'** tab sorting type
        """
        self.test_003_choose_tab_sorting_type(sorting_type=self.upcoming_type)

    def test_021_repeat_steps_4_19(self):
        """
        DESCRIPTION: Repeat steps 4-19
        """
        self.test_004_find_an_event_with_price_odds_buttons_displaying_prices(sorting_type=self.upcoming_type)
        self.test_005_trigger_primary_market_suspension()
        self.test_006_verify_outcomes_for_the_event(sorting_type=self.upcoming_type)
        self.test_007_trigger_primary_market_activation(sorting_type=self.upcoming_type)
        self.test_008_collapse_section_where_this_event_belongs_to(sorting_type=self.upcoming_type)
        self.test_009_trigger_primary_market_suspension()
        self.test_010_expand_section_with_the_event_and_verify_its_outcomes(sorting_type=self.upcoming_type)
        self.test_011_collapse_section()
        self.test_012_trigger_primary_market_activation()
        self.test_013_expand_section_and_verify_outcomes_for_the_event(sorting_type=self.upcoming_type)
        self.test_015_trigger_primary_market_suspension()
        self.test_016_open_in_play_page_sport_tab_and_verify_event_outcomes(sorting_type=self.upcoming_type)
        self.test_017_close_in_play_page_sport_tab()
        self.test_018_trigger_primary_market_activation()
        self.test_019_open_in_play_page_sport_tab_and_verify_event_outcomes(sorting_type=self.upcoming_type)
