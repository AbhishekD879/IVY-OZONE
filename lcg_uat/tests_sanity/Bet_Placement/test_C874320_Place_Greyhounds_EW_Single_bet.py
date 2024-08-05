import re

import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.each_way
@pytest.mark.safari
@pytest.mark.sanity
@vtest
class Test_C874320_Place_Greyhounds_EW_Single_bet(BaseBetSlipTest, BaseGreyhound):
    """
    TR_ID: C874320
    NAME: Place Greyhounds EW Single bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single E/W bet on Greyhounds
    DESCRIPTION: Note: according to BMA-47237 event time is displayed twice in My Bets section
    """
    keep_browser_open = True
    expected_currency = '£'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Login to Oxygen
        PRECONDITIONS: **Mobile Only** Quick Bet should be switch off for your user:
        PRECONDITIONS: **CORAL** Account Menu ->Settings ->Betting Settings ->Allow Quick Bet (switch off)
        PRECONDITIONS: **Ladbrokes** Account Menu ->Settings ->Quick Bet (switch off)
        """
        if tests.settings.backend_env != 'prod':
            self.__class__.expected_ew_terms = self.ew_terms
            event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1,
                                                                        ew_terms=self.expected_ew_terms)
            self.__class__.event_id = event_params.event_id
            self.__class__.meeting_name = self.greyhound_autotest_name_pattern if self.brand == 'ladbrokes'\
                else self.greyhound_autotest_name_pattern.upper()
            self.__class__.event_off_time = event_params.event_off_time
            self.__class__.each_way_coef = int(self.expected_ew_terms['ew_fac_num']) / int(self.expected_ew_terms['ew_fac_den'])
        else:
            ew_available_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE), \
                simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE')
            event_ew_available = \
                self.get_active_events_for_category(category_id=self.ob_config.greyhound_racing_config.category_id,
                                                    additional_filters=ew_available_filter)[0]
            self.__class__.event_id = event_ew_available['event']['id']
            market = next((market['market'] for market in event_ew_available['event']['children']), None)
            if not market:
                raise SiteServeException('There are not available outcomes')
            self.__class__.expected_ew_terms = {"ew_places": market["eachWayPlaces"],
                                                "ew_fac_num": market["eachWayFactorNum"],
                                                "ew_fac_den": market["eachWayFactorDen"]}
            self.__class__.each_way_coef = int(market['eachWayFactorNum']) / int(market['eachWayFactorDen'])
            self.__class__.meeting_name = event_ew_available['event']['typeName'] if self.brand == 'ladbrokes' \
                else event_ew_available['event']['typeName'].upper()
            event_name = event_ew_available['event']['name']
            search = re.search(r'^(\d{1,2}:\d{2})(?:\s)', event_name)
            self.__class__.event_off_time = search.group(1) if search else None
            # events are sorted on UI by start time, but event time shown on UI is taken from event name
            if not self.event_off_time:
                raise SiteServeException(f'Cannot detect UI start time from name "{event_name}" for event "{self.event_id}"')
        self._logger.info(f'*** Found Event "{self.event_id}" "{self.meeting_name}" with time "{self.event_off_time}"')
        self.site.login()

        self.site.toggle_quick_bet()

    def test_001_navigate_to_greyhounds_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds Page
        EXPECTED: Greyhounds Page is loaded
        """
        if self.brand != 'ladbrokes':
            self.navigate_to_page(name='greyhounds')
            self.site.wait_content_state('Greyhounds')
        else:
            self.navigate_to_page(name='greyhound-racing')
            self.site.wait_content_state('Greyhoundracing')

    def test_002_click_on_one_event_from_all_races_section(self):
        """
        DESCRIPTION: Click on one event from All Races section
        EXPECTED: The event page is loaded
        """
        self.site.greyhound.tabs_menu.click_button(vec.sb.TABS_NAME_TODAY.upper())
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')

    def test_003_add_one_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add one selection to bet slip
        EXPECTED: The selection is added to bet slip
        """
        event_name = self.site.greyhound_event_details.event_title
        self._logger.debug(f'*** Race event name: "{event_name}"')
        sections = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertIn(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB, markets,
                      msg=f'"{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}" market is not in "{markets}" markets')

        w_or_ew_section = markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        outcomes = w_or_ew_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')

        outcome_name, outcome = list(outcomes.items())[0]
        self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Racing outcome "{outcome_name}" is disabled')
        outcome.bet_button.click()
        if self.device_type == 'mobile':
            if self.site.is_cookie_banner_shown():
                self.site.cookie_banner.ok_button.click()
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.__class__.expected_betslip_counter_value += 1
        self.site.open_betslip()

    def test_004_add_a_stake_eg_1_tick_the_ew_checkbox_and_then_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£), tick the "E/W" checkbox and then click on 'Place Bet' button
        EXPECTED: The bet is successfully placed
        """
        section = self.get_betslip_sections().Singles
        _, selection = list(section.items())[0]
        selection.amount_form.input.value = self.bet_amount
        self.assertTrue(selection.has_each_way_checkbox(), msg='Each way checkbox is absent.')
        selection.each_way_checkbox.click()
        # self.__class__.betslip_bet_type = section.name
        self.__class__.betslip_odds = selection.odds
        self.__class__.betslip_selection_name = selection.outcome_name
        self.__class__.betslip_market_name = selection.market_name
        self.__class__.betslip_event_name = selection.event_name
        self.__class__.betslip_estimated_returns = selection.est_returns
        self.__class__.betslip_total_stake = self.site.betslip.total_stake
        self.__class__.betslip_currency = self.site.betslip.total_stake_currency
        place_bet_button = self.get_betslip_content().bet_now_button

        self.assertTrue(self.site.betslip.has_bet_now_button(), msg='Place Bet button is not present.')
        self.assertTrue(place_bet_button.is_displayed(), msg='Place Bet button is not displayed.')
        self.assertTrue(place_bet_button.is_enabled(), msg='Place Bet button is not enabled.')
        place_bet_button.click()

        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed.')

    def test_005_verify_the_bet_confirmation_eg_bet_receipt_details(self):
        """
        DESCRIPTION: Verify the Bet Confirmation (e.g. bet receipt details)
        EXPECTED: Correct information is displayed in bet receipt:
        EXPECTED: - sign ![](index.php?/attachments/get/19830152)
        EXPECTED: with text 'Bet Placed Successfully' at the left side and date/time when the bet was placed at the right side - VANILLA ONLY
        EXPECTED: - 'Your Bets: (1)' text - VANILLA ONLY
        EXPECTED: - Bet Type ('Single') and odds (@1/4 or @SP)
        EXPECTED: - Bet ID
        EXPECTED: - Selection name
        EXPECTED: - Market name
        EXPECTED: - Event name
        EXPECTED: - Each Way conditions
        EXPECTED: - Stake
        EXPECTED: - Total Stake
        EXPECTED: - Est. Returns (CORAL)/Potential Returns(LADBROKES) (N/A if SP price)
        EXPECTED: - Currency is correct
        EXPECTED: - 'REUSE SELECTIONS' and 'GO BETTING' buttons
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/19764606)
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/19764607)
        """
        self.__class__.bet_receipt = self.site.bet_receipt
        bet_receipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found.')
        single_section = bet_receipt_sections.get(vec.betslip.SINGLE)
        self.assertTrue(single_section, msg='No Single sections found.')
        selections = single_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No stakes found in singles section.')
        _, selection = list(selections.items())[0]

        # removed single for bet recipet
        # if self.brand != 'ladbrokes':
        #     bet_type = single_section.bet_type
        #     self.assertEqual(bet_type, self.betslip_bet_type,
        #                      msg=f'Bet type is not the same as on betslip "{self.betslip_bet_type}" and is "{bet_type}"')
        # else:
        #     bet_type = selection.type_name.name
        #     self.assertIn(bet_type, self.betslip_bet_type,
        #                   msg=f'Bet type is not the same as on betslip "{self.betslip_bet_type}" and is "{bet_type}"')
        ew_terms = selection.ew_terms.split('\n')[0]
        self.check_each_way_terms_format(each_way_terms=ew_terms, format=vec.regex.EXPECTED_EACH_WAY_FORMAT_BET_RECEIPT)
        self.check_each_way_terms_correctness(each_way_terms=ew_terms,
                                              expected_each_way_terms=self.expected_ew_terms, betslip=True)
        odds = selection.odds
        self.assertEqual(odds, self.betslip_odds,
                         msg=f'Odds value is not the same as on betslip "{self.betslip_odds}" and is "{odds}".')
        self.assertTrue(selection.bet_id, msg='Bet ID is not displayed.')
        selection_name = selection.name
        self.assertEqual(selection_name, self.betslip_selection_name,
                         msg=f'Selection name is not the same as on betslip "{self.betslip_selection_name}" and is "{selection_name}".')
        market_name = selection.event_market
        self.assertEqual(market_name, self.betslip_market_name,
                         msg=f'Market name is not the same as on betslip "{self.betslip_market_name}" and is "{market_name}".')
        event_name = selection.event_name
        self.assertEqual(event_name, self.betslip_event_name,
                         msg=f'Event name is not the same as on betslip "{self.betslip_event_name}" and is "{event_name}".')
        stake = selection.total_stake
        self.assertEqual(stake, self.betslip_total_stake, msg=f'Stake is not displayed.')
        total_stake = self.bet_receipt.footer.total_stake
        self.assertEqual(total_stake, self.betslip_total_stake,
                         msg=f'Total stake is not the same as on betslip "{self.betslip_total_stake}" and is "{total_stake}".')
        est_returns = self.bet_receipt.footer.total_estimate_returns
        self.verify_estimated_returns(odds=odds, bet_amount=self.bet_amount, est_returns=est_returns, each_way_coef=self.each_way_coef)

        currency = selection.stake_currency
        self.assertEqual(currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{currency}" instead.')
        self.assertTrue(self.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Bet receipt has no "Reuse Selection" button.')
        self.assertTrue(self.bet_receipt.footer.has_done_button(),
                        msg='Bet receipt has no "Done" button.')

    def test_006_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on 'Go Betting' button
        EXPECTED: The customer is redirected to Greyhounds Page - User is redirected to homepage because selection was added via deep link
        """
        self.bet_receipt.footer.done_button.click()
        self.site.wait_content_state('GreyHoundEventDetails')

    def test_007_click_on_my_bets_button_from_the_header_and_select_open_bets_tab(self):
        """
        DESCRIPTION: Click on My Bets button from the header and select 'Open Bets' tab
        """
        self.site.open_my_bets_open_bets()

    def test_008_check_that_the_bet_is_displayed_in_open_bets(self):
        """
        DESCRIPTION: Check that the bet is displayed in 'Open Bets'
        EXPECTED: Correct information is displayed in bet history:
        EXPECTED: - Bet Type (SINGLE(EACH WAY))
        EXPECTED: - Selection name with odds (@1/4)
        EXPECTED: - Market name
        EXPECTED: - Event name and event off time
        EXPECTED: - Event time and date
        EXPECTED: - Sign that redirects to the event detail page ![](index.php?/attachments/get/19830149)
        EXPECTED: - Unit Stake
        EXPECTED: - Total Stake
        EXPECTED: - Est. Returns (CORAL)/Potential Returns(LADBROKES) (N/A if SP price)
        EXPECTED: - Currency is correct
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/19830151)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/19830150)
        """
        bet_type = vec.bet_history.SINGLE_EACH_WAY_BET_TYPE
        self.__class__.bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, number_of_bets=1)

        actual_bet_type = self.bet.bet_type
        self.assertIn(actual_bet_type, bet_type,
                      msg=f'Bet Type is not the same as expected "{bet_type}" and equals "{actual_bet_type}". ')
        bet_legs = self.bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No bet legs found for bet: {self.bet_name}')
        betleg_name, betleg = list(bet_legs.items())[0]
        selection_name = betleg.outcome_name
        self.assertEqual(selection_name, self.betslip_selection_name,
                         msg=f'Selection name is not the same as on betslip "{self.betslip_selection_name}" and is "{selection_name}".')
        odds = betleg.odds_value
        self.assertEqual(odds, self.betslip_odds,
                         msg=f'Odds value is not the same as on betslip "{self.betslip_odds}" and is "{odds}".')
        market_name = betleg.market_name
        self.assertIn(self.betslip_market_name, market_name,
                      msg=f'Market name is not the same as on betslip "{self.betslip_market_name}" and is "{market_name}".')
        event_name = self.bet.event_name
        self.assertIn(event_name, self.betslip_event_name,
                      msg=f'Event name is not the same as on betslip "{self.betslip_event_name}" and is "{event_name}".')
        self.assertTrue(betleg.event_start_time.name, msg='Event start time is not displayed.')
        self.assertTrue(self.bet.unit_stake, msg='Unit stake is not displayed.')
        total_stake = self.bet.stake.stake_value
        self.assertEqual(total_stake, self.betslip_total_stake,
                         msg=f'Total stake is not the same as on betslip "{self.betslip_total_stake}" and is "{total_stake}".')
        est_returns = self.bet.est_returns.stake_value
        self.verify_estimated_returns(odds=odds, bet_amount=self.bet_amount, est_returns=est_returns, each_way_coef=self.each_way_coef)
        currency = self.bet.stake.currency
        self.assertEqual(currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{currency}" instead.')
