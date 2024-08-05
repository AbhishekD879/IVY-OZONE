import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
# @pytest.mark.sanity
@vtest
class Test_C59015301_Transactions_History(BaseBetSlipTest):
    """
    TR_ID: C59015301
    NAME: Transactions History
    DESCRIPTION: This test case verifies Transactions History page.
    PRECONDITIONS: 1 User is logged in to view their Payment History
    PRECONDITIONS: 2 User has Approved and Declined Deposit transactions for the past three months
    PRECONDITIONS: 3 User has Approved/Pending/Declined Withdraw transactions for the past three months (optional)
    PRECONDITIONS: 4 User has Gaming / Casino transactions (optional)
    PRECONDITIONS: 5 User has navigated to the 'My Account' menu
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Load Oxygen/Roxanne Application and login
        DESCRIPTION: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
        DESCRIPTION: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=1)
            outcomes_1 = next(((market['market'].get('children')) for market in events[0]['event'].get('children')), None)
            if outcomes_1 is None:
                raise SiteServeException('There are no available outcomes')

            team1_1 = next((outcome['outcome']['name'] for outcome in outcomes_1 if
                            outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not team1_1:
                raise SiteServeException('No Home team present is SS response')
            self.__class__.selection_ids_1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_1}.get(team1_1)
        else:
            events_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=2)
            self.__class__.selection_ids = [event_params.selection_ids[event_params.team1] for event_params in events_params]
            self.__class__.selection_ids_1 = self.selection_ids[0]

    def test_001_navigate_to_history___transactions_history(self):
        """
        DESCRIPTION: Navigate to History -> Transactions History
        EXPECTED: Transactions History page is Opened
        EXPECTED: ![](index.php?/attachments/get/111269055)
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids_1)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.device.refresh_page()
        self.assertTrue(self.site.header.right_menu_button.is_displayed(),
                        msg='[My Account] button is not displayed on Header')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')

        history_config = self.site.window_client_config.get_gvc_config_item(
            key_title='name', value_title='history')
        self.__class__.history_title = history_config.get('text').upper()
        self.site.right_menu.click_item(item_name=self.history_title)
        sleep(2)
        history_items = self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='historyitems')
        history_menu_names = [item.get('text').upper() if self.brand == 'bma' else item.get('text') for item in history_items.get('children')]
        sections = self.site.right_menu.items_names
        self.assertEqual(set(sections), set(history_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{history_menu_names}')
        item_name = vec.bma.HISTORY_MENU_ITEMS[1] if self.brand == 'bma' else vec.bma.HISTORY_MENU_ITEMS[2]
        self.site.right_menu.items_as_ordered_dict.get(item_name).click()
        sleep(5)
        self.site.wait_content_state_changed(timeout=30)
        transaction_text = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='transaction')
        bypass_exceptions = (NoSuchElementException, StaleElementReferenceException, VoltronException)
        wait_for_result(lambda: transaction_text in self.site.menus.items_names,
                        timeout=20,
                        name=f'Item "{transaction_text}" to be present',
                        bypass_exceptions=bypass_exceptions)
        self.site.wait_splash_to_hide()

    def test_002_verify_the_transactions_table_after_filter_selection(self):
        """
        DESCRIPTION: Verify the transactions table after filter selection
        EXPECTED: Table can include following transactions:
        EXPECTED: - deposit transactions
        EXPECTED: - gaming / casino transactions
        EXPECTED: etc.
        EXPECTED: ![](index.php?/attachments/get/111269061)
        """
        self.assertTrue(self.site.transaction_history.transaction_data, msg='No transactions history found')
        self.assertTrue(self.site.transaction_history.transaction_entries, msg='No Transactions displayed')

    def test_003_verify_profitloss__total_stake__total_returns_fields(self):
        """
        DESCRIPTION: Verify Profit/Loss | Total Stake | Total Returns fields
        EXPECTED: Information is shown according to the selected dates and list of transactions
        """
        stake_labels = self.site.transaction_history.stake_returns.stake_lables
        label_list = ['PROFIT/LOSS', 'TOTAL STAKES', 'TOTAL RETURNS']
        for item in stake_labels:
            self.assertTrue(item.text.upper() in label_list, msg=f'"{item.text}" field is not displayed')

        stake_values = self.site.transaction_history.stake_returns.stake_values
        for item in stake_values:
            self.assertTrue(item.text, msg='Stake table field value not displayed')
