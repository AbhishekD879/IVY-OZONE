import pytest
import datetime
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.footer
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C16408291_Verify_My_Bets_counter_after_login_logout(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C16408291
    VOL_ID: C29431476
    NAME: Verify My Bets counter after login/logout
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after login/logout
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Make sure to have at least 2 users with different number of open bets and one user with no bets placed
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - To verify correct number of my bets check response of 'count?' XHR request
    PRECONDITIONS: ( e.g.https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountHistory/count?fromDate=2018-09-25%2015%3A28%3A08&toDate=2019-09-26%2000%3A00%3A00&group=BET&pagingBlockSize=20&settled=N)
    """
    keep_browser_open = True
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        self.check_my_bets_counter_enabled_in_cms()

        self.__class__.user_1 = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=self.user_1,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        else:
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self._logger.info(f'*** Using Football event with selection ids: "{self.selection_ids}"')

        self.site.login(username=self.user_1)
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

        self.site.logout()

        self.__class__.user_2 = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=self.user_2,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.site.login(username=self.user_2, async_close_dialogs=False)

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

        self.site.logout()

    def test_001_login_with_user_who_has_placed_bets(self, user=None):
        """
        DESCRIPTION: Login with user who has placed bets
        EXPECTED: User is successfully logged in
        """
        user = self.user_1 if not user else user
        self.site.login(username=user, async_close_dialogs=False)

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_002_verify_my_bets_counter_on_footer_menu(self):
        """
        DESCRIPTION: Verify My bets counter on Footer menu
        EXPECTED: My bets counter is displaying a number of open bets available for user
        """
        self.site.open_my_bets_open_bets()
        expected_indicator = len(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict)

        actual_indicator = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(actual_indicator, expected_indicator,
                         msg=f'Actual value indicator "{actual_indicator}" != Expected "{expected_indicator}"')

    def test_003_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: My bets counter is not displayed anymore
        """
        self.site.logout()
        self.__class__.expected_betslip_counter_value = 0

        my_bets = self.get_my_bets_from_footer()
        self.assertFalse(my_bets.has_indicator(expected_result=False),
                         msg=f'My bets counter is displayed')

    def test_004_repeat_step_1_2_for_another_user(self):
        """
        DESCRIPTION: Repeat step # 1-2 for another user
        EXPECTED: My bets counter is showing corresponding number of bets
        """
        self.test_001_login_with_user_who_has_placed_bets(user=self.user_2)
        self.test_002_verify_my_bets_counter_on_footer_menu()

    def test_005_valid_for_coral_only_expire_user_session_and_check_my_bets_counter_on_footer_menu_ladbrokes_coral_log_out(self):
        """
        DESCRIPTION: [Valid for Coral only] expire user session and check My bets counter on Footer menu
        DESCRIPTION: [Ladbrokes/Coral] Log out
        EXPECTED: User is logged out
        EXPECTED: My bets counter is not displayed anymore
        """
        self.logout_in_new_tab()
        self.verify_logged_out_state()

        my_bets = self.get_my_bets_from_footer()
        self.assertFalse(my_bets.has_indicator(expected_result=False),
                         msg=f'My bets counter is displayed')

    def test_006_log_in_with_user_who_has_no_open_bets_verify_my_bets_counter_on_footer_menu(self):
        """
        DESCRIPTION: * Log in with user who has no open bets
        DESCRIPTION: * Verify My bets counter on Footer menu
        EXPECTED: * My bets counter icon is not displayed
        EXPECTED: * '0' is NOT displayed on My Bets counter icon
        """
        self.site.login(username=tests.settings.no_bet_history_user)

        my_bets = self.get_my_bets_from_footer()
        self.assertFalse(my_bets.has_indicator(expected_result=False),
                         msg=f'My bets counter is displayed')
