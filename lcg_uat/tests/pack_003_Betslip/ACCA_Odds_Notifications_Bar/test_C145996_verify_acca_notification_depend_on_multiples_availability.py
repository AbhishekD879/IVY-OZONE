from collections import OrderedDict
from random import choice

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.safari
@vtest
class Test_C145996_Verify_Acca_Notification_Depend_On_Multiples_Availability(BaseBetSlipTest):
    """
    TR_ID: C145996
    VOL_ID: C9698710
    NAME: Verify ACCA Odds Notification message displaying depend on Multiples availability in the Betslip
    """
    keep_browser_open = True
    events = OrderedDict()
    leagues = []

    def verify_acca_notification_presence(self, expected_result=True):
        result = self.site.wait_for_acca_notification_present(expected_result=expected_result)
        self.assertEqual(result, expected_result,
                         msg=f'Acca notification presence status "{result}" is not the same as expected "{expected_result}"')

    def verify_betslip_multiples(self, expected_result=True, clear_betslip=True):
        self.site.open_betslip()
        betslip_sections = wait_for_result(lambda: self.get_betslip_content().betslip_sections_list,
                                           timeout=1,
                                           name='Betslip sections to load')
        self.assertTrue(len(betslip_sections) > 0, msg='No bets found')
        result = vec.betslip.MULTIPLES in betslip_sections
        self.assertEqual(result, expected_result, msg=f'Multiples presence status "{result}" is not the same as expected "{expected_result}"')
        if clear_betslip:
            self.clear_betslip()
        else:
            self.site.close_betslip()
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is still opened')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create Football events, PROD: Find Football events
        """
        self.__class__.leagues = []  # this is for repeated preconditions situation
        if tests.settings.backend_env == 'prod':
            # football
            football_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                                  number_of_events=3)
            # event 1
            event1 = choice(football_events)
            football_events.remove(event1)
            self.__class__.created_event_name = normalize_name(event1['event']['name'])
            event_id = event1['event']['id']
            self.events[self.created_event_name] = event_id
            self.__class__.leagues.append(self.get_accordion_name_for_event_from_ss(event=event1))

            # event 2
            event2 = choice(football_events)
            football_events.remove(event2)
            self.__class__.created_event2_name = normalize_name(event2['event']['name'])
            event2_id = event2['event']['id']
            self.events[self.created_event2_name] = event2_id
            self.__class__.leagues.append(self.get_accordion_name_for_event_from_ss(event=event2))

            # event 3
            event3 = choice(football_events)
            football_events.remove(event3)
            self.__class__.created_event3_name = normalize_name(event3['event']['name'])
            event3_id = event3['event']['id']
            self.events[self.created_event3_name] = event3_id
            self.__class__.leagues.append(self.get_accordion_name_for_event_from_ss(event=event3))
        else:
            # football
            for i in range(0, 3):
                event_params = self.ob_config.add_autotest_premier_league_football_event()
                event_id = event_params.event_id
                event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id,
                                                                       query_builder=self.ss_query_builder)
                self.__class__.events[normalize_name(event_resp[0]['event']['name'])] = event_id
                self.__class__.leagues.append(self.get_accordion_name_for_event_from_ss(event=event_resp[0]))
            self.assertTrue(len(self.events.items()) == 3,
                            msg='Actual number of created events %s is not the same as expected 3'
                            % len(self.events.items()))
            self.__class__.created_event_name, self.__class__.created_event2_name, self.__class__.created_event3_name = self.events
        self.__class__.league1, self.__class__.league2, self.__class__.league3 = self.leagues
        self.__class__.event_id, self.__class__.event_id2, self.__class__.event_id3 = self.events.values()
        self.__class__.event_name, self.__class__.event_name2, self.__class__.event_name3 = self.events.keys()
        self._logger.info(
            f'*** Found/Created Football events "{list(self.events.keys())}" with ids "{list(self.events.values())}", leagues "{self.leagues}"')

    def test_001_open_football_landing_page(self):
        """
        DESCRIPTION: Click 'FOOTBALL'
        """
        self.navigate_to_page(name='sport/football')

    def test_002_make_single_selection(self):
        """
        DESCRIPTION: Add one selection to the Betslip
        EXPECTED: Multiples are NOT available in the Betslip
        EXPECTED: ACCA Odds Notification message doesn't appear
        """
        event = self.get_event_from_league(event_id=self.event_id, section_name=self.league1)
        self.__class__.prices = event.get_active_prices()
        if not self.prices:
            self.test_000_preconditions()
            event = self.get_event_from_league(event_id=self.event_id, section_name=self.league1)
            self.__class__.prices = event.get_active_prices()
        self.assertTrue(self.prices, msg=f'There is no active prices for event is "{self.event_id}"')
        name, price = list(self.prices.items())[0]
        self.assertTrue(price, msg=f'Bet button "{name}" is not found')
        price.click()

        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=15)
        self.verify_acca_notification_presence(expected_result=False)
        self.verify_betslip_multiples(expected_result=False)

    def test_003_add_two_selections_from_the_same_event_to_betslip(self):
        """
        DESCRIPTION: Add two selections from the same event to the Betslip
        EXPECTED: Multiples are NOT available in the Betslip
        EXPECTED: ACCA Odds Notification message doesn't appear
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices, msg=f'Could not find output prices for created event "{self.event_name}"')
        name, price = list(output_prices.items())[0]
        name2, price2 = list(output_prices.items())[1]
        self.assertTrue(price, msg=f'Bet button "{name}" is not found')
        self.assertTrue(price2, msg=f'Bet button "{name2}" is not found')
        price.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=10)
        price2.click()
        self.verify_acca_notification_presence(expected_result=False)
        self.verify_betslip_multiples(expected_result=False)

    def test_004_make_add_at_least_two_selections_from_different_events_to_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: Multiples are available in the Betslip
        EXPECTED: ACCA Odds Notification message appears
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices, msg=f'Could not find output prices for created event "{self.event_name}"')
        name, price = list(output_prices.items())[0]
        self.assertTrue(price, msg=f'Bet button "{name}" is not found')
        price.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=10)

        event2 = self.get_event_from_league(event_id=self.event_id2,
                                            section_name=self.league2)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2, msg=f'Could not find output prices for created event "{self.event_name2}"')
        name2, price2 = list(output_prices2.items())[1]
        self.assertTrue(price2, msg=f'Bet button "{name2}" is not found')
        price2.click()
        self.assertTrue(price2.is_selected(timeout=2), msg=f'Price "{name2}" was not selected after click')

        self.verify_acca_notification_presence()

        self.__class__.orig_acca_odds_value = self.site.acca_notification.odds_value
        self.assertTrue(self.orig_acca_odds_value, msg='Odds value is not displayed in Acca notification')

        self.verify_betslip_multiples(clear_betslip=False)

    def test_005_add_one_more_selection_from_another_event(self):
        """
        DESCRIPTION: Add one more selection from another event
        EXPECTED: Multiples are available in the Betslip
        EXPECTED: ACCA Odds Notification message is still displayed
        EXPECTED: Multiples name on ACCA Odds Notification message is updated properly
        EXPECTED: Odds is recalculated and new price is displayed
        """
        event3 = self.get_event_from_league(event_id=self.event_id3,
                                            section_name=self.league3)
        output_prices3 = event3.get_active_prices()
        self.assertTrue(output_prices3, msg=f'Could not find output prices for created event "{self.event_name3}"')
        self.__class__.name3, self.__class__.price3 = list(output_prices3.items())[0]
        self.__class__.name4, self.__class__.price4 = list(output_prices3.items())[1]
        self.assertTrue(self.price3, msg=f'Bet button "{self.name3}" is not found')
        self.assertTrue(self.price4, msg=f'Bet button "{self.name4}" is not found')
        self.price3.click()
        self.assertTrue(self.price3.is_selected(timeout=2), msg=f'Price "{self.name3}" was not selected after click')

        self.verify_acca_notification_presence()
        acca = self.site.acca_notification
        result = wait_for_result(lambda: acca.odds_value != self.orig_acca_odds_value,
                                 name='Odds to recalculate',
                                 timeout=2)
        self.__class__.mod_acca_odds_value = acca.odds_value
        self.assertTrue(result, msg='Odds value is not recalculated after adding new selection')
        self.assertEqual(acca.bet_type, vec.betslip.TBL,
                         msg=f'Bet Type "{acca.bet_type}" is not the same as expected "{vec.betslip.TBL}"')
        self.verify_betslip_multiples(clear_betslip=False)

    def test_006_add_one_more_selection_from_the_same_event(self):
        """
        DESCRIPTION: Add one more selection from the same event
        EXPECTED: Multiples are available in the Betslip
        EXPECTED: ACCA Odds Notification message is NOT displayed
        """
        self.price4.click()
        self.assertTrue(self.price4.is_selected(timeout=2), msg=f'Price "{self.name4}" was not selected after click')
        self.verify_acca_notification_presence(expected_result=False)
        self.verify_betslip_multiples(clear_betslip=False)

    def test_007_remove_selection_added_in_previous_step(self):
        """
        DESCRIPTION: Remove selection added in the previous step
        EXPECTED: Multiples are available in the Betslip
        EXPECTED: ACCA Odds Notification message appears again
        """
        self.price4.click()
        self.assertFalse(self.price4.is_selected(timeout=2, expected_result=False),
                         msg=f'Price "{self.name4}" was not deselected after click')
        self.verify_acca_notification_presence()
        self.verify_betslip_multiples(clear_betslip=False)

    def test_008_remove_one_more_selection_added_to_betslip(self):
        """
        DESCRITION: Remove one more selection added to the Betslip by clicking on Price/Odds buttons
        EXPECTED: Multiples are available in the Betslip
        EXPECTED: ACCA Odds Notification message is still displayed
        EXPECTED: Multiples name on ACCA Odds Notification message is updated properly
        EXPECTED: Odds is recalculated and new price is displayed
        """
        self.price3.click()
        self.assertFalse(self.price3.is_selected(timeout=2, expected_result=False),
                         msg=f'Price "{self.name4}" was not deselected after click')
        self.verify_acca_notification_presence()
        result = wait_for_result(lambda: self.site.acca_notification.odds_value != self.mod_acca_odds_value,
                                 name='Odds to recalculate',
                                 timeout=2)
        self.assertTrue(result, msg='Odds value is not recalculated after adding new selection')
        acca = self.site.acca_notification
        self.assertEqual(acca.bet_type, vec.betslip.DBL,
                         msg=f'Bet Type "{acca.bet_type}" is not the same as expected "{vec.betslip.DBL}"')
        self.verify_betslip_multiples()

    def test_009_remove_selections_added_to_betslip(self):
        """
        DESCRIPTION: Remove selections added to the Betslip by clicking on 'Clear Betslip' button
        EXPECTED: All selections are removed from the Betslip
        EXPECTED: ACCA Odds Notification message disappears
        """
        #  removing from betslip is covered in previous step
        self.verify_acca_notification_presence(expected_result=False)
