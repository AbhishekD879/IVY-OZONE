import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-55182')  # Coral only
@vtest
class Test_C29007_Bet_Slip_Icon(BaseBetSlipTest):
    """
    TR_ID: C29007
    TR_ID: C16379429
    VOL_ID: C9698244
    NAME: Verifying that betslip counter increases with each bet
    DESCRIPTION: This scenario verifies functionality of Bet slip icon which is shown after a user has added a selection to the Bet Slip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add test events
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=2)
            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.event_id = events[0]['event']['id']
            self.__class__.event2_name = events[1]['event']['name']
            self.__class__.event2_id = events[1]['event']['id']
            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=events[0])
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=events[1])
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
            self.__class__.event_id = event_params.event_id
            event2_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event2_id = event2_params.event_id
            self.__class__.event2_name = f'{event2_params.team1} v {event2_params.team2}'
            self.__class__.league1 = self.__class__.league2 = tests.settings.football_autotest_league

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that do not have enough money to place bet
        """
        self.site.login()

    def test_002_tap_sport(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL', timeout=3)

    def test_003_make_selection(self):
        """
        DESCRIPTION: Add selection to betslip. Betslip counter is increased to value which is equal to quantity of added selections
        """
        self.__class__.expected_betslip_counter_value = 0
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event {self.event_name}')
        for count, (name, price) in enumerate(list(output_prices.items()), 1):
            price.click()
            if count == 1:
                self.site.add_first_selection_from_quick_bet_to_betslip()
                self.assertTrue(price.is_selected(timeout=4),
                                msg=f'Output price "{name}" is not highlighted after selection')
            self.assertTrue(price.is_selected(timeout=3),
                            msg=f'Output price "{name}" is not highlighted after selection')

            self.__class__.expected_betslip_counter_value += 1
            self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_004_deselect_all_selections(self):
        """
        DESCRIPTION: Remove all selections. Verify that Betslip counter == 0
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event {self.event_name}')

        for name, price in output_prices.items():
            price.click()
            self.assertFalse(price.is_selected(expected_result=False, timeout=2),
                             msg=f'Output price {name} is highlighted after deselection')

            self.__class__.expected_betslip_counter_value -= 1
            self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        self.verify_betslip_counter_change(expected_value=0)

    def test_005_make_single_selection(self):
        """
        DESCRIPTION: Make single selection
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event {self.event_name}')
        name, price = list(output_prices.items())[0]
        price.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(price.is_selected(timeout=4),
                        msg=f'Output price {name} is not highlighted after selection')

        self.__class__.expected_betslip_counter_value += 1
        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_006_go_to_betslip(self):
        """
        DESCRIPTION: Go to the BetSlip and place bet. Verify that Betslip counter decrease to 0
        """
        self.site.header.bet_slip_counter.click()
        self.site.close_all_dialogs()
        self.place_single_bet()
        self.site.bet_receipt.footer.click_done()

        self.verify_betslip_counter_change(expected_value=0)
        self.__class__.expected_betslip_counter_value -= 1

    def test_007_make_multiple_selection(self):
        """
        DESCRIPTION: Add selection to betslip. Betslip counter is increased to value which is equal to quantity of added selections
        """
        self.navigate_to_page(name='/sport/football')
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event {self.event_name}')
        event2 = self.get_event_from_league(event_id=self.event2_id,
                                            section_name=self.league2)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2,
                        msg=f'Could not find output prices for created event {self.event2_name}')
        name, price = list(output_prices.items())[0]
        name2, price2 = list(output_prices2.items())[0]
        price.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(price.is_selected(timeout=4),
                        msg=f'Output price "{name}"" is not highlighted after selection')
        self.site.wait_for_quick_bet_panel(expected_result=False)
        price2.click()
        self.assertTrue(price2.is_selected(timeout=2),
                        msg=f'Output price "{name2}" is not highlighted after selection')

        self.__class__.expected_betslip_counter_value += 2
        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_008_go_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Go to BetSlip and place a bet
        """
        self.site.header.bet_slip_counter.click()
        self.place_multiple_bet()
        self.site.bet_receipt.footer.click_done()

        self.verify_betslip_counter_change(expected_value=0)
