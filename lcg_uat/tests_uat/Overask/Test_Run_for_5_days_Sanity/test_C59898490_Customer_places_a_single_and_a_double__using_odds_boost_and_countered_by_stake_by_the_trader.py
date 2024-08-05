import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime, timedelta
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.slow
@vtest
class Test_C59898490_Customer_places_a_single_and_a_double__using_odds_boost_and_countered_by_stake_by_the_trader(BaseBetSlipTest):
    """
    TR_ID: C59898490
    NAME: Customer places a single and a double - using odds boost and countered by stake by the trader
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    suggested_max_bet = 0.25
    prices = [{0: '1/2', 1: '1/10', 2: '1/9'},
              {0: '1/2', 1: '1/11', 2: '1/11'}]
    event_ids = []
    event_names = []
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(default_market_name='|Draw No Bet|',
                                                                                     lp=self.prices[i], max_bet=self.max_bet,
                                                                                     max_mult_bet=self.max_mult_bet)
            self.event_ids.append(event_params.event_id)
            self.event_names.append(f'{event_params.team1} v {event_params.team2}')
            self.selection_ids.append(list(event_params.selection_ids.values())[0])
        if self.site.wait_logged_out():
            self.__class__.username = tests.settings.betplacement_user
            self.site.login(self.username)
        self.__class__.exp_date_1 = datetime.now() + timedelta(hours=7)
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_ids[0], expiration_date=self.exp_date_1)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_hr_selections_or_any_sport_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stakemake_sure_bet_is_boosted__click_on_odds_boosted_(self, single=True):
        """
        DESCRIPTION: Add HR selections OR ANY sport SELECTIONS to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        DESCRIPTION: Make sure Bet is boosted ( Click on Odds Boosted )
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.5
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section, multiples_section = sections.Singles, sections.Multiples
        if single:
            old_stake = list(singles_section.values())[0]
            old_price = old_stake.odds
            for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=1).items():
                self.enter_stake_amount(stake=stake)
        else:
            old_stake = list(multiples_section.values())[0]
            old_price = old_stake.odds
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
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section, multiples_section = sections.Singles, sections.Multiples
        if single:
            new_stake = list(singles_section.values())[0]
        else:
            new_stake = list(multiples_section.values())[0]
        self.__class__.new_price = new_stake.boosted_odds_container.price_value
        self.assertNotEqual(old_price, self.new_price,
                            msg=f'Actual price"{old_price}" is same as updated price "{self.new_price}')
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_by_stake_in_ob_ti_tool(self, single=True):
        """
        DESCRIPTION: Counter by stake in OB TI tool
        EXPECTED: Counter is seen a offer with the new stake highlighted and updated potential returns shown to the customeron FE
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.event_ids[0])
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id, betslip_id=betslip_id,
                                       max_bet=self.suggested_max_bet)
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=25)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain "{cms_overask_expires_message}" from CMS')
        if single:
            sections = self.get_betslip_sections().Singles
            self.__class__.actual_stake = float(sections.overask_trader_offer.stake_content.stake_value.value.strip('£'))
        else:
            sections = self.get_betslip_sections(multiples=True).Multiples
            self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
            self.__class__.actual_stake = float(sections.overask_trader_offer.stake_content.stake_value.name[1:])
        expected_stake = float(self.suggested_max_bet)
        self.assertEqual(self.actual_stake, expected_stake,
                         msg=f'Actual stake "{self.actual_stake}" is not same as Expected stake "{expected_stake}"')
        stake_color = sections.overask_trader_offer.stake_content.stake_value.value_color
        self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified stake is not highlighted in yellow')
        new_potential_returns = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=new_potential_returns, bet_amount=self.suggested_max_bet,
                                      odds=self.new_price)

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: The balance should be updated correctly and bet receipt shown to the customer with odds boost signposting
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.has_odds_boost_signpost(),
                        msg='"odds boost" signpost is not displayed')
        self.device.refresh_page()
        expected_user_balance = self.user_balance - float(self.actual_stake)
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_004_navigate_to_my_bets(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History. and  user should see signposted in My Bets section
        """
        self.site.open_my_bets_open_bets()
        self.site.wait_content_state_changed()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=bet_type,
                                                                                event_names=self.event_names[0])
        self.assertTrue(self.event_names[0] in bet_name,
                        msg=f'*** "{self.event_names[0]}" bet not found in the openbets')
        self.assertTrue(bet.has_odds_boost_signpost(), msg=f'"odds boost" signpost is not displayed for "{bet_name}"')
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.site.wait_content_state_changed()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=bet_type,
                                                                                event_names=self.event_names[0])
        self.assertTrue(self.event_names[0] in bet_name,
                        msg=f'*** "{self.event_names[0]}" bet not found in the openbets')
        self.assertTrue(bet.has_odds_boost_signpost(), msg=f'"odds boost" signpost is not displayed for "{bet_name}"')

    def test_005_if_customer_declines_the_offer(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.event_ids.clear()
        self.selection_ids.clear()
        self.event_names.clear()
        self.test_000_preconditions()
        if bet_type == vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE:
            self.test_001_add_hr_selections_or_any_sport_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stakemake_sure_bet_is_boosted__click_on_odds_boosted_()
            self.test_002_counter_by_stake_in_ob_ti_tool()
        else:
            self.test_001_add_hr_selections_or_any_sport_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stakemake_sure_bet_is_boosted__click_on_odds_boosted_(single=False)
            self.test_002_counter_by_stake_in_ob_ti_tool(single=False)
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.site.wait_content_state_changed()
        self.verify_bet_in_open_bets(bet_type=bet_type, event_name=self.event_names[0], bet_in_open_bets=False)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(bet_type=bet_type, event_name=self.event_names[0], bet_in_open_bets=False)
        self.site.wait_content_state_changed()

    def test_006_Repeat_the_same_steps_by_adding_a_double_selection_from_HR_or_any_other_sports(self):
        """
        DESCRIPTION: Repeat the same steps by adding a double selection from HR or any other sports
        """
        self.event_ids.clear()
        self.selection_ids.clear()
        self.event_names.clear()
        self.test_000_preconditions()
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_ids[0], expiration_date=self.exp_date_1)
        self.test_001_add_hr_selections_or_any_sport_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stakemake_sure_bet_is_boosted__click_on_odds_boosted_(
            single=False)
        self.test_002_counter_by_stake_in_ob_ti_tool(single=False)
        self.test_003_if_customer_accepts_the_offer()
        self.test_004_navigate_to_my_bets(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
        self.test_005_if_customer_declines_the_offer(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
