import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
# @pytest.mark.stg2 - #TODO VOL-2175
# @pytest.mark.prod - Can't be executed now, not sure if Private markets can be configured on prod
# @pytest.mark.hl
@pytest.mark.smoke
@pytest.mark.user_journey_new_customer
@pytest.mark.private_markets
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.promotions_banners_offers
@pytest.mark.login
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-2175')
class Test_C29436_Bet_Placement_on_Private_Markets(BasePrivateMarketsTest, BaseUserAccountTest):
    """
    TR_ID: C29436
    NAME: Bet Placement on Private Markets
    DESCRIPTION: This test case verifies Bet Placement on Private Markets.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market
    PRECONDITIONS:     for particular user after a page refresh or navigating to Homepage from any other page and
    PRECONDITIONS:     **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: 3.  User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 5.  Private market offers should be active (not expired)
    """
    keep_browser_open = True
    odds = '1/2'
    stake = '0.03'
    est_return = '0.05'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Places a bet again on the event which triggers Private Market appearance
        """
        self.__class__.user = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.user, amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.user, async_close_dialogs=False)
        self.trigger_private_market_appearance(
            user=self.user,
            expected_market_name=self.private_market_name)

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        EXPECTED: 'Your Enhanced Markets' tab is present and selected by default for mobile/tablet
        EXPECTED: 'Your Enhanced Markets' section is present at the top of the page (below Hero Header) for mobile/tablet
        EXPECTED: All eligible private markets and associated selections are shown
        """
        if self.device_type != 'desktop':
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='No tabs are displayed at the Home page')

            tab_name = self.expected_sport_tabs.private_market
            self.assertIn(tab_name, tabs.keys(), msg=f'Tab "{tab_name}" is not displayed for the user')
            self.assertTrue(tabs[tab_name].is_selected(), msg=f'"{tab_name}" tab is not selected by default')
        else:
            sections = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(sections, msg='Desktop sections are not present')
            self.__class__.private_market_section = sections.get(self.expected_sport_tabs.private_market)
            self.assertTrue(self.private_market_section,
                            msg=f'Section "{self.expected_sport_tabs.private_market}" is not '
                                f'present in "{sections.keys()}"')
            index = 1 if self.site.home.desktop_modules.is_enhanced_module_displayed(timeout=1) else 0  # enhanced module is always on top of all modules
            first_top_section_name = list(sections.keys())[index]
            self.assertEqual(first_top_section_name, self.expected_sport_tabs.private_market,
                             msg=f'Section "{self.expected_sport_tabs.private_market}" is not placed at the '
                                 f'top of the page, instead "{first_top_section_name}" is placed')

    def test_002_add_selection_from_private_market_to_the_Betslip(self):
        """
        DESCRIPTION: Add selection from private market to the Betslip
        EXPECTED: Selection is added
        EXPECTED: Betslip counter is increased for mobile/tablet
        """
        private_market_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        markets = private_market_tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='Private markets is not found')
        market = markets.get(self.private_market_name.upper())
        self.assertTrue(market, msg=f'Market "{self.private_market_name.upper()}" not found in "{markets.keys()}"')
        if market.has_show_all_button:
            market.show_all_button.click()
        wait_for_result(lambda: self.private_outcome_name in market.items_as_ordered_dict,
                        timeout=3)

        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes are displayed')
        self.assertIn(self.private_outcome_name, outcomes.keys(), msg=f'Outcome "{self.private_outcome_name}" is not displayed')
        outcomes[self.private_outcome_name].bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()

            self.verify_betslip_counter_change(expected_value=1)

    def test_003_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip page is opened
        EXPECTED: Added selection is displayed
        """
        self.site.open_betslip()
        self.assertIn(self.private_outcome_name, self.get_betslip_sections().Singles,
                      msg=f'No section "{self.private_outcome_name}" in Betslip')
        self.__class__.section = self.get_betslip_sections().Singles[self.private_outcome_name]
        self.assertTrue(self.section, msg=f'Outcome "{self.private_outcome_name}" is not found in Betslip')

    def test_004_verify_added_selection_correctness(self):
        """
        DESCRIPTION: Verify added selection are correct and correspond to the information in response from SS:
        EXPECTED: *   Selection name
        EXPECTED: *   Market name
        EXPECTED: *   Event start time and name
        EXPECTED: *   Odds
        """
        self.assertEqual(self.section.outcome_name, self.private_outcome_name,
                         msg=f'Actual selection name: "{self.section.outcome_name}", '
                             f'is not equal to expected: "{self.private_outcome_name}"')
        self.assertEqual(self.section.market_name, self.private_market_name,
                         msg=f'Actual market name: "{self.section.market_name}", '
                             f'is not equal to expected: "{self.private_market_name}"')
        self.assertEqual(self.section.odds, self.odds,
                         msg=f'Actual odds: "{self.section.odds}", are not equal to expected: "{self.odds}"')

    def test_005_enter_valid_stake_in_stake_field(self):
        """
        DESCRIPTION: Enter valid stake in 'Stake' field
        """
        self.section.amount_form.input.value = self.stake

    def test_006_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is shown
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_007_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: 1. Bet Receipt contains the following information:
        EXPECTED: *   header 'Singles' with the total number of single bets - i.e. Singles (1)
        EXPECTED: *   the selection made by the customer - i.e. outcome (display the outcome name)
        EXPECTED: *   the market type user has bet on - i.e. Win or Each Way
        EXPECTED: *   the event name to which the outcome belongs to
        EXPECTED: *   the Bet ID. The Bet ID is start with O and contain numeric values - i.e. O/0123828/0000155
        EXPECTED: *   'i' icon
        EXPECTED: *   Odds of the selection (for <Race> with 'SP' price - N/A)
        EXPECTED: *   Stake
        EXPECTED: *   Est. Returns (for <Race> with 'SP' price - N/A)
        EXPECTED: *   Total Stake
        EXPECTED: *   Total Est. Returns (for <Race> with 'SP' price - N/A)
        EXPECTED: *   'Reuse Selection' and 'Done' buttons
        EXPECTED: 2. Information in Bet Receipt corresponds to placed bet information
        """
        bet_receipt = self.site.bet_receipt
        section = vec.betslip.BETSLIP_SINGLES_NAME.title()
        bet_receipt_name = bet_receipt.bet_receipt_sections_list.items_as_ordered_dict[section].name
        self.assertEqual(bet_receipt_name, f'{section}',
                         msg=f'Actual Bet Receipt Name "{bet_receipt_name}" does not match expected "{section} (1)"')

        bet_receipt_info = bet_receipt.bet_receipt_sections_list.items_as_ordered_dict[section] \
                                                                .items_as_ordered_dict[self.private_outcome_name]
        self.assertEqual(bet_receipt_info.name, self.private_outcome_name,
                         msg=f'Actual Outcome Name "{bet_receipt_info.name}" does not match expected "{self.private_outcome_name}"')
        self.assertEqual(bet_receipt_info.event_market, self.private_market_name,
                         msg=f'Actual Market Name "{bet_receipt_info.event_market}" does not match expected "{self.private_market_name}"')
        self.assertEqual(bet_receipt_info.event_name, self.event_name,
                         msg=f'Actual Event Name "{bet_receipt_info.event_name}" does not match expected "{self.event_name}"')
        self.assertTrue(bet_receipt_info.bet_id, msg='Bet id is not shown')
        self.assertEqual(bet_receipt_info.odds, self.odds,
                         msg=f'Actual odds "{bet_receipt_info.odds}" does not match expected "{self.odds}"')
        self.assertEqual(str(bet_receipt_info.total_stake), str(self.bet_amount),
                         msg=f'Actual Total Stake "{bet_receipt_info.total_stake}" does not match expected "{self.bet_amount}"')
        self.assertEqual(bet_receipt_info.estimate_returns, self.est_return,
                         msg=f'Actual Est Returns "{bet_receipt_info.estimate_returns}" does not match expected "{self.est_return}"')
        bet_receipt_footer = bet_receipt.footer
        self.assertEqual(float(bet_receipt_footer.total_stake), float(self.bet_amount),
                         msg=f'Actual Total Stake "{bet_receipt_footer.total_stake}" does not match expected "{self.bet_amount}" (Footer)')
        self.assertEqual(bet_receipt_footer.total_estimate_returns, self.est_return,
                         msg=f'Actual Est Returns "{bet_receipt_footer.total_estimate_returns}" does not match expected'
                             f' "{self.est_return}" (Footer)')
        self.assertTrue(bet_receipt_footer.reuse_selection_button.is_displayed(),
                        msg='"Reuse Selection" button is not displayed')
        self.assertTrue(bet_receipt_footer.done_button.is_displayed(), msg='"Done" button is not displayed.')

    def test_008_check_placed_bet_correctness_in_ob_backoffice_using_the_bet_receipt_number(self):
        """
        DESCRIPTION: Check placed bet correctness in OB Backoffice using the Bet Receipt number
        EXPECTED: Information should be correct
        """
        pass

    def test_009_add_a_few_selections_to_the_betslip_from_different_private_markets(self):
        """
        DESCRIPTION: Add a few selections to the Betslip from different private markets
        EXPECTED: *   Selections are added
        EXPECTED: *   Betslip counter is increased
        """
        pass  # need different markets

    def test_010_repeat_steps_3_9(self):
        """
        DESCRIPTION: Repeat steps #3-9
        """
        pass

    # URL for manual triggering in case of any problems
    # 'https://invictus.coral.co.uk/event/football/football-auto-test/autotest-premier-league/auto-test-private-tonyland-v-auto-test-south-scott/8536689/main-markets'
