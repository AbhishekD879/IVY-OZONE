import pytest
import tests
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C12600660_Verify_Reuse_Selections_and_Start_Betting_Go_Betting_buttons_on_Bet_Receipt(BaseCashOutTest):
    """
    TR_ID: C12600660
    NAME: Verify 'Reuse Selections' and 'Start Betting'/'Go Betting' buttons on Bet Receipt
    DESCRIPTION: This test case verifies 'Reuse Selections' and 'Start Betting'/'Go Betting' buttons on Bet Receipt
    """
    keep_browser_open = True
    number_of_events = 4
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load Oxygen app
        PRECONDITIONS: 2. Make sure the user is logged into their account
        PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
        PRECONDITIONS: 4. Make bet placement for several single selections (at least 4)
        PRECONDITIONS: 5. Make sure Bet is placed successfully
        PRECONDITIONS: For <Sport>  it is possible to place a bet from:
        PRECONDITIONS: - event landing page
        PRECONDITIONS: - event details page
        PRECONDITIONS: For <Races> it is possible to place a bet from:
        PRECONDITIONS: - 'Next 4' module
        PRECONDITIONS: - event details page
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            events = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.selection_ids = [event.selection_ids[event.team1] for event in events]

        self.site.login()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        EXPECTED: * 'Reuse Selections' and 'Go Betting' buttons are present in the bottom area of Bet Receipt
        """
        self.check_bet_receipt_is_displayed()
        self.__class__.bet_receipt = self.site.bet_receipt
        if (self.brand == 'bma' and self.device_type == 'desktop') or self.brand == 'ladbrokes':
            self.assertTrue(self.bet_receipt.footer.has_reuse_selections_button(),
                            msg='Reuse Selection button is not displayed')
            self.assertTrue(self.bet_receipt.footer.has_done_button(),
                            msg='Go Betting button is not displayed, Bet was not placed')

    def test_002_scroll_the_page_down_and_up(self):
        """
        DESCRIPTION: Scroll the page down and up
        EXPECTED: * Bottom area with 'Reuse Selections' and 'Go Betting' buttons is sticky (for Coral only)
        EXPECTED: * Bottom area with 'Reuse Selections' and 'Go Betting' buttons is sticky (for Ladbrokes only)
        """
        self.bet_receipt.bet_receipt_sections_list.scroll_to_bottom()
        if (self.brand == 'bma' and self.device_type == 'desktop') or self.brand == 'ladbrokes':
            self.assertTrue(self.bet_receipt.footer.has_reuse_selections_button(),
                            msg='Reuse Selection button is not Sticky')
            self.assertTrue(self.bet_receipt.footer.has_done_button(),
                            msg='Go Betting button is not Sticky')

    def test_003_clicktap_reuse_selection_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Click/Tap 'Reuse Selection' button on Bet Receipt page
        EXPECTED: User is returned to the Betslip to initiate bet placement again on the same selection or selections
        """
        if (self.brand == 'bma' and self.device_type == 'desktop') or self.brand == 'ladbrokes':
            self.bet_receipt.footer.reuse_selection_button.click()
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=self.selection_ids)
            self.place_multiple_bet(number_of_stakes=1)

    def test_004_clicktap_go_betting_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Click/Tap 'Go Betting' button on Bet Receipt page
        EXPECTED: * BetSlip page closes
        EXPECTED: * 'Go Betting' button navigates to the last visited page
        """
        if (self.brand == 'bma' and self.device_type == 'desktop') or self.brand == 'ladbrokes':
            self.test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button()
            self.bet_receipt.footer.click_done()
            self.site.wait_content_state(state_name='Homepage')
