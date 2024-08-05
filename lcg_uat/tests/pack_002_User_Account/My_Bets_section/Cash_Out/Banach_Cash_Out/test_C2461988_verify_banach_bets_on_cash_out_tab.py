import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from crlat_ob_client.utils.date_time import validate_time
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.build_your_bet
@pytest.mark.bet_placement
@pytest.mark.banach
@pytest.mark.currency
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
@pytest.mark.issue("https://jira.egalacoral.com/browse/BMA-55778")
class Test_C2461988_verify_banach_bets_on_cash_out_tab(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C2461988
    NAME: Verify Banach bets on 'Cash Out' tab
    DESCRIPTION: Test case verifies Banach bet display on Cash out
    PRECONDITIONS: Related to Full Cash out, Partial Cash out
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Cash-out tab:
    PRECONDITIONS: in Dev tools > Network find getBetDetails request
    PRECONDITIONS: User has placed Banach bet(s)
    """
    keep_browser_open = True
    proxy = None
    bet_amount = 0.5
    selection_names = []
    date_pattern_today = '%H:%M, Today'
    currency = '£'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Place Banach bet
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        byb_markets = self.cms_config.get_build_your_bet_markets()
        markets_list = [market['bybMarket'] for market in byb_markets]
        if self.expected_market_tabs.build_your_bet.title() and self.expected_market_sections.match_betting.title() \
                and self.expected_market_sections.both_teams_to_score.title() not in markets_list:
            raise CmsClientException(f'BYB Markets "{self.expected_market_tabs.build_your_bet.title()}" or'
                                     f'"{self.expected_market_sections.match_betting.title()}" or'
                                     f'"{self.expected_market_sections.both_teams_to_score.title()}" was not found')
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(
            self.expected_market_tabs.build_your_bet, timeout=5),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.bet_type = vec.bet_history.MY_BETS_SINGLE_BET_BUILDER_STAKE_TITLE

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'"{self.expected_market_sections.match_betting}" market does not exist')
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1
        selection_name = ''.join(match_betting_selection_name)
        self.__class__.selection_names.append(f'{self.expected_market_sections.match_betting.title()} '
                                              f'{selection_name}')

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score_market,
                        msg=f'"{self.expected_market_sections.both_teams_to_score}" market does not exist')
        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1
        team1 = ''.join(both_teams_to_score_names)
        both_teams_to_score_and_selection_name = f'{self.expected_market_sections.both_teams_to_score.title()} ' \
                                                 f'{team1}'.replace('  ', ' ')
        self.__class__.selection_names.append(both_teams_to_score_and_selection_name)

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='Build Your Bet Betslip not appears')
        self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)

        stake_section = self.site.byb_betslip_panel.selection.content
        self.__class__.odd_value = stake_section.odds
        self.site.byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=15),
                        msg='Build Your Bet Bet Receipt NOT displayed')
        self.__class__.est_returns = self.site.byb_bet_receipt_panel.selection.total_est_returns
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_byb_bet_receipt_panel(expected_result=False),
                         msg='Build Your Bet Bet Receipt still displayed')

    def test_001_navigate_to_my_bets_cashout(self):
        """
        DESCRIPTION: Navigate to My Bets > Cash-out and verify Banach bet details
        EXPECTED: Cash-out tab contains Banach bet with correct details of:
        EXPECTED:    - bet type Single
        EXPECTED:    - Selection names user has bet on, separated by comma, truncated into a few lines
        EXPECTED:    - Build Your Bet Coral/Bet Builder Ladbrokes text
        EXPECTED:    - Corresponding Event name which is redirecting users to corresponding Event Details Page
        EXPECTED:    - Event start date in DD MMM, hh:mm AM/PM (time only displayed for Today's events)
        EXPECTED:    - Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED:    - Odds
        EXPECTED:    - Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED:    - 'Cash Out <currency symbol> <value>' and 'Partial Cashout' buttons
        """
        self.site.open_my_bets_cashout()
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(bet_type=self.bet_type,
                                                                              event_names=self.event_name,
                                                                              number_of_bets=1)
        self.assertTrue(bet, msg=f'Event: "{self.event_name}" Single bet not found')

        # bet type Single
        self.assertEqual(bet.bet_type, self.bet_type,
                         msg=f'Actual bet type: "{bet.bet_type}", expected: "{self.bet_type}"')
        # Selection names user has bet on, separated by comma, truncated into a few lines
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet: "{bet_name}" leg found')
        bet_leg_name, bet_leg = list(bet_legs.items())[0]
        outcome_names = list(bet_leg.byb_selections.items_as_ordered_dict.keys())
        sorted_outcomes_names = sorted(outcome_names)
        market = sorted_outcomes_names[0]
        if 'Yes' in market:
            market = market.replace('Yes', '90 Minutes')
            sorted_outcomes_names[0] = market

        self.assertTrue(sorted_outcomes_names, msg=f'Selections names: "{sorted_outcomes_names}", is not displayed')
        # Build Your Bet text
        self.assertEqual(bet_leg.market_name, vec.yourcall.BUILD_YOUR_BET,
                         msg=f'Actual bet leg text: "{bet_leg.market_name}", expected: "{vec.yourcall.BUILD_YOUR_BET}"')
        # Corresponding Event name which is redirecting users to corresponding Event Details Page
        self.assertEqual(bet_leg.event_name, self.event_name,
                         msg=f'Actual event name: "{bet_leg.event_name}", expected: "{self.event_name}"')

        # Event start date in DD MMM, hh:mm AM/PM (time only displayed for Today's events)
        error_msg = f'Event start date: {bet_leg.event_time} does not match expected: "{self.event_card_future_time_format_pattern}"'
        try:
            result = validate_time(bet_leg.event_time, self.date_pattern_today)
        except Exception as e:
            result = validate_time(bet_leg.event_time, self.event_card_future_time_format_pattern)
            error_msg = e
        self.assertTrue(result, msg=error_msg)

        # Stake <currency symbol> <value> (e.g., £10.00)
        actual_stake = bet.stake.name.replace('\n', ' ').strip()
        stake_value = '{0:.2f}'.format(self.bet_amount)
        expected_stake = f'Stake:{self.currency}{stake_value}'
        self.assertEqual(actual_stake, expected_stake,
                         msg=f'Actual bet stake: "{actual_stake}", expected: "{expected_stake}"')

        # Odds
        self.assertEqual(bet_leg.odds_value, self.odd_value,
                         msg=f'Actual odds value: "{bet_leg.odds_value}", expected: "{self.odd_value}"')

        # Est. Returns <currency symbol> <value> (e.g., £30.00)
        actual_est_returns = bet.est_returns.stake_value
        self.verify_estimated_returns(est_returns=actual_est_returns, odds=bet_leg.odds_value, bet_amount=self.bet_amount)

        # 'Cash Out <currency symbol> <value>' and 'Partial Cashout' buttons
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(), msg='FULL CASHOUT button is not present')
        cashout_value = self.bet_amount - (self.bet_amount * 0.1)
        expected_cashout_button_value = 'CASH OUT {0}{1:.2f}'.format(self.currency, cashout_value)
        actual_cashout_button_value = bet.buttons_panel.full_cashout_button.name
        self.assertEqual(actual_cashout_button_value, expected_cashout_button_value,
                         msg=f'Actual full cash out button value: "{actual_cashout_button_value}", '
                             f'expected: "{expected_cashout_button_value}"')
