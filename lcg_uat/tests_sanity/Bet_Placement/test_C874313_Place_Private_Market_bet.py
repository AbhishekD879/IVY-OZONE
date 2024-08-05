import tests
import pytest
from tests.base_test import vtest
from crlat_ob_client.offer import Offer
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from crlat_ob_client.utils.date_time import validate_time
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - Private markets can not be configured on prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_placement
@pytest.mark.private_markets
@pytest.mark.desktop
@vtest
class Test_C874313_Place_Private_Market_bet(BasePrivateMarketsTest, BaseUserAccountTest):
    """
    TR_ID: C874313
    NAME: Place Private Market bet
    DESCRIPTION: Verify that the customer can see Private Markets and can bet on Private Markets
    PRECONDITIONS: Make sure that the Private Markets Offer is valid
    PRECONDITIONS: Make sure that the customer is qualified to see the Private Market
    PRECONDITIONS: Login to Oxygen
    PRECONDITIONS: NOTE: Production/HL users: In order to create a user with an available private market, without the need to use OB Prod backoffice, follow guidelines here:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets
    """
    keep_browser_open = True
    expected_currency = '£'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Make sure that the Private Markets Offer is valid
        PRECONDITIONS: Make sure that the customer is qualified to see the Private Market
        PRECONDITIONS: Login to Oxygen
        """
        user = tests.settings.betplacement_user
        self.site.login(username=user)
        offer_id = self.ob_config.backend.ob.private_market_offer.offer_id
        offer = Offer(env=tests.settings.backend_env, brand=self.brand)
        self.trigger_private_market_appearance(
            user=user,
            expected_market_name=self.private_market_name)
        offer.give_offer(username=user, offer_id=offer_id)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('homepage')

        self.__class__.tab_name = self.expected_sport_tabs.private_market.upper()

    def test_001_check_that_the_private_market_is_available_on_homepage(self):
        """
        DESCRIPTION: Check that the Private Market is available on Homepage
        EXPECTED: * The customer can see the Private Market in the first 'Your Enhanced Markets' tab selected by default **For Mobile/Tablet**
        EXPECTED: * The customer can see the Private Market in the first 'Your Enhanced Markets' section at the Homepage **For Desktop**
        """
        self.site.wait_content_state_changed()
        if self.device_type != 'desktop':
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='"No tabs" are displayed at the Home page')
            self.assertIn(self.tab_name, tabs.keys(), msg=f'Tab "{self.tab_name}" was not found in the '
                                                          f'tabs list: "{tabs.keys()}"')
            self.assertTrue(tabs[self.tab_name].is_selected(), msg=f'"{self.tab_name}" tab is not selected by default')
        else:
            self.assertTrue(self.site.home.get_module_content(self.expected_sport_tabs.private_market),
                            msg=f'Module "{self.expected_sport_tabs.private_market}" is not present')

    def test_002_add_one_selection_from_the_private_market_to_bet_slip(self):
        """
        DESCRIPTION: Add one selection from the Private Market to bet slip
        EXPECTED: The customer is able to add selection from private market to bet slip
        """
        pm_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        markets = pm_tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='"No markets" found')
        market = markets.get(self.private_market_name.upper())
        self.assertTrue(market, msg=f'"{self.private_market_name.upper()}" was not found among markets: "{markets}"')
        market.show_all_button.click()
        wait_for_result(lambda: self.private_outcome_name in market.items_as_ordered_dict,
                        timeout=3)

        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='"No outcomes" are displayed')
        self.assertIn(self.private_outcome_name, outcomes.keys(),
                      msg=f'Outcome "{self.private_outcome_name}" was not found in the '
                          f'outcomes list: "{outcomes.keys()}"')
        outcomes[self.private_outcome_name].bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()

            self.verify_betslip_counter_change(expected_value=1)

    def test_003_navigate_to_bet_slip(self):
        """
        DESCRIPTION: Navigate to bet slip
        EXPECTED: The selection was correctly added to bet slip
        """
        self.site.open_betslip()
        self.assertIn(self.private_outcome_name, self.get_betslip_sections().Singles,
                      msg=f'No section "{self.private_outcome_name}" in Betslip')
        section = self.get_betslip_sections().Singles[self.private_outcome_name]
        self.assertTrue(section, msg=f'Outcome "{self.outcome_name}" is not found in Betslip')

    def test_004_add_a_stake_and_click_on_bet_now_button_from_ox_99___place_bet_button(self):
        """
        DESCRIPTION: Add a stake and click on "Bet Now" button (From OX 99 - "Place Bet" button)
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is in £.
        """
        self.__class__.bet_info = self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_005_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Time and Event is displayed;
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        self.check_bet_receipt(betslip_info=self.bet_info)

        self.__class__.bet_receipt = self.site.bet_receipt
        bet_receipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='"No BetReceipt sections" found.')
        single_section = bet_receipt_sections.get(vec.betslip.SINGLE)
        self.assertTrue(single_section, msg='"No Single sections" found.')
        selections = single_section.items_as_ordered_dict
        self.assertTrue(selections, msg='"No stakes" found in singles section.')
        _, selection = list(selections.items())[0]

        currency = selection.stake_currency
        self.assertEqual(currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{currency}" instead.')
        self.assertTrue(self.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Bet receipt has no "Reuse Selection" button.')
        self.assertTrue(self.bet_receipt.footer.has_done_button(),
                        msg='Bet receipt has no "Done" button.')

    def test_006_click_on_done_button(self):
        """
        DESCRIPTION: Click on Done button
        EXPECTED: The customer stays on the Homepage
        """
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('Homepage')

    def test_007_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: The private market is no longer available
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed()

        if self.device_type != 'desktop':
            sections = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(sections, msg='"No tabs" are displayed at the Home page')
        else:
            sections = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(sections, msg='"Desktop sections" are not present')

        try:
            pm_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
            markets = pm_tab_content.accordions_list.items_as_ordered_dict
            # added softAssert here because the availablity of Private market depeneds on number of offers present for user
            self.softAssert(self.assertNotIn, self.private_market_name.upper(), markets,
                            msg=f'Market "{self.private_market_name.upper()}" still is present in "{markets.keys()}"')
        except VoltronException:
            # added softAssert here because the availablity of Your Enhanced Markets depeneds on number of offers present for user
            self.softAssert(self.assertNotIn, self.tab_name, sections.keys(),
                            msg=f'Tab "{self.tab_name}" was still found in the tab list: "{sections.keys()}"')

    def test_008_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: My Bets page is opened
        """
        self.site.open_my_bets_open_bets()
        if self.device_type == 'mobile':
            self.site.wait_content_state('open-bets')

    def test_009_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: **Bet Receipt unique ID
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: **Correct Stake is correctly displayed;
        """
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name)

        bet_info = self.bet_info.get(self.private_outcome_name)
        self.assertEqual(single_bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type: "{single_bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertEqual(single_bet.selection_name, self.private_outcome_name,
                         msg=f'Selection Name: "{single_bet.selection_name}" '
                             f'is not as expected: "{self.private_outcome_name}"')
        self.assertEqual(single_bet.odds_value, bet_info.get('odds'),
                         msg=f'Odds value: "{single_bet.odds_value}" '
                             f'is not as expected: "{bet_info.get("odds")}"')
        self.assertEqual(single_bet.event_name, self.event_name,
                         msg=f'Event Name: "{single_bet.event_name}" '
                             f'is not as expected: "{self.event_name}"')
        self.assertEqual(single_bet.market_name, bet_info.get('market_name'),
                         msg=f'Bet market name: "{single_bet.market_name}" '
                             f'is not as expected: "{bet_info.get("market_name")}"')
        expected_stake = f'£{self.bet_amount}'
        self.assertEqual(single_bet.stake.value, expected_stake,
                         msg=f'Bet Stake value: "{single_bet.stake.value}" '
                             f'is not as expected: "{expected_stake}"')

        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        _, betleg = list(bet_legs.items())[0]
        validate_time(actual_time=betleg.event_time, format_pattern=self.event_card_future_time_format_pattern)
