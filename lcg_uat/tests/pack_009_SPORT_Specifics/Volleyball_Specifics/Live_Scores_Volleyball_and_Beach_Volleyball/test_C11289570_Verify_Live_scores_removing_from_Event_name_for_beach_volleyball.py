from time import sleep

import pytest
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  # can't change change_is_off_flag on prod endpoints
@pytest.mark.sports
@pytest.mark.beach_volleyball
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
@vtest
class Test_C11289570_Verify_Live_scores_removing_from_Event_name_for_beach_volleyball(BaseFeaturedTest, BaseBetSlipTest,
                                                                                      BaseFallbackScoreboardTest):
    """
    TR_ID: C11289570
    NAME: Verify Live scores removing from Event name for beach volleyball
    DESCRIPTION: This test case verifies BIP scores in Event Name are replaced to ''v'' for Volleyball events on Front End on different pages
    PRECONDITIONS: 1. In order to get events with Scorers use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN, Ukr)
    PRECONDITIONS: 2. OB tool:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    """
    keep_browser_open = True
    score = {'current': '25-18', 'set': '(2):(0)'}
    events_from_hours_delta = -15
    sport_name = vec.siteserve.BEACH_VOLLEYBALL.upper()
    bet_type = vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE

    def get_accordion_name_for_event_from_ss(self, event: dict, **kwargs) -> str:
        """
        Gets league name from event response
        :param event - event response
        :param kwargs: in_play_tab_slp - In Play tab on SLP (Sport Landing Page,
        :param kwargs: in_play_tab_home_page - In Play tab on Homepage
        :param kwargs: live_stream_tab_homepage - Live Stream tab on Homepage
        :param kwargs: in_play_page_sport_tab - In Play page sport tab (e.g.: Football, Cricket, etc.)
        :param kwargs: in_play_page_watch_live - In Play page Watch Live tab
        :param kwargs: in_play_module_slp - In Play Module on SLP
        :param kwargs: in_play_module_homepage - In Play Module on Homepage Featured/Highlights tab
        :return: League name
        """
        in_play_tab_slp = kwargs.get('in_play_tab_slp')
        in_play_tab_home_page = kwargs.get('in_play_tab_home_page')
        live_stream_tab_homepage = kwargs.get('live_stream_tab_homepage')
        in_play_page_watch_live = kwargs.get('in_play_page_watch_live')
        in_play_page_sport_tab = kwargs.get('in_play_page_sport_tab')
        in_play_module_slp = kwargs.get('in_play_module_slp')
        in_play_module_homepage = kwargs.get('in_play_module_homepage')
        prematch = not any((in_play_tab_slp, in_play_tab_home_page, live_stream_tab_homepage, in_play_page_sport_tab,
                            in_play_page_watch_live, in_play_module_slp, in_play_module_homepage))
        type_name = event['event']['typeName']
        category_code = event['event']['categoryCode'].title().replace('_', ' ')
        class_name = event['event']['className'].replace(category_code, '', 1).lstrip()

        if prematch:
            league_name = f'{class_name.replace(category_code, "").lstrip().upper()} - {type_name.upper()}'
            return league_name

        if self.brand != 'ladbrokes':
            if self.device_type != 'desktop':
                if any((in_play_page_watch_live, in_play_tab_home_page, live_stream_tab_homepage, in_play_module_slp)):
                    league_name = type_name
                elif in_play_tab_slp or in_play_page_sport_tab:
                    league_name = type_name.upper()
                elif in_play_module_homepage:
                    league_name = category_code
                else:
                    league_name = type_name
            else:
                if any((in_play_page_watch_live,)):
                    league_name = type_name.upper()
                elif any((in_play_page_sport_tab, in_play_tab_home_page, in_play_tab_slp)):
                    league_name = f'{category_code} - {type_name}'.upper()
                else:
                    league_name = type_name
        else:
            if self.device_type != 'desktop':
                if any((in_play_page_watch_live, in_play_page_sport_tab, in_play_tab_home_page, live_stream_tab_homepage,
                        in_play_module_slp, in_play_tab_slp)):
                    league_name = type_name.upper()
                elif in_play_module_homepage:
                    league_name = category_code.upper()
                else:
                    league_name = type_name.upper()
            else:
                if any((in_play_page_watch_live, )):
                    league_name = type_name
                elif any((in_play_tab_slp, in_play_page_sport_tab, in_play_tab_home_page, live_stream_tab_homepage)):
                    league_name = f'{category_code} - {type_name}'.upper()
                else:
                    league_name = type_name

        return league_name.strip()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test live event Beach Volleyball
        """
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.beach_volleyball_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.beach_volleyball_config.category_id)

        event_params = self.ob_config.add_beach_volleyball_event_to_austrian_cup(score=self.score, is_live=True,
                                                                                 img_stream=True)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self.__class__.eventID = event_params.event_id
        self.__class__.marketID = self.ob_config.market_ids.get(event_params.event_id).get('match_betting')
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.team1 = event_params.team1
        type_id = self.ob_config.backend.ti.beach_volleyball.beach_volleyball_austria.austrian_cup_womans.type_id
        event = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID, query_builder=self.ss_query_builder)

        self.__class__.league_name = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                               in_play_page_watch_live=True)

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=type_id, module_time_from_hours_delta=self.events_from_hours_delta,
            events_time_from_hours_delta=self.events_from_hours_delta, show_all_events=True)['title'].upper()

    def test_001_go_to_oxygen_and_check_event_name_displaying_on_page_in_play(self):
        """
        DESCRIPTION: Go to Oxygen and check event name displaying on pages:
        DESCRIPTION: |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
        DESCRIPTION: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
        EXPECTED: '(2) 12-5 (0)' should be replaced on 'v'
        """
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.beach_volleyball.category_id)

        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name}" league')
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
        EXPECTED: '(2) 12-5 (0)' should be replaced on 'v'
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/live-stream')
            self.site.wait_content_state(state_name='homepage')
            module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream)
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.beach_volleyball.category_id)

            sections = self.site.home.get_module_content(module_name=module_name).live_now.items_as_ordered_dict
        else:
            self.navigate_to_page(name='live-stream')
            self.site.wait_content_state(state_name='LiveStream')
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.beach_volleyball.category_id)

            sections = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sports sections found')
        section = sections.get(self.sport_name)
        self.assertTrue(section, msg=f'"{self.sport_name}" section not found')
        section.expand()
        leagues = section.items_as_ordered_dict
        self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
        league = leagues.get(self.league_name)
        self.assertTrue(league, msg=f'"{self.league_name}" league not found')
        events = league.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found')
        actual_event = events.get(self.event_name)
        self.assertTrue(actual_event, msg=f'"{self.event_name}" event not found')
        self.assertEqual(actual_event.event_name, self.event_name,
                         msg=f'\nActual event name: "{actual_event.event_name}"'
                             f'\nis not as expected: "{self.event_name}"')

    def test_003_featured_module_page(self):
        """
        DESCRIPTION: Featured (created by type id)
        DESCRIPTION: |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
        DESCRIPTION: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
        EXPECTED: Event name should be:
        EXPECTED: '(2) 12-5 (0)' should be replaced on 'v'
        """
        # Changed order of steps because in step test_006_bet_history_page resulting of event is happening
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=False)  # necessary spike to see this event on Featured, otherwise it is always shown on In Play
        sleep(10)
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
        self.assertIn(self.event_name, events,
                      msg=f'"{self.event_name}" event not found among events: {list(events.keys())}')
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=True)

    def test_004_betslip_widget_added_via_deep_link(self):
        """
        DESCRIPTION: * Betslip slider/widget (adding via deep link too)
        EXPECTED: Event name should be:
        DESCRIPTION: |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
        DESCRIPTION: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
        EXPECTED: '(2) 12-5 (0)' should be replaced on 'v'
        """
        self.site.login(async_close_dialogs=False)
        self.open_betslip_with_selections(self.selection_ids[self.team1])
        sections = self.get_betslip_sections().Singles
        for actual_event in list(sections.values()):
            self.assertEqual(actual_event.event_name, self.event_name,
                             msg=f'\nActual event name: "{actual_event.event_name}"'
                                 f'\nis not as expected: "{self.event_name}"')

    def test_005_event_with_cashout_available(self):
        """
        DESCRIPTION: Cashout page
        DESCRIPTION: |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
        DESCRIPTION: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
        EXPECTED: '(2) 12-5 (0)' should be replaced on 'v'
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_cashout()
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=self.bet_type, event_names=self.event_name, number_of_bets=1)
        self.assertIn(self.event_name, bet_name, msg=f'"{self.event_name}" can not be found')

    def test_006_bet_history_page(self):
        """
        DESCRIPTION: * Settled Bets/Open bets
        DESCRIPTION: |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
        DESCRIPTION: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
        EXPECTED: '(2) 12-5 (0)' should be replaced on 'v'
        """
        self.result_event(selection_ids=self.selection_ids[self.team1], market_id=self.marketID, event_id=self.eventID)
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')
        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=self.bet_type, event_names=self.event_name, number_of_bets=1)
        self.assertIn(self.event_name, bet_name, msg=f'"{self.event_name}" can not be found')
