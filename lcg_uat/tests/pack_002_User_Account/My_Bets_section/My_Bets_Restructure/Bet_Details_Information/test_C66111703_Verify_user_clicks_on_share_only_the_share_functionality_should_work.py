import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_details_information
@vtest
class Test_C66111703_Verify_user_clicks_on_share_only_the_share_functionality_should_work(BaseBetSlipTest):
    """
    TR_ID: C66111703
    NAME: Verify user clicks on share only the share functionality should work
    DESCRIPTION: This test case verify user clicks on share only the share functionality should work
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True

    def verify_my_bets_share_icon(self, bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                        msg=f'Share button is not displayed under {tab_name}')
        bet.bet_details.share_button.click()
        share_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_SHARE, timeout=5)
        self.assertIsNotNone(share_dialog,
                             msg=f'Share dialog is not displayed after clicking share icon under {tab_name}')
        share_dialog.close_dialog()
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details is not collapsed state after performing actions on share icon under {tab_name}')

        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details is not expanded after click on Bet Details chevron under {tab_name}')
        self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                        msg=f'Share button is not displayed under {tab_name}')
        bet.bet_details.share_button.click()
        share_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_SHARE, timeout=5)
        self.assertIsNotNone(share_dialog,
                             msg=f'Share dialog is not displayed after clicking share icon under {tab_name}')
        share_dialog.close_dialog()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details is not expanded state after performing actions on share icon under {tab_name}')

    def test_000_preconditions(self):
        """
        Get selections to place single and multiple bets
        """
        self.__class__.number_of_events = 1
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    additional_filters=cashout_filter,
                                                    number_of_events=1)[0]
        match_result_market = next((market['market'] for market in event['event']['children'] if
                                    market.get('market').get('templateMarketName') == 'Match Betting'), None)
        outcomes = match_result_market['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_id = list(all_selection_ids.values())[0]

    def test_001_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        # Covered in above step

    def test_003_place_singlemutiple_bets__from_sportsraces(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from Sports/Races
        EXPECTED: Bets should be placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        # Covered in below step

    def test_005_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        # Covered in below step

    def test_006_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        # Covered in below step

    def test_007_click_on_expand_to_see_share_icon_functionality(self):
        """
        DESCRIPTION: Click on expand to see share icon functionality
        EXPECTED: Share functionality should be same
        """
        # Covered in below step

    def test_008_collapse_the_bet_detail_and_check_the_share_icon(self):
        """
        DESCRIPTION: Collapse the bet detail and check the share icon
        EXPECTED: Share functionality should be same in collapse state
        EXPECTED: ![](index.php?/attachments/get/cea9402b-a0e0-4c12-a5f6-6fd603bdb8bc)
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_my_bets_share_icon(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_my_bets_share_icon(bet=cash_out_bet, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_my_bets_share_icon(bet=settled_bet, tab_name='Settled tab')

    def test_009_repeat_the_above_steps_for_cashout_tab_for_share_icon(self):
        """
        DESCRIPTION: Repeat the above steps for cashout tab for share icon
        EXPECTED:
        """
        # Covered in above step

    def test_010_repeat_the_above_steps_for_settle_tab(self):
        """
        DESCRIPTION: Repeat the above steps for settle tab
        EXPECTED:
        """
        # Covered in above step