import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.racing
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@vtest
class Test_C883644_Reflection_on_Race_Price_Changed_for_live_served_events(BaseRacing):
    """
    TR_ID: C883644
    VOL_ID: C9698433
    NAME: Reflection on Race Price Changed for live served events
    DESCRIPTION: This test case verifies Quick Bet reflection on Race Price Changed.
    PRECONDITIONS: 1. To get SiteServer info about event use the following URL: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Race> Event should be LiveServed:
    PRECONDITIONS: Event should not be 'Live' ('isStarted' - absent)
    PRECONDITIONS: Event, Market, Outcome should be Active
    PRECONDITIONS: 4. Price format should be Fractional
    PRECONDITIONS: 5. Link to backoffice tool for price changing: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 6. Price updates are received in Quick Bet microservice:
    PRECONDITIONS: Development tool> Network> WS> quickbet/?EIO=3&transport=websocket
    PRECONDITIONS: NOTE: test case may be run for selections with LP price
    """
    keep_browser_open = True
    prices = {0: '1/6'}
    selection = None
    decreased_price = '1/8'
    increased_price = '1/4'
    quick_bet = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1, lp_prices=self.prices)
        self.__class__.eventID = event.event_id
        self.__class__.selection = list(event.selection_ids.values())[0]

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Go to the racing event details page
        DESCRIPTION: Make single selections where price is LP
        EXPECTED: Event details page is opened
        EXPECTED: Quick Bet is opened with selection added
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        stake_name, outcome = list(outcomes.items())[0]
        outcome.bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')

        self.device.driver.implicitly_wait(1)  # VOL-1107
        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content

    def test_002_increase_price_for_the_selection_in_backoffice_tool(self):
        """
        DESCRIPTION: Increase price for the selection in Backoffice tool
        """
        self.__class__.old_price = self.site.quick_bet_panel.selection.content.odds_value
        self.ob_config.change_price(selection_id=self.selection, price=self.increased_price)

    def test_003_check_price_displaying_in_quick_bet(self):
        """
        DESCRIPTION: Check price displaying in Quick Bet
        EXPECTED: Old Odds are instantly changed to New Odds
        EXPECTED: When clicked into, dropdown shows both updated Odds value and 'SP' value as selectable options
        EXPECTED: NOTE: Price corresponds to value received in 'remotebetslip/?EIO=3&transport=websocket' response
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{self.selection}" is not received')

        quick_bet = self.site.quick_bet_panel.selection.content
        result = wait_for_result(lambda: self.increased_price in quick_bet.odds_value,
                                 name='Odd changes',
                                 timeout=3)

        self.assertTrue(result, msg=f'Old Odd "{quick_bet.odds_value}" is not instantly changed to "{self.increased_price}"')

        odds = self.quick_bet.odds
        self.assertEqual(odds, self.increased_price,
                         msg=f'Actual price "{odds}" is not the same as expected "{self.increased_price}"')

        odds_dropdown = self.site.quick_bet_panel.selection.content.odds_dropdown
        self.assertTrue(odds_dropdown, msg='No odds dropdown found in Quick Bet')
        odds_dropdown.click()
        self.assertTrue(odds_dropdown.is_expanded(), msg='Odds dropdown is not expanded')
        values = odds_dropdown.items_as_ordered_dict
        for odd in [self.increased_price, 'SP']:
            self.assertIn(odd, values.keys(), msg=f'Odd value "{odd}" is not selectable option in "{values.keys()}"')
        odds_dropdown.click()
        self.assertFalse(odds_dropdown.is_expanded(expected_result=False), msg='Odds dropdown is not expanded')

    def test_004_verify_warning_message_and_login_place_bet_button_displaying(self):
        """
        DESCRIPTION: Verify warning message and 'LOGIN & PLACE BET' button displaying
        EXPECTED: * 'Price changed from 'n' to 'n'' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: * 'LOGIN & PLACE BET' button is disabled
        """
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        self.device.driver.implicitly_wait(0)  # VOL-1107
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=self.old_price, new=self.increased_price)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')

    def test_005_enter_stake_in_stake_field_and_trigger_price_change(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and trigger price change
        EXPECTED: 1.Old Odds are instantly changed to New Odds
        EXPECTED: - When clicked into, dropdown shows both updated Odds value and 'SP' value as selectable
        EXPECTED: 2.'Price changed from 'n' to 'n'' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: 3.Est. Returns and Total Est. Returns should be recalculated
        EXPECTED: 4.'LOGIN & PLACE BET' button becomes enabled
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = '0.01'

        self.ob_config.change_price(selection_id=self.selection, price=self.decreased_price)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection, price=self.decreased_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{self.selection}" is not received')

        quick_bet = self.site.quick_bet_panel.selection.content
        odds = quick_bet.odds
        self.assertEqual(odds, self.decreased_price, msg=f'Actual price "{odds}" '
                                                         f'is not the same as expected "{self.decreased_price}"')

        result = wait_for_result(lambda: self.decreased_price in quick_bet.odds_value,
                                 name='Odd changes',
                                 timeout=2)
        self.assertTrue(result, msg=f'Old Odd "{quick_bet.odds_value}" is not instantly changed to "{self.decreased_price}"')

        odds_dropdown = self.site.quick_bet_panel.selection.content.odds_dropdown
        self.assertTrue(odds_dropdown, msg='No odds dropdown found in Quick Bet')
        odds_dropdown.click()
        self.assertTrue(odds_dropdown.is_expanded(), msg='Odds dropdown is not expanded')
        values = odds_dropdown.items_as_ordered_dict
        for odd in [self.decreased_price, 'SP']:
            self.assertIn(odd, values.keys(), msg=f'Odd value "{odd}" is not selectable option in "{values.keys()}"')

        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=self.increased_price, new=self.decreased_price)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')
