import datetime
import voltron.environments.constants as vec
import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C18258214_Vanilla_Place_bet_after_account_closure__long_time(BaseBetSlipTest):
    """
    TR_ID: C18258214
    NAME: [Vanilla] Place bet after account closure - long time
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and have Sports product closed
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in and have Sports product closed
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount,
                                                                 card_number=tests.settings.master_card,
                                                                 card_type='mastercard', expiry_month=self.expiry_month,
                                                                 expiry_year=self.expiry_year,
                                                                 cvv=tests.settings.master_card_cvv)
        self.site.login(username=user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=30)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.site.wait_splash_to_hide(7)
        options = self.site.account_closure.items
        options[0].click()
        self.site.account_closure.continue_button.click()
        self.site.service_closure.items_as_ordered_dict[vec.bma.SPORTS.title()].close_button.click()
        self.site.service_closure.duration_options.items[0].click()
        self.site.service_closure.reason_options.items[0].click()
        self.site.service_closure.continue_button.perform_click()
        self.site.service_closure.close_button.click()
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_SPORTS_INFO_TEXT,
                         msg=f'Actual text: "{actual_info_text}" is not same as '
                             f'Expected text: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_SPORTS_INFO_TEXT}"')

    def test_001_make_a_bet_selection(self):
        """
        DESCRIPTION: Make a bet selection
        EXPECTED: Selection is added to Bet Slip.
        """
        if tests.settings.backend_env == 'prod':
            selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
        else:
            selection_ids = self.ob_config.add_autotest_premier_league_football_event(in_play_event=False).selection_ids
        self._logger.info(f'Found Football event with selections "{self.selection_ids}"')
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        self.verify_betslip_counter_change(expected_value=1)

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter stake
        EXPECTED: Stake is added
        """
        self.__class__.bet_amount = 0.5
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(), msg='Stake was not added')

    def test_003_click_the_place_bet_button(self):
        """
        DESCRIPTION: Click the 'Place bet' button
        EXPECTED: Error message appears:
        EXPECTED: "..."
        EXPECTED: Bet is not placed.
        """
        self.get_betslip_content().bet_now_button.click()
        sleep(5)  # Getting attribute error due to synchronization issue
        actual_message = self.get_betslip_content().suspended_account_warning_message.text
        self.assertEqual(actual_message, vec.betslip.ACCOUNT_SUSPENDED,
                         msg=f'Actual suspension message: "{actual_message}" is not same as expected suspension message: "{vec.betslip.ACCOUNT_SUSPENDED}"')
        self.assertTrue(self.get_betslip_counter_value() == "1", msg='Bet was placed')

    def test_004_go_to_settled_bets(self):
        """
        DESCRIPTION: Go to 'Settled Bets'
        EXPECTED: Bet is not present there
        """
        self.navigate_to_page("Homepage")
        self.site.open_my_bets_settled_bets()
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.assertFalse(len(bets),
                         msg='Bet is present in the Settled bets tab')

    def test_005_go_to_cash_out(self):
        """
        DESCRIPTION: Go to 'Cash out'
        EXPECTED: Bet is not present there
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
            self.assertFalse(len(bets),
                             msg='Bet is present in the Cashout tab')

    def test_006_go_to_open_bets(self):
        """
        DESCRIPTION: Go to 'Open bets'
        EXPECTED: Bet is not present there
        """
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertFalse(len(bets),
                         msg='Bet is present in the Open bets tab')
