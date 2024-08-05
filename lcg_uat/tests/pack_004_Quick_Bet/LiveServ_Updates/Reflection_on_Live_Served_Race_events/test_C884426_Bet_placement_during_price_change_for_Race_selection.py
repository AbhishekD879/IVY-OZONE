import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.racing
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C884426_Bet_placement_during_price_change_for_Race_selection(BaseRacing):
    """
    TR_ID: C884426
    VOL_ID: C9697712
    NAME: Bet placement during price change for Race selection
    DESCRIPTION: This test case verifies Quick Bet reflection on <Race> events simultaneously with bet placement when price is changed
    PRECONDITIONS: 1. User is logged in with positive balance
    PRECONDITIONS: 2. Price updates are received in Betslip microservice:
    PRECONDITIONS: Development tool> Network> WS> quickbet/?EIO=3&transport=websocket
    PRECONDITIONS: 3. Price updates can be received for LP priced selections
    """
    keep_browser_open = True

    prices = {0: '6/17'}
    selection = None
    new_price = '1/8'
    quick_bet = None

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Go to the racing event details page
        DESCRIPTION: Make single selections where price is LP
        EXPECTED: Event details page is opened
        EXPECTED: Quick Bet is opened with selection added
        """
        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1, lp_prices=self.prices)
        self.__class__.selection = list(event.selection_ids.values())[0]
        self.navigate_to_edp(event_id=event.event_id, sport_name='horse-racing')
        self.site.login()
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        stake_name, outcome = list(outcomes.items())[0]
        outcome.bet_button.click()
        self.device.driver.implicitly_wait(1)  # VOL-1107
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')

    def test_002_enter_stake_value_for_selection(self):
        """
        DESCRIPTION: Enter stake value for selection
        DESCRIPTION: In Backoffice tool change price for selection and save changes
        DESCRIPTION: In the same time while changes in Backoffice are not saved > Tap 'PLACE BET' button
        EXPECTED: Stake value is entered
        """
        quick_bet = self.site.quick_bet_panel
        quick_bet.selection.content.amount_form.input.value = '0.01'
        place_bet = quick_bet.place_bet

        self.ob_config.change_price(selection_id=self.selection, price=self.new_price)
        place_bet.click()

    def test_003_check_error_message(self):
        """
        DESCRIPTION: Check Error Message on Quick Bet
        EXPECTED: 'Price changed from 'n' to 'n'' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: 'ADD TO BETSLIP' and 'ACCEPT & PLACE BET' buttons are enabled
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{self.selection}" is not received')

        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(), msg='LOGIN & PLACE BET button is disabled')
        error_message = self.site.quick_bet_panel.info_panels_text
        actual_message = error_message[0]
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=list(self.prices.values())[0], new=self.new_price)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                        msg='"ACCEPT & PLACE BET" button is not enabled')

    def test_004_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'PLACE BET' button
        EXPECTED: Spinner appears instead of label 'ACCEPT & PLACE BET'.
        EXPECTED: Bet is placed successfully and Bet receipt is shown.
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
