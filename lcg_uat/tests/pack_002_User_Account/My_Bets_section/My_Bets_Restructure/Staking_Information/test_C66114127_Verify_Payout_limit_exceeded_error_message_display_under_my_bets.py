import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.staking_information
@vtest
class Test_C66114127_Verify_Payout_limit_exceeded_error_message_display_under_my_bets(BaseBetSlipTest):
    """
    TR_ID: C66114127
    NAME: Verify Payout limit exceeded error message display under my bets
    DESCRIPTION: This test case is to verify Payout limit exceeded error message display
    PRECONDITIONS: 1.Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2.Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3.Max Pay Out banner should be enabled in CMS
    """
    keep_browser_open = True
    bet_amount = 0.50
    selection_ids = {}

    def verify_max_payout_message(self, bet=None, tab_name=None):
        self.assertTrue(bet.has_max_payout_msg(expected_result=True),
                        msg=f'Payout limit exceeded, for more info click here message is not displayed under {tab_name}')
        self.assertTrue(bet.has_max_payout_link(expected_result=True),
                        msg=f'For more info click here link is not displayed under {tab_name}')

        bet.chevron_arrow.click()
        self.assertFalse(bet.is_expanded(expected_result=False),
                         msg=f'Bet is not collapsed after clicking on chevron arrow under {tab_name}')

        self.assertFalse(bet.has_max_payout_msg(expected_result=False),
                        msg=f'Payout limit exceeded, for more info click here message is displayed under {tab_name}')
        self.assertFalse(bet.has_max_payout_link(expected_result=False),
                        msg=f'For more info click here link is displayed under {tab_name}')

        bet.chevron_arrow.click()
        self.assertTrue(bet.is_expanded(expected_result=True),
                         msg=f'Bet is not expanded after clicking on chevron arrow under {tab_name}')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 20 Selections are required
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     all_available_events=True)
        for event in events:
            market = next((market for market in event['event']['children'] if market['market'].get('children') and market['market']['templateMarketName'] == 'Match Betting'), None)
            outcomes_resp = market['market']['children']
            for outcome in outcomes_resp:
                if outcome['outcome']['children'][0]['price']['priceDen'] == '1' and int(
                        outcome['outcome']['children'][0]['price']['priceNum']) < 100 and 'Unnamed' not in \
                        outcome['outcome']['name'] and outcome['outcome']['children'][0]['price']['priceNum'] not in self.selection_ids.values():
                    self.selection_ids[outcome['outcome']['id']] = outcome['outcome']['children'][0]['price']['priceNum']
                    break
            if len(self.selection_ids.keys()) == 19:
                break

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
        """
        self.site.login()

    def test_002_log_into_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Log into the application with valid credentials
        EXPECTED: User should be able to login
        """
        # Covered in above step

    def test_003_go_to_any_sport_from_sports_ribbona_z_menu(self):
        """
        DESCRIPTION: Go to any sport from Sports ribbon/A-z menu
        EXPECTED: User should be able to navigate to sport landing page
        """
        # Covered in above step

    def test_004_click_on_any_selection_from_any_event(self):
        """
        DESCRIPTION: Click on any selection from any event
        EXPECTED: Desktop: Selection should be added to betslip  Mobile: Click on add to betslip is quick bet overlay (quick bet should popup first)
        """
        selections = ''.join(['%s,' % selection for selection in self.selection_ids.keys()]).rstrip(',')
        url = f'https://{tests.HOSTNAME}/betslip/add/{selections}'
        self.device.navigate_to(url=url)
        self.site.wait_splash_to_hide(timeout=60)
        if self.device_type == 'mobile':
            self.site.has_betslip_opened()

    def test_005_enter_stake_amount_and_validate_the_display_of_max_payout_banner__entered_stake_should_trigger_the_estimatedpotential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Enter stake amount and validate the display of Max payout banner  (Entered stake should trigger the estimated/potential returns higher than Maximum Payout configured)
        EXPECTED: Payout limit exceeded, for more info' message should be display along with  click here and 'i' signpsoting
        """
        multiples_sections = list(self.get_betslip_sections(multiples=True).Multiples.values())
        stake_name, stake = next(([section.outcome_name, section] for section in multiples_sections if float(section.odds.split('/')[0]) > 300000), [None, None])
        if stake is None or stake_name is None:
            raise SiteServeException('There are no selections available to get potential returns more than 100000')
        self.enter_stake_amount(stake=(stake_name, stake))
        betslip = self.get_betslip_content()
        self.assertTrue(betslip.has_max_payout_msg(expected_result=True), msg=f'Payout limit exceeded, for more info click here message is not displayed')
        self.assertTrue(betslip.has_max_payout_link(expected_result=True), msg=f'For more info click here link is not displayed')
        betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_006_click_on_place_bet_and_verify(self):
        """
        DESCRIPTION: Click on place bet and verify
        EXPECTED: Bet placement should happened successfully
        """
        # Covered in above step

    def test_007_navigate_to_my_bets_section(self):
        """
        DESCRIPTION: Navigate to My bets section
        EXPECTED: Open tab should display and selected by default
        """
        # Covered in above step

    def test_008_verify_the_max_tool_tip_for_placed_bet_in_open_and_cashout_tabs(self):
        """
        DESCRIPTION: Verify the max tool tip for placed bet in OPEN and Cashout Tabs
        EXPECTED: Payout limit exceeded, for more info' message should be display along with  'click here' hyperlink and 'i' signpsoting
        EXPECTED: Note:Max payout tool tip(i) should not display  displayed in collapse state.
        EXPECTED: ![](index.php?/attachments/get/5d26e7b9-7ecf-4cd0-a8bf-d34bbe36525d)
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_max_payout_message(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_max_payout_message(bet=cash_out_bet, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_max_payout_message(bet=settled_bet, tab_name='Settled tab')

    def test_009_verify_the_bet_in_settled_tab_once_it_is_resulted_in_both_expandedcollapsed_state(self):
        """
        DESCRIPTION: Verify the bet in Settled tab Once it is resulted in both expanded/Collapsed state
        EXPECTED: Payout limit exceeded, for more info' message should be display along with  'click here' Hyperlink and 'i' signpsoting  Note:Max payout tool tip(i) should not display  displayed in collapse state.
        """
        # Covered in above step

    def test_010_repeat_the_step_3_to_step_9_by_placing_bets_in_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat the step 3 to step 9 by placing bets in lottos and pools along with races
        EXPECTED: Result should be same as above
        """
        pass
