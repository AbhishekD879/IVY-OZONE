import pytest
import voltron.environments.constants as vec
import tests
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C18753269_Verify_My_Bets_counter_after_Edit_My_acca(BaseUserAccountTest, BaseCashOutTest):
    """
    TR_ID: C18753269
    NAME: Verify My Bets counter after Edit My acca
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after user edits acca on My Bets page
    """
    keep_browser_open = True
    number_of_events = 4
    selection_ids = []
    selection_ids1 = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - Load Oxygen/Roxanne Application
        PRECONDITIONS: - Make sure user has open(unsettled) bets with edit my acca available ( for multiples)
        PRECONDITIONS: - Make sure My bets counter config is turned on in CMS > System configurations
        PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
        """
        self.check_my_bets_counter_enabled_in_cms()
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
                selection_id, selection_id1 = list(all_selection_ids)[0], list(all_selection_ids)[1]
                self.selection_ids.append(selection_id)
                self.selection_ids1.append(selection_id1)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events)
            self.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
            self.selection_ids1 = [list(event.selection_ids.values())[1] for event in event_params]
        self.site.login()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=1)
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_navigate_to_cash_out_or_my_bets_tabpage(self):
        """
        DESCRIPTION: Navigate to 'Cash out' or 'My Bets' tab/page
        EXPECTED: 'Cash Out'/'My Bets' tab/page is opened
        """
        self.site.open_my_bets_open_bets()
        open_bets_tab_name = self.site.open_bets.tabs_menu.current
        self.assertEqual(open_bets_tab_name.title(), vec.bet_history.OPEN_BETS_TAB_NAME.title(),
                         msg="Open bets was page not opened")

    def test_002__select_edit_my_acca_and_delete_one_or_more_selections_confirm_changes(self):
        """
        DESCRIPTION: * Select edit my acca and delete one or more selections
        DESCRIPTION: * Confirm changes
        EXPECTED: Bet is modified
        """
        self.__class__.initial_counter = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets are available')
        bet = list(bets.values())[0]
        self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                        msg='"Edit my bet" button is not displayed')
        bet.edit_my_acca_button.click()
        wait_for_result(
            lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0].edit_my_acca_button.name == vec.ema.CANCEL.upper(),
            name='"CANCEL EDITING" text to be displayed', timeout=10)
        selections = list(bet.items_as_ordered_dict.values())
        selection = selections[0]
        selection.edit_my_acca_remove_icon.click()
        sleep(3)
        wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(),
                        name='"UNDO button" to be displayed', timeout=10)
        self.assertTrue(bet.confirm_button.is_enabled(), msg='"Confirm" button is not clickable')
        bet.confirm_button.click()
        wait_for_result(lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0].cash_out_successful_message == vec.ema.EDIT_SUCCESS.caption,
                        name='"Acca Edited Successfully" message to be displayed', timeout=20)

    def test_003_check_my_bets_counter_on_footer_remains_the_same(self):
        """
        DESCRIPTION: Check my bets counter on Footer remains the same
        EXPECTED: My bets counter didn't change
        """
        counter_value = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        self.assertEqual(counter_value, self.initial_counter,
                         msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter}"')

    def test_004_repeat_steps_1_3_for_another_bet_with_edit_my_acca_available(self):
        """
        DESCRIPTION: Repeat steps #1-3 for another bet with edit my acca available
        EXPECTED: Results are the same
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids1)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=1)
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state(state_name='HomePage')
        self.test_001_navigate_to_cash_out_or_my_bets_tabpage()
        self.test_002__select_edit_my_acca_and_delete_one_or_more_selections_confirm_changes()
        self.test_003_check_my_bets_counter_on_footer_remains_the_same()
