import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # need to create events
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.sanity
@pytest.mark.desktop
@vtest
class Test_C59550817_Verify_that_Bets_are_not_duplicated_during_bet_placement_with_Overask(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C59550817
    NAME: Verify that Bets are not duplicated during bet placement with Overask
    DESCRIPTION: This test case verifies that Bets are not duplicated during bet placement via Overask after selection change in Betslip
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask guides:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    """
    keep_browser_open = True
    max_bet = 0.3
    new_price = '3/1'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        """
        self.__class__.username = tests.settings.betplacement_user
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        self.__class__.selection_id = list(self.event.selection_ids.values())[0]

    def test_001__add_any_selection_from_eg_football_to_betslip_open_betslip(self):
        """
        DESCRIPTION: * Add any selection from e.g. Football to Betslip
        DESCRIPTION: * Open Betslip
        EXPECTED: Selection is present in Betslip
        """
        self.site.login(self.username)
        self.open_betslip_with_selections(self.selection_id)
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        betslip = self.get_betslip_content()
        selections_count = betslip.selections_count
        self.assertEqual(selections_count, betslip_counter,
                         msg=f'BetSlip counter in section name "{selections_count}" '
                             f'and counter "{selections_count}" doesn\'t match')
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.event.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found in "{singles_section.keys()}"')
        self.__class__.old_price = stake.odds

    def test_002_trigger_price_change_for_the_selection_inside_betslip(self):
        """
        DESCRIPTION: Trigger price change for the selection inside Betslip
        EXPECTED: Price change message is displayed in Betslip
        """
        self.ob_config.change_price(self.selection_id, price=self.new_price)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id)
        self.assertTrue(price_update, msg=f'Price is not updated for selection with id "{self.selection_id}"')
        singles_sections = self.get_betslip_sections().Singles
        stake = list(singles_sections.values())[0]
        expected_message = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(old=self.old_price,
                                                                     new=self.new_price)
        self.assertEqual(stake.error_message, expected_message,
                         msg=f'Actual price change message: "{stake.error_message}" '
                             f'is not equal to expected: "{expected_message}"')
        stake.remove_button.click()

    def test_003_remove_selection_from_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip
        EXPECTED: Betslip becomes empty and closes automatically
        """
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(), msg='BetSlip is not closed yet')
            self.site.open_betslip()
        no_selection_title = self.site.betslip.no_selections_title
        self.assertEqual(no_selection_title, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'"{no_selection_title}" is not same as expected '
                             f'"{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_004__add_anothersame_selection_from_eg_football_to_quickbet(self):
        """
        DESCRIPTION: * Add another/same selection from e.g. Football to Quickbet
        EXPECTED: Selection is present in Quickbet
        """
        self.__class__.expected_betslip_counter_value = 0
        if self.device_type == 'mobile':
            self.navigate_to_edp(event_id=self.event.event_id)
            bet_button = self.site.home.bet_buttons[0]
            self.assertTrue(bet_button, msg='No bet buttons present in the EDP')
            bet_button.click()
            self.site.wait_for_quick_bet_panel()
            selection_name = self.site.quick_bet_panel.selection.content.outcome_name
            expected_selection_name = list(self.event.selection_ids.keys())[0]
            self.assertEqual(selection_name, expected_selection_name, msg=f'Actual selection "{selection_name}" is not same as '
                                                                          f'Expected selection "{expected_selection_name}"')
        else:
            self.open_betslip_with_selections(self.selection_id)
            singles_section = self.get_betslip_sections().Singles
            stake = singles_section.get(self.event.team1)
            self.assertTrue(stake, msg=f'"{self.team1}" stake was not found in "{singles_section.keys()}"')

    def test_005__enter_a_stake_which_could_trigger_overask_bet_interception_tappress_place_bet_button(self):
        """
        DESCRIPTION: * Enter a stake which could trigger Overask Bet Interception
        DESCRIPTION: * Tap/Press 'Place bet' button
        EXPECTED: Betslip opens with Overask overlay is displayed
        """
        self.__class__.bet_amount = self.max_bet + 0.14
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
        else:
            self.place_single_bet()
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_006_open_related_tinavigate_to_bet__bi_requests__results_tab(self):
        """
        DESCRIPTION: Open related TI
        DESCRIPTION: Navigate to Bet > BI Requests > 'Results' tab
        EXPECTED: Only one request from the user is present in the list
        """
        # cannot automate OB front end

    def test_007__accept_the_bet_by_trader_observe_result_in_app(self):
        """
        DESCRIPTION: * Accept the bet by trader
        DESCRIPTION: * Observe result in app
        EXPECTED: Bet receipt is displayed with correct bet information
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.event.event_id)
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.check_bet_receipt_is_displayed()
        stake = self.site.bet_receipt.footer.total_stake
        self.assertEqual(str(stake), str(self.bet_amount), msg=f'Actual stake "{stake}" is not same as '
                                                               f'Expected stake "{self.bet_amount}"')
        returns = self.site.bet_receipt.footer.total_estimate_returns
        self.verify_estimated_returns(est_returns=returns, odds=self.new_price, bet_amount=self.bet_amount)
        self.site.bet_receipt.footer.click_done()

    def test_008_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        EXPECTED: Only one new bet from the user is present
        """
        event_name = self.event.team1, ' v ', self.event.team2
        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=event_name)
        self.assertTrue(bet, msg='Bet is not present')
