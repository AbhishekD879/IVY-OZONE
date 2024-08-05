import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.reg167_fix
@vtest
class Test_C29027_Section_Open_User_with_Zero_Insufficient_Balance(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C29027
    NAME: Section Open User with Zero/ Insufficient Balance
    DESCRIPTION: This test case verifies 'Quick Deposit' section on the Betslip for the User with 0 or Insufficient balance
    PRECONDITIONS: 1.  User account with **0 balance and at least one registered Credit Card** (Additional pop-up Quick Deposit)
    PRECONDITIONS: 2.  User account with **positive balance and at least one registered Credit Card**
    """
    keep_browser_open = True
    bet_amount = 1
    additional_amount = 6
    min_deposit_for_bet_message = vec.Quickdeposit.EXPECTED_MIN_DEPOSIT_FOR_BET_MESSAGE_CURRENCY

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1.  User account with **0 balance and at least one registered Credit Card** (Additional pop-up Quick Deposit)
        PRECONDITIONS: 2.  User account with **positive balance and at least one registered Credit Card**
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            market_name, outcomes = next(((market['market']['name'], market['market']['children']) for market in event['event']['children']
                                         if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.expected_market_name = normalize_name(event['event']['children'][0].get('market').get('name'))
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name, self.__class__.selection_id = list(self.selection_ids.items())[1]
            self.__class__.selection_id1 = list(self.selection_ids.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id
            self.__class__.selection_name, self.__class__.selection_id = list(event.selection_ids.items())[1]
            self.__class__.selection_id1 = list(event.selection_ids.values())[0]
            market_name = normalize_name(
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
            self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_load_application_and_log_in_with_account_1(self):
        """
        DESCRIPTION: Load application and Log in with account 1
        EXPECTED: - User is logged in
        """
        # User have zero balance with Quick deposite card
        self.site.login(username= "testgvcld_XP7IG0" if self.brand == "ladbrokes" else "testgvccl-QLNJ8U")
        self.__class__.user_balance = self.site.header.user_balance
        if self.user_balance:
            self.open_betslip_with_selections(selection_ids=self.selection_id)
            self.bet_amount = self.user_balance
            self.place_single_bet()
            self.navigate_to_page("Homepage")

    def test_002_open_the_betslip_pagewidget_with_an_added_selection(self):
        """
        DESCRIPTION: Open the Betslip page/widget with an added selection
        EXPECTED: - Made selection is displayed correctly within Betslip content area
        EXPECTED: **Coral**
        EXPECTED: - 'QUICK DEPOSIT' section is displayed on the bottom of the Bet Slip
        # EXPECTED: - 'Please deposit a min of <currency>5.00/50 for SEK to continue placing your bet' default message is shown within Quick Deposit
        EXPECTED: - 'DEPOSIT' button is shown at the bottom of the section
        EXPECTED: **Ladbrokes**
        EXPECTED: - There is NO 'Quick Deposit' section or error message displayed on the Bet Slip
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        bet_button = self.get_selection_bet_button(selection_name=self.selection_name, market_name=self.expected_market_name)
        bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip(timeout=15)
            self.site.open_betslip()
        self.site.wait_content_state_changed(timeout=5)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        self.assertIn(self.selection_name, singles_section.keys(),
                      msg=f'Actual list "{singles_section.items()}" does not contain Added selection "{self.selection_name}"')
        if self.device_type == 'mobile':
            if not self.get_betslip_content().has_deposit_form():
                self.site.close_betslip()
                self.site.wait_content_state_changed(10)
                self.site.open_betslip()
        else:
            self.navigate_to_page(name='?automationtest=true&q=1')
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit is not displayed')
        self.assertTrue(self.site.betslip.quick_deposit.is_displayed(), msg='Deposit button is not displayed')

    def test_003_coralclicktap_x_close_icon(self):
        """
        DESCRIPTION: **Coral**
        DESCRIPTION: Click/Tap 'X' (Close) icon
        EXPECTED: **Coral**
        EXPECTED: - 'QUICK DEPOSIT' section is closed
        EXPECTED: - 'DEPOSIT' button changes to 'PLACE BET'
        """
        # deposit_button = self.get_betslip_content().make_quick_deposit_button.name
        self.site.betslip.quick_deposit.close_button.click()
        sleep(2)
        # self.assertFalse(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is displayed')
        self.assertTrue(self.site.betslip.has_bet_now_button(), msg='Place Bet button is not displayed')
        # self.__class__.place_bet_button = self.site.betslip.bet_now_button.name
        # self.assertNotEqual(deposit_button, self.place_bet_button,
        #                     msg=f'Deposit Button name: "{deposit_button}" is not changed to Place bet button: "{self.place_bet_button}"')

    def test_004_enter_value_less_than_5_in_the_stake_field(self):
        """
        DESCRIPTION: Enter value less than 5 in the 'Stake' field
        EXPECTED: - 'Please deposit a min of <currency>5.00/50 for SEK to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: - 'PLACE BET' button becomes 'MAKE A DEPOSIT'
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')
        # make_deposit_button = self.site.betslip.make_quick_deposit_button.name
        # self.assertNotEqual(self.place_bet_button, make_deposit_button,
        #                     msg=f'Place bet button name: "{self.place_bet_button}" is not changed to Make deposit button: {make_deposit_button}')

    def test_005_enter_value_equal_or_more_than_5_in_the_stake_field(self):
        """
        DESCRIPTION: Enter value equal or more than 5 in the 'Stake' field
        EXPECTED: - 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: - 'PLACE BET' button becomes 'MAKE A DEPOSIT'
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        # stake.amount_form.input.value = ''
        # place_bet_button = self.site.betslip.bet_now_button.name

        stake.amount_form.input.value = self.additional_amount
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(6)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')
        # make_deposit_button = self.site.betslip.make_quick_deposit_button.name
        # self.assertNotEqual(place_bet_button, make_deposit_button,
        #                     msg=f'Place bet button name: "{place_bet_button}" is not changed to Make deposit button: {make_deposit_button}')

    def test_006_clicktap_make_a_deposit_button(self, positive_balance_user=False, bet_amount=None):
        """
        DESCRIPTION: Click/Tap 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is present
        EXPECTED: - 'Please deposit a min of <currency>XX.XX to continue placing your bet' error message is shown within 'QUICK DEPOSIT' section
        EXPECTED: -  The 'Deposit Amount' field must be in real time auto-populated with the calculated funds needed to cover the User’s bet
        EXPECTED: - 'DEPOSIT &/AND PLACE BET' button is shown at the bottom of the section
        """
        if positive_balance_user:
            singles_section = self.get_betslip_sections().Singles
            stake = list(singles_section.values())[0]
            stake.amount_form.input.value = bet_amount

        self.site.betslip.make_quick_deposit_button.click()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit is not displayed')

        # info_panel_text = self.get_betslip_content().bet_amount_warning_message
        # expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.stake_input)
        # self.assertEqual(info_panel_text, expected_message_text,
        #                  msg=f'Error message "{info_panel_text}" is not the same as expected "{expected_message_text}"')

        # quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        # self.__class__.deposit_and_place_bet_button = quick_deposit.deposit_and_place_bet_button.name
        # self.assertEqual(self.deposit_and_place_bet_button, vec.gvc.DEPOSIT_AND_PLACE_BTN,
        #                  msg=f'Actual Desposit and place bet button name: "{self.deposit_and_place_bet_button}" is not '
        #                      f'same is Expected name: "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')

    def test_007_clicktap_x_close_icon(self):
        """
        DESCRIPTION: Click/Tap 'X' (Close) icon
        EXPECTED: - 'QUICK DEPOSIT' section is closed
        EXPECTED: - 'DEPOSIT &/AND PLACE BET' button becomes 'MAKE A DEPOSIT'
        """
        try:
            self.site.betslip.quick_deposit.close_button.click()
        except Exception:
            self.navigate_to_page('Homepage')
            self.site.wait_content_state_changed()
            self.site.open_betslip()
            self.site.wait_content_state_changed()
            sleep(5)
            if self.get_betslip_content().has_deposit_form():
                self.site.betslip.quick_deposit.close_button.click()
        self.site.wait_splash_to_hide(10)
        # self.assertFalse(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')
        # make_deposit_button = self.site.betslip.make_quick_deposit_button.name
        # self.assertNotEqual(self.deposit_and_place_bet_button, make_deposit_button,
        #                     msg=f'Deposit and place bet button name: '
        #                     f'{self.deposit_and_place_bet_button} was not changed to Make deposit: "{make_deposit_button}"')

    def test_008_change_value_in_stake_field_and_open_quick_deposit_section(self, bet_amount=8):
        """
        DESCRIPTION: Change value in 'Stake' field and Open 'QUICK DEPOSIT' section
        EXPECTED: - Value is recalculated in 'Please deposit a min..' message and 'Deposit Amount' field to cover the User's bet in real time
        """
        try:
            self.__class__.user_balance = self.get_betslip_content().header.user_balance
        except NotImplementedError as e:
            self._logger.warning(e)
            self.__class__.user_balance = self.get_balance_by_page('all')
        self.__class__.bet_amount = bet_amount
        singles_section = self.get_betslip_sections().Singles
        self.stake_name, self.stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.bet_amount - self.user_balance)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')

    def test_009_add_a_few_more_selections_to_the_bet_slip_open_the_bet_slip_and_enter_stake_for_added_selections(self, zero_balance_user=True):
        """
        DESCRIPTION: Add a few more selections to the Bet Slip, open the Bet Slip and enter 'Stake' for added selections
        EXPECTED: - Value is recalculated in 'Please deposit a min..' message and 'Deposit Amount' field to cover the User's bet in real time
        """
        self.__class__.expected_betslip_counter_value = 1
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        if zero_balance_user:
            result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                     name='Quick deposit section to be displayed', timeout=10)
            if result:
                self.site.betslip.quick_deposit.close_button.click()

        singles_section = self.get_betslip_sections().Singles
        self.stake_name, self.stake = list(singles_section.items())[1]
        self.stake.amount_form.input.value = self.additional_amount
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.bet_amount + self.additional_amount - self.user_balance)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')
        self.stake.remove_button.click()

    def test_010_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - User is  logged out
        EXPECTED: - There is NO 'Quick Deposit' section or error message displayed on the Bet Slip
        """
        self.navigate_to_page('Homepage')
        self.site.logout()
        self.site.wait_logged_out(15)
        self.navigate_to_page(name='?automationtest=true&q=1')  # to handle Cookies pop up
        self.site.open_betslip()
        # self.assertFalse(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')
        self.site.close_betslip()
        self.site.wait_content_state('Homepage')

    def test_011_log_in_with_account_2(self):
        """
        DESCRIPTION: Log in with account 2
        EXPECTED: - User is logged in
        """
        self.site.login(username=tests.settings.quick_deposit_user)
        self.site.wait_content_state("Homepage")

    def test_012_open_the_betslip_pagewidget(self):
        """
        DESCRIPTION: Open the Betslip page/widget
        EXPECTED: - Made selection is displayed within Betslip content area
        EXPECTED: - There is NO 'QUICK DEPOSIT' section or error message displayed on the Bet Slip
        EXPECTED: - Numeric keyboard with 'Quick stakes' buttons are displayed (if one selection has been added, mobile only)
        """
        self.site.open_betslip()
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertTrue(self.singles_section.items(), msg='No stakes found')
        self.assertIn(self.selection_name, self.singles_section.keys(),
                      msg=f'Actual list "{self.singles_section.items()}" does not contain Added selection "{self.selection_name}"')
        # self.assertFalse(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')

    def test_013_enter_stake_amount_greater_than_current_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount greater than current user's balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        try:
            self.__class__.user_balance = self.get_betslip_content().header.user_balance
        except NotImplementedError as e:
            self._logger.warning(e)
            self.__class__.user_balance = self.get_balance_by_page('all')
        singles_section = self.get_betslip_sections().Singles
        self.stake_name, self.stake = list(singles_section.items())[0]
        self.stake.amount_form.input.value = self.user_balance + self.additional_amount
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')

    def test_014_repeat_steps_6_10(self):
        """
        DESCRIPTION: Repeat steps 6-10
        """
        self.test_006_clicktap_make_a_deposit_button(positive_balance_user=True, bet_amount=self.user_balance + self.additional_amount)
        self.test_007_clicktap_x_close_icon()
        self.test_008_change_value_in_stake_field_and_open_quick_deposit_section(bet_amount=self.user_balance + self.additional_amount)
        self.test_009_add_a_few_more_selections_to_the_bet_slip_open_the_bet_slip_and_enter_stake_for_added_selections(zero_balance_user=False)
        self.test_010_log_out()
