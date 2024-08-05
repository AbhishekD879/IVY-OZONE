import pytest
import tests
from voltron.environments import constants as vec
from collections import defaultdict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C59898491_Customer_places_a_bet__1_single_and_a_double__using_odds_boost_and_accepted_by_the_trader(BaseBetSlipTest):
    """
    TR_ID: C59898491
    NAME: Customer places a bet - 1 single and a double - using odds boost and accepted by the trader
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = [{0: '1/2', 1: '1/3', 2: '1/4'},
              {0: '1/2', 1: '1/6', 2: '1/7'}]
    eventIDs = []
    selectionIDs = []
    event_names = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        for i in range(0, 2):
            event = self.ob_config.add_autotest_premier_league_football_event(default_market_name='|Draw No Bet|',
                                                                              lp=self.prices[i], max_bet=self.max_bet,
                                                                              max_mult_bet=self.max_mult_bet)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
            self.event_names.append(f'{event.team1} v {event.team2}')
        username = tests.settings.betplacement_user
        self.site.login(username)
        self.ob_config.grant_odds_boost_token(username=username, level='selection', id=self.selectionIDs[0])
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_hr_selections_or_any_sport_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stakemake_sure_bet_is_boosted__click_on_odds_boosted_(self):
        """
        DESCRIPTION: Add HR selections OR ANY sport SELECTIONS to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        DESCRIPTION: Make sure Bet is boosted ( Click on Odds Boosted )
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.bet_amount = self.max_mult_bet + 0.5
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section, multiples_section = sections.Singles, sections.Multiples
        old_stake1 = list(singles_section.values())[0]
        old_price1 = old_stake1.odds
        old_stake2 = list(multiples_section.values())[0]
        old_price2 = old_stake2.odds
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)
        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)
        odds_boost_header = self.get_betslip_content().odds_boost_header
        boosted = odds_boost_header.boost_button.name
        if boosted == vec.odds_boost.BOOST_BUTTON.disabled:
            odds_boost_header.boost_button.click()
        self.site.wait_content_state_changed()
        boosted = odds_boost_header.boost_button.name
        self.assertEqual(boosted, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg=f'Actual button"{boosted}" not changed to Expected button "{vec.odds_boost.BOOST_BUTTON.enabled}"')
        singles_section, multiples_section = sections.Singles, sections.Multiples
        new_stake1 = list(singles_section.values())[0]
        new_stake2 = list(multiples_section.values())[0]
        self.__class__.new_price1 = new_stake1.boosted_odds_container.price_value
        self.__class__.new_price2 = new_stake2.boosted_odds_container.price_value
        self.assertNotEqual(old_price1, self.new_price1,
                            msg=f'Actual price"{old_price1}" is same as updated price "{self.new_price1}')
        self.assertNotEqual(old_price2, self.new_price2,
                            msg=f'Actual price"{old_price2}" is same as updated price "{self.new_price2}')
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_accept_the_bet_in_ti(self):
        """
        DESCRIPTION: Accept the bet in TI
        EXPECTED: User is  taken to the bet receipt with bet as placed
        EXPECTED: Correct potential return should be shown to user
        EXPECTED: The balance should be updated correctly and bet receipt shown to the customer with odds boost signposting
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.eventIDs)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        data = defaultdict(dict)
        for bet_id, bet_type in bets_details.items():
            if bet_type == 'SGL':
                data['bet1']['id'] = bet_id
                data['bet1']['action'] = 'A'
                data['bet1']['bettype'] = bet_type
            elif bet_type == 'DBL':
                data['bet2']['id'] = bet_id
                data['bet2']['action'] = 'A'
                data['bet2']['bettype'] = bet_type
        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        self.check_bet_receipt_is_displayed()
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        single_section = bet_receipt_sections.get(vec.betslip.SINGLE).items_as_ordered_dict
        len_of_expected_singles = 1
        self.assertEqual(len(single_section), len_of_expected_singles,
                         msg=f'Length of singles section "{len(single_section)}" '
                             f'is not same as Expected length of singles "{len_of_expected_singles}"')
        selection = list(single_section.values())[0]
        new_potential_returns1 = selection.estimate_returns
        self.verify_estimated_returns(est_returns=new_potential_returns1, bet_amount=self.bet_amount,
                                      odds=self.new_price1)
        double_section = bet_receipt_sections.get(vec.betslip.DBL).items_as_ordered_dict
        len_of_expected_doubles = 2
        self.assertEqual(len(double_section), len_of_expected_doubles,
                         msg=f'Length of double section "{len(double_section)}" '
                             f'is not same as Expected length of double section items "{len_of_expected_doubles}"')
        new_potential_returns2 = bet_receipt_sections.get(vec.betslip.DBL).estimate_returns
        self.verify_estimated_returns(est_returns=new_potential_returns2, bet_amount=self.bet_amount,
                                      odds=self.new_price2)
        self.assertTrue(self.site.bet_receipt.has_odds_boost_signpost(),
                        msg='"odds boost" signpost is not displayed')
        self.device.refresh_page()
        expected_user_balance = self.user_balance - float(self.bet_amount * 2)
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_003_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History. and user should see signposted in My Bets section
        """
        self.site.open_my_bets_open_bets()
        self.site.wait_content_state_changed()
        bet_name1, bet1 = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                                  event_names=self.event_names[0])
        self.assertTrue(self.event_names[0] in bet_name1,
                        msg=f'*** "{self.event_names[0]}" bet not found in the openbets')
        self.assertTrue(bet1.has_odds_boost_signpost(), msg=f'"odds boost" signpost is not displayed for "{bet_name1}"')
        bet_name2, bet2 = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                                                                                  event_names=self.event_names[0])
        self.assertTrue(self.event_names[0] in bet_name2, msg=f'*** "{self.event_names[0]}" bet not found in the openbets')
        self.assertTrue(bet2.has_odds_boost_signpost(), msg=f'"odds boost" signpost is not displayed for "{bet_name2}"')
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.site.wait_content_state_changed()
        bet_name1, bet1 = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                                  event_names=self.event_names[0])
        self.assertTrue(self.event_names[0] in bet_name1,
                        msg=f'*** "{self.event_names[0]}" bet not found in the openbets')
        self.assertTrue(bet1.has_odds_boost_signpost(), msg=f'"odds boost" signpost is not displayed for "{bet_name1}"')
        bet_name2, bet2 = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
            event_names=self.event_names[0])
        self.assertTrue(self.event_names[0] in bet_name2,
                        msg=f'*** "{self.event_names[0]}" bet not found in the openbets')
        self.assertTrue(bet2.has_odds_boost_signpost(), msg=f'"odds boost" signpost is not displayed for "{bet_name2}"')
