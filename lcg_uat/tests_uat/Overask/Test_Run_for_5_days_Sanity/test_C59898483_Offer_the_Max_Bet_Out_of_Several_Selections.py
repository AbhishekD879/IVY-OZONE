import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C59898483_Offer_the_Max_Bet_Out_of_Several_Selections(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C59898483
    NAME: Offer the Max Bet Out of Several Selections
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    selection_ids = []
    bet_amount = 0
    max_bet = 2
    event_ids = []
    event_names = []
    stake_1 = 1
    stake_2 = 3

    def create_events(self):
        self.selection_ids.clear()
        self.event_ids.clear()
        self.event_names.clear()
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet,
                                                                                     max_mult_bet=self.max_bet)
            selection_id, eventID = \
                event_params.selection_ids, event_params.event_id
            self.__class__.event_ids.append(eventID)
            self.__class__.selection_ids.append(list(selection_id.values())[0])
            start_time = event_params.event_date_time
            start_time_local = self.convert_time_to_local(date_time_str=start_time,
                                                          future_datetime_format=self.event_card_future_time_format_pattern)
            self.__class__.event_names.append(f'SINGLE - [{event_params.team1} v {event_params.team2} {start_time_local}]')

    def enter_stake_click_place_bet_button(self):
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        self.bet_amount = self.stake_1
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.bet_amount = self.stake_2
        stake_name1, stake1 = list(singles_section.items())[1]
        self.enter_stake_amount(stake=(stake_name1, stake1))
        self.get_betslip_content().bet_now_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Events
        PRECONDITIONS: User is logged in to application
        EXPECTED: creating events and login to the application
        """
        self.create_events()
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.site.wait_content_state('Homepage')
        self.__class__.user_balance_before_bet = self.site.header.user_balance

    def test_001_add_several_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add several selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.enter_stake_click_place_bet_button()
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

    def test_002_offer_the_max_bet_out_of_several_selections_in_ob_ti_tool(self):
        """
        DESCRIPTION: Offer the Max Bet Out of Several Selections in OB TI tool
        EXPECTED: Customer should see a counter offer with the OA bet countered by max stake.
        EXPECTED: The other selections in the bet are unchanged
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.event_ids[1])
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.offer_max_bet(bet_id=bet_id, betslip_id=betslip_id)
        singles_section = self.get_betslip_sections().Singles
        stake_name1, self.__class__.stake1 = list(singles_section.items())[0]
        actual_stake_value1 = float(self.stake1.offered_stake.name.strip('£'))
        self.assertEqual(actual_stake_value1, float(self.stake_1),
                         msg=f'New stake value: "{actual_stake_value1}" '
                             f'is not as expected: "{self.stake_1}"')
        stake_name2, self.__class__.stake2 = list(singles_section.items())[1]
        actual_stake_value2 = float(self.stake2.offered_stake.name.strip('£'))
        self.assertNotEqual(actual_stake_value2, float(self.stake_2),
                            msg=f'New stake value: "{actual_stake_value2}" '
                                f'is not as expected: "{self.stake_2}"')

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated correctly
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        total_bet_amount = self.stake_1 + self.max_bet
        self.verify_user_balance(expected_user_balance=self.user_balance_before_bet - total_bet_amount)

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        self.navigate_to_page("Homepage")
        self.site.wait_splash_to_hide()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[1],
                                     bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[1],
                                     bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page("Homepage")
        self.site.wait_splash_to_hide()
        self.site.logout()

    def test_005_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.create_events()
        self.site.login(username=self.username, async_close_dialogs=False)
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_add_several_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_offer_the_max_bet_out_of_several_selections_in_ob_ti_tool()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[1],
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[1],
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
