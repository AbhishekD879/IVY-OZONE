import datetime
import tests
import voltron.environments.constants as vec
import pytest
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C16408296_Verify_My_Bets_counter_displaying_maximum_Open_Bets_number20(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C16408296
    NAME: Verify My Bets counter displaying maximum Open Bets number(20)
    DESCRIPTION: This test case verifies displaying more than 20 open bets on My Bets Badge Icon
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Login with user who has 21 open (unsettled) bets
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True
    bet_amount = 0.10
    number_of_events = 21
    selection_ids = []
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def place_multiple_single_bets(self, start, end):
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[start:end])
        singles_section = self.get_betslip_sections().Singles
        for stake in list(singles_section.items()):
            self.enter_stake_amount(stake=stake)
            self.site.wait_splash_to_hide(5)
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state('Homepage')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - Load Oxygen/Roxanne Application
        PRECONDITIONS: - Login with user who has 21 open (unsettled) bets
        PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
        PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=user_name, amount=str(20),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        self.site.login(username=user_name)
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in cms')
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = [i['outcome']['id'] for i in outcomes]
                selection_id = list(all_selection_ids)[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events, )
            self.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]

        self.place_multiple_single_bets(start=0, end=7)
        self.place_multiple_single_bets(start=7, end=14)
        self.place_multiple_single_bets(start=14, end=len(self.selection_ids))

    def test_001_verify_my_bets_on_footer_menu(self):
        """
        DESCRIPTION: Verify 'My bets' on Footer Menu
        EXPECTED: My bets counter icon is displayed with '20+' in top right corner
        """
        my_bets_counter = self.get_my_bets_counter_value_from_footer()
        self.assertEqual(my_bets_counter, '20+',
                         msg=f'Actual My Bets counter value: "{my_bets_counter}" is not same Expected value: "20+"')

    def test_002_go_to_cashout_pagetab_and_make_a_full_cashout_of_one_bet(self):
        """
        DESCRIPTION: Go to Cashout page/tab and make a full cashout of one bet
        EXPECTED: Bet is cashed out successfully
        """
        self.site.open_my_bets_cashout()
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg=f'Bets are not found on "Open Bets" page')
        bet = list(bets.values())[0]
        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

    def test_003_verify_my_bets_on_footer_menu(self):
        """
        DESCRIPTION: Verify 'My bets' on Footer Menu
        EXPECTED: My bets counter icon is displayed with '20' in top right corner
        """
        sleep(3)
        counter_after_cashout = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_after_cashout, 20,
                         msg=f'Actual My Bets counter value after cashout: "{counter_after_cashout}" is not same Expected value: "20"')

    def test_004_add_selection_to_betslipquickbet_and_place_bet(self):
        """
        DESCRIPTION: Add selection to Betslip/QuickBet and place bet
        EXPECTED: Bet is placed successfully
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state('Homepage')

    def test_005_verify_my_bets_on_footer_menu(self):
        """
        DESCRIPTION: Verify 'My bets' on Footer Menu
        EXPECTED: My bets counter icon is displayed with '20+' in top right corner
        """
        my_bets_counter = self.get_my_bets_counter_value_from_footer()
        self.assertEqual(my_bets_counter, '20+',
                         msg=f'Actual My Bets counter value: "{my_bets_counter}" is not same Expected value: "20+"')

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: My Bets Footer menu is displayed without counter
        """
        self.site.logout()
        my_bets_counter = self.get_my_bets_counter_value_from_footer()
        self.assertEqual(my_bets_counter, '0',
                         msg=f'Actual My Bets counter value: "{my_bets_counter}" is not same Expected value: "0"')
