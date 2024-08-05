import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089594_Verify_MS_on_Competitions_Tab_for_Ice_Hockey(BaseSportTest, BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C60089594
    NAME: Verify MS on Competitions Tab for Ice Hockey
    DESCRIPTION: This testcase verifies  the behavior of 'Market Selector' dropdown list
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|60 Minute betting|,|Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|Money Line (WW)|- Money Line
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- 60 Minute Betting
    PRECONDITIONS: *|Puck Line (Handicap)| - "Puck Line"
    PRECONDITIONS: *|Total Goals 2-way (Over/Under)| - "Total Goals 2-way"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    preplay_list = []
    inplay_list = []
    event_markets = [
        ('sixty_minutes_betting',),
        ('puck_line',),
        ('total_goals_2_way',)
    ]
    multiple = False
    status = False
    number_of_events = 0

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the IceHockey Landing Page -> 'Click on Competition Tab'
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for IceHockey sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        if tests.settings.backend_env != 'prod':
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.backend.ti.ice_hockey.category_id,
                disp_sort_names='HH,WH,MR,HL',
                primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')
            for i in range(0, 2):
                self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)

        self.site.login()
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.ice_hockey_config.category_id)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Ice Hockey')
        self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type == 'desktop':
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                sleep(2)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        else:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            sleep(2)
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line,
                         msg=f'Actual market value: "{selected_value.upper()}" is not same as'
                             f'Expected market value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line}"')

    def test_002_verify_the_competition_page(self):
        """
        DESCRIPTION: Verify the Competition page
        EXPECTED: One of the below market will be selected by default according to which events will be displayed with odds value.
        EXPECTED: • Puck Line
        EXPECTED: • 60 Minute Betting
        EXPECTED: • Total Goals 2-way
        EXPECTED: >If a market is only for Preplay event then only Preplay events will be displayed with odds
        EXPECTED: >If a market is only for Preplay event then only Preplay events will be displayed with odds
        EXPECTED: > If a market is having both Preplay and Inplay event then both inplay and Preplay events will be displayed with odds
        """
        leagues = list(
            self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(leagues, msg='Leagues not found')

        for league in leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                is_live = event_template.is_live_now_event
                self.inplay_list.append(is_live) if is_live else self.preplay_list.append(is_live)
                odds = list(event_template.items_as_ordered_dict.values())
                for odd in odds:
                    self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                self.assertTrue(event_template.event_name,
                                msg=' "Event Name" not displayed')
                if is_live:
                    self._logger.info(f'{event_template.event_name} is live event')
                else:
                    self.assertTrue(event_template.event_time,
                                    msg=' "Event time" not displayed')
                if event_template.has_markets():
                    self._logger.info(f'{event_template.event_name} has more markets')
                else:
                    self._logger.info(f'{event_template.event_name} has no more markets')

        if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
            self._logger.info(msg=f'Only "In-Play" events are available ')
        elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
            self._logger.info(msg=f'Only "Pre-Play" events are available ')
        else:
            self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_003_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets:
        EXPECTED: . Money Line
        EXPECTED: • Puck Line
        EXPECTED: • 60 Minute Betting
        EXPECTED: • Total Goals 2-way
        """
        self.__class__.actual_markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if len(self.actual_markets_list) == 1:
            self.__class__.actual_markets_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        self.assertTrue(self.actual_markets_list, msg=f'"Market Selector" dropdown list not opened')
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.sixty_minutes_betting,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_2_way]
        if tests.settings.backend_env != 'prod':
            self.assertListEqual(self.actual_markets_list, self.expected_list,
                                 msg=f'Actual list : "{self.actual_markets_list}" is not same as '
                                     f'Expected list : "{self.expected_list}"')
        else:
            for market in self.actual_markets_list:
                self.assertIn(market, self.expected_list,
                              msg=f'Actual list : "{self.actual_markets_list}" is not same as '
                                  f'Expected list : "{self.expected_list}"')

    def test_004_select_money_line_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Money Line' in the 'Market Selector' dropdown list
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • Money Line (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        # Covered in step 2

    def test_005_repeat_step_3_for_the_following_markets_puck_line_preplay_and_inplay_market_60_minute_betting_preplay_and_inplay_market_total_goals_2_way_preplay_and_inplay_market(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Puck Line (Preplay and Inplay market)
        DESCRIPTION: • 60 Minute Betting (Preplay and Inplay market)
        DESCRIPTION: • Total Goals 2-way (Preplay and Inplay market)
        """
        self.site.contents.scroll_to_top()
        if vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line in self.actual_markets_list:
            try:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    'Puck Line').click()
            except Exception:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    'Puck Line').click()
            self.test_002_verify_the_competition_page()
            self.site.contents.scroll_to_top()
        if vec.siteserve.EXPECTED_MARKETS_NAMES.sixty_minutes_betting in self.actual_markets_list:
            try:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    '60 Minutes Betting').click()
            except Exception:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    '60 Minutes Betting').click()
            self.test_002_verify_the_competition_page()
            self.site.contents.scroll_to_top()
        if vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_2_way in self.actual_markets_list:
            try:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    'Total Goals 2-way').click()
            except Exception:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    'Total Goals 2-way').click()
            self.test_002_verify_the_competition_page()

    def test_006_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_money_line_puck_line_60_minute_betting_total_goals_2_way(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Puck Line
        DESCRIPTION: • 60 Minute Betting
        DESCRIPTION: • Total Goals 2-way
        EXPECTED: Bet should be placed successfully
        """
        for market in self.expected_list:
            if market in self.actual_markets_list or tests.settings.backend_env != 'prod':
                self.site.sports_page.tab_content.dropdown_market_selector.scroll_to()
                if not self.dropdown.is_expanded():
                    self.dropdown.click()
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
                self.site.wait_content_state('ice-hockey')
                self.__class__.multiple = False
                leagues = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
                self.assertTrue(leagues, msg='"Leagues" are not available')
                for league in leagues:
                    events = league.items_as_ordered_dict.values()
                    self.assertTrue(events, msg='"Events" are not available')
                    for event in events:
                        self.site.wait_content_state_changed()
                        bet_buttons = list(event.template.get_available_prices().values())
                        bet_buttons[0].scroll_to()
                        bet_buttons[0].click()
                        if self.device_type == 'desktop':
                            sleep(2)
                            bet_buttons[1].click()
                            if not bet_buttons[1].is_selected():
                                sleep(2)
                                bet_buttons[1].click()
                        self.__class__.number_of_events = self.number_of_events + 1
                        if not self.multiple:
                            if self.device_type == 'mobile':
                                self.site.wait_for_quick_bet_panel(timeout=10)
                                self.site.quick_bet_panel.selection.content.amount_form.input.value = 0.03
                                self.site.quick_bet_panel.place_bet.click()
                                self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(timeout=10),
                                                msg='Bet Receipt is not shown')
                                self.site.quick_bet_panel.header.close_button.click()
                                self.site.wait_content_state_changed(timeout=15)
                                bet_buttons[1].click()
                                self.site.wait_for_quick_bet_panel(timeout=10)
                                self.site.quick_bet_panel.add_to_betslip_button.click()
                                self.site.wait_content_state_changed()
                                self.site.open_betslip()
                                self.place_single_bet()
                                self.check_bet_receipt_is_displayed()
                                self.site.bet_receipt.close_button.click()
                                self.__class__.multiple = True
                                sleep(2)
                                bet_buttons[0].scroll_to()
                                bet_buttons[0].click()
                                self.site.wait_for_quick_bet_panel(timeout=10)
                                self.site.quick_bet_panel.add_to_betslip_button.click()
                                self.site.wait_content_state_changed()
                            else:
                                singles_section = self.get_betslip_sections().Singles
                                stake_name, stake = list(singles_section.items())[0]
                                self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts={stake_name: 0.03})
                                self.get_betslip_content().bet_now_button.click()
                                self.check_bet_receipt_is_displayed()
                                self.site.wait_content_state_changed(timeout=15)
                                self.__class__.multiple = True
                                bet_buttons[0].click()
                        else:
                            self.site.open_betslip()
                            try:
                                singles_section = self.get_betslip_sections(multiples=True).Multiples
                            except Exception:
                                self.site.close_betslip()
                                bet_buttons[1].click()
                                self.site.open_betslip()
                                singles_section = self.get_betslip_sections(multiples=True).Multiples
                            stake_name, stake = list(singles_section.items())[0]
                            self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts={stake_name: 0.03})
                            self.get_betslip_content().bet_now_button.click()
                            self.check_bet_receipt_is_displayed()
                            self.site.bet_receipt.close_button.click()
                            self.__class__.status = True
                            break
                    if self.status:
                        betslip_counter = int(self.site.header.bet_slip_counter.counter_value)
                        if betslip_counter > 0:
                            self.site.open_betslip()
                            self.clear_betslip()
                        break
                if not self.number_of_events >= 2:
                    raise Exception("Multiple betplacement not happened as the number of events are less than 2")
