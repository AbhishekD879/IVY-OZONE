import pytest
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Live scores cannot be automated on hl and prod
# @pytest.mark.hl
@pytest.mark.sports
@pytest.mark.handball
@pytest.mark.module_ribbon
@pytest.mark.cms
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.in_play
@pytest.mark.featured
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@pytest.mark.live_scores
# todo VOL-5713 [tst] Adapt pack_009_SPORT_Specifics > Scores
@vtest
class Test_C717555_Verify_Live_scores_removing_from_Event_name_for_Handball(BaseFeaturedTest, BaseBetSlipTest, BaseFallbackScoreboardTest):
    """
    TR_ID: C717555
    NAME: Verify Live scores removing from Event name for Handball
    DESCRIPTION: This test case verifies BIP scores in Event Name are replaced to ''v'' for Handball events on Front End
    PRECONDITIONS: 1. In order to get events with Scorers use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN, Ukr)
    PRECONDITIONS: 2. OB tool: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    """
    keep_browser_open = True
    score = {'current': '25-18'}
    events_from_hours_delta = -15
    bet_type = vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE.upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Go to OB and create Handball live event with name:
        DESCRIPTION: |Team A Name| ScoreA-ScoreB |Team B Name|
        DESCRIPTION: (e.g. |Saint Raphael| 25-18 |Selestat|(BG)|
        EXPECTED: Event is successfully created
        """
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.handball_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.handball_config.category_id)

        event_params = self.ob_config.add_handball_event_to_croatian_premijer_liga(
            score=self.score, is_live=True, img_stream=True)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self.__class__.eventID = event_params.event_id
        event = self.ss_req.ss_event_to_outcome_for_event(event_id=event_params.event_id,
                                                          query_builder=self.ss_query_builder)
        self.__class__.marketID = self.ob_config.market_ids.get(event_params.event_id).get('match_betting')
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.team1 = event_params.team1
        event_params = self.ob_config.add_handball_event_to_croatian_premijer_liga(
            score=self.score, img_stream=True)
        self.__class__.event_name2 = event_params.team1 + ' v ' + event_params.team2
        self.__class__.type_id = self.ob_config.backend.ti.handball.handball_croatia.dukat_premijer_liga.type_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=self.type_id, events_time_from_hours_delta=self.events_from_hours_delta,
            module_time_from_hours_delta=self.events_from_hours_delta, show_all_events=True)['title'].upper()

        sport_name_raw = self.get_sport_name_for_event(event=event[0])
        self.__class__.sport_name = sport_name_raw.title() if self.brand == 'ladbrokes' else sport_name_raw.upper()

        self.__class__.league_name_in_play_watch_live = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                  in_play_page_watch_live=True)

    def test_001_go_to_oxygen_and_check_event_name_displaying_on_page_in_play(self):
        """
        DESCRIPTION: Go to Oxygen and check event name displaying on pages:
        DESCRIPTION: * In Play page/tab/widget ( all sports filter and handball sports filter)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: '25-18' should be replaced on 'v'
        """
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(vec.sb.WATCH_LIVE_LABEL)

        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.handball.category_id)

        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_in_play_watch_live)
        self.assertTrue(events, msg=f'No events found')
        actual_event = events.get(self.event_name)
        self.assertTrue(actual_event, msg=f'"{self.event_name}" event not found among: {list(events.keys())}')
        self.assertEqual(actual_event.event_name, self.event_name,
                         msg=f'\nActual event name: "{actual_event.event_name}"'
                             f'\nis not as expected: "{self.event_name}"')

    def test_002_live_stream_page(self):
        """
        DESCRIPTION: Live Stream page/widget (if live stream is available for event)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: '25-18' should be replaced on 'v'
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/live-stream')
            self.site.wait_content_state(state_name='homepage')
            module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream)
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.handball.category_id)

            sections = self.site.home.get_module_content(module_name=module_name).live_now.items_as_ordered_dict
        else:
            self.navigate_to_page(name='live-stream')
            self.site.wait_content_state(state_name='LiveStream')
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.handball.category_id)

            sections = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sports sections found')
        section = sections.get(self.sport_name.upper())

        self.assertTrue(section, msg=f'"{self.sport_name.upper()}" section not found')
        section.expand()
        leagues = section.items_as_ordered_dict
        self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
        league = leagues.get(self.league_name_in_play_watch_live)
        self.assertTrue(league, msg=f'"{self.league_name_in_play_watch_live}" league not found')
        events = league.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found for "{self.league_name_in_play_watch_live}"')
        actual_event = events.get(self.event_name)
        self.assertTrue(actual_event, msg=f'"{self.event_name}" event not found among events "{events.keys()}"')
        self.assertEqual(actual_event.event_name, self.event_name,
                         msg=f'\nActual event name: "{actual_event.event_name}"'
                             f'\nis not as expected: "{self.event_name}"')

    def test_003_betslip(self):
        """
        DESCRIPTION: * Betslip slider/widget (adding via deep link too)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: '25-18' should be replaced on 'v'
        """
        self.site.login()
        self.open_betslip_with_selections(self.selection_ids[self.team1])
        sections = self.get_betslip_sections().Singles
        for actual_event in list(sections.values()):
            self.assertEqual(actual_event.event_name, self.event_name,
                             msg=f'\nActual event name: "{actual_event.event_name}"'
                                 f'\nis not as expected: "{self.event_name}"')

    def test_004_event_with_cashout_available(self):
        """
        DESCRIPTION: Cashout page
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: '25-18' should be replaced on 'v'
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_cashout()
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=self.bet_type, event_names=self.event_name, number_of_bets=1)
        self.assertIn(self.event_name, bet_name, msg=f'"{self.event_name}" can not be found')

    def test_005_settled_bets_open_bets_page(self):
        """
        DESCRIPTION: * Settled Bets/Open bets
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: '25-18' should be replaced on 'v'
        """
        self.result_event(selection_ids=list(self.selection_ids.values()), market_id=self.marketID,
                          event_id=self.eventID)
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')
        wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict,
                        name='Settled bets to be displayed', timeout=5)
        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=self.bet_type, event_names=self.event_name, number_of_bets=1)
        self.assertIn(self.event_name, bet_name, msg=f'"{self.event_name}" can not be found')

    def test_006_featured_module_page(self):
        """
        DESCRIPTION: Featured (created by type id, selection id)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: '25-18' should be replaced on 'v'
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Home')
        self.wait_for_featured_module(name=self.module_name)
        module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        module_content = self.site.home.get_module_content(module_name=module_name)
        module_content.scroll_to()
        added_module = module_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(added_module, msg=f'"{self.module_name}" section cannot be found on Featured tab')
        try:
            events = added_module.items_as_ordered_dict
        except StaleElementReferenceException:
            module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            module_content = self.site.home.get_module_content(module_name=module_name)
            module_content.scroll_to()
            added_module = module_content.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertTrue(added_module, msg=f'"{self.module_name}" section cannot be found on Featured tab')
            events = added_module.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events for "{self.module_name}" section')
        self.assertIn(self.event_name2, list(events.keys()),
                      msg=f'"{self.event_name2}" event not found among events: {list(events.keys())}')
