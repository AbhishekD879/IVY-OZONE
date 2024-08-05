from random import choice

import pytest
from collections import OrderedDict
from deepdiff import DeepDiff

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.virtual_sports
@pytest.mark.bet_placement
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C869664_Bet_Placement_on_Virtual_Sports(BaseBetSlipTest):
    """
    TR_ID: C869664
    NAME: Bet Placement on Virtual Sports
    DESCRIPTION: This test case verifies bet placement on Virtual Football
    PRECONDITIONS: Login with user account that has positive balance
    """
    keep_browser_open = True
    max_number_of_events = 2
    maxDiff = None
    bet_info_1st_try = None

    def place_bet_on_all_available_stakes(self, freebet=False, each_way=False):
        """
        Placing bet on all available stakes (singles, multiples, acca)
        """
        self.__class__.bet_amount = 1
        bet_info = OrderedDict()
        all_sections = self.get_betslip_sections(all_available=True)
        for section_name, section in all_sections.items():
            stake_info = OrderedDict()
            section.wait_until_refreshed(timeout=.5)
            for stake in self.zip_available_stakes(section=section).items():
                stake_name = stake[0]
                self.enter_stake_amount(stake=stake, each_way=each_way) \
                    if stake_name not in ['Trixie', 'Round Robin', 'Flag', 'Single Stakes About (2)',
                                          'Double Stakes About (2)'] else None
                one_stake_info = self.collect_stake_info(stake=stake,
                                                         multiples=stake_name not in ['Double', 'Trixie', 'Round Robin',
                                                                                      'Flag', 'Single Stakes About',
                                                                                      'Double Stakes About'])

                stake_info.update({stake_name: one_stake_info})
            bet_info.update({section_name: stake_info})
        betnow_section = self.get_betslip_content()
        wait_for_result(lambda: betnow_section.bet_now_button.is_enabled(timeout=0.5))
        betnow_section.bet_now_button.click()
        return bet_info

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find Virtual Sports events
        DESCRIPTION: Login as user that has enough money to place few bets
        """
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_football.class_id,
                                                 raise_exceptions=False)
        if events is None:
            self.__class__.bet_amount = 0.10
            events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.pt_virtual_football.class_id)
        event = choice(events)
        selections = next(((market['market']['children']) for market in event['event']['children'] if
                           market['market'].get('children')), None)
        if not selections:
            raise SiteServeException('There are no available selections')

        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}

        selections2 = next(((market['market']['children']) for market in events[1]['event']['children'] if
                            market['market'].get('children')), None)
        if not selections2:
            raise SiteServeException(f'Can not find any selection')

        selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in selections2}
        self.__class__.selection_ids_all_events_football = [list(selection_ids.values())[0],
                                                            list(selection_ids2.values())[1]]
        self._logger.info(f'*** Found Virtual Football outcomes "{self.selection_ids_all_events_football}"')

        self.site.login()

    def test_001_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: - Selections with bet details is displayed in the Betlsip
        EXPECTED: - Selections are present in Section 'Singles (2)'
        EXPECTED: - 'Multiples(1)' section contains multiples calculated based on added selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_football)

    def test_002_set_stake_for_singles2_and_multiples1_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Set 'Stake' for 'Singles(2)' and 'Multiples(1)' and tap 'Bet Now' button
        EXPECTED: - Bet is placed
        EXPECTED: - Bet receipt appears in Betslip
        EXPECTED: - 'Reuse selections' and 'Done' buttons are present in footer
        """
        self.__class__.bet_info_1st_try = self.place_bet_on_all_available_stakes()
        self._logger.info(f'*** Bet info on the 1st try "{self.bet_info_1st_try}"')
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(), msg='Done button is not found in Bet Receipt')
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Reuse selection button is not found in Bet Receipt')

    def test_003_tap_reuse_selections_button(self):
        """
        DESCRIPTION: Tap 'Reuse selections' button
        DESCRIPTION: Place bet
        EXPECTED: Betslip contains all the same selections
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()
        bet_info_2nd_try = self.place_bet_on_all_available_stakes()
        self._logger.info(f'*** Bet info on the 2nd try "{bet_info_2nd_try}"')
        result = DeepDiff(bet_info_2nd_try, self.bet_info_1st_try, ignore_order=True)
        self.assertFalse(bool(result), msg=f'Diff is not empty {result}')

    def test_004_click_done_button(self):
        """
        DESCRIPTION: Click 'Done' button
        EXPECTED: Betslip is empty with no selections
        """
        self.site.bet_receipt.close_button.click()
        if self.device_type == 'mobile':
            result = self.site.has_betslip_opened(expected_result=False, timeout=5)
            self.assertFalse(result, msg='Betslip/Bet Receipt overlay is not closed after closing Bet Receipt')

            # workaround for betslip sometimes not opening on virtuals
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
        # can't open bet slip without selections
        #     counter = self.site.header.bet_slip_counter
        #     self.assertTrue(counter.is_displayed(), msg='Betslip counter is not displayed')
        #     self.assertTrue(counter.is_enabled(), msg='Betslip counter is not enabled')
        #
        #     counter.click()
        #     self.assertTrue(self.site.has_betslip_opened(), msg='Betslip has not opened')
        #
        # message = self.get_betslip_content().no_selections_title
        # self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE,
        #                  msg=f'Betslip "No selections" message "{message}" '
        #                      f'is not the same as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

        self.__class__.bet_info_1st_try = None
        self.__class__.expected_betslip_counter_value = 0

    def test_005_repeat_this_test_case_for_the_following_virtual_sports_tennis(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Tennis
        """
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_tennis.class_id,
                                                 raise_exceptions=False)
        if events:
            event = choice(events)
            markets = event['event'].get('children')
            if not markets:
                self._logger.info('*** Skipping step since no active Virtual Tennis events')
                return
            selections = markets[0]['market'].get('children')
            if not selections:
                self._logger.info('*** Skipping step since no active Virtual Tennis events')
                return

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}
            events.remove(event)
            event2 = choice(events)
            selections2 = event2['event']['children'][0]['market']['children']

            selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in selections2}

            self.__class__.selection_ids_all_events_tennis = [list(selection_ids.values())[0],
                                                              list(selection_ids2.values())[1]]

            self._logger.info(f'*** Found Virtual Tennis outcomes "{self.selection_ids_all_events_tennis}"')
            self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_tennis)
            self.test_002_set_stake_for_singles2_and_multiples1_and_tap_bet_now_button()
            # not repeating 3rd step as reusing selections works the same way, no matter which sport selected
            self.test_004_click_done_button()
        else:
            self._logger.warning('*** Skipping step since no active Virtual Tennis events')

    def test_006_repeat_this_test_case_for_the_following_virtual_sports_speedway(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Speedway
        """
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_speedway.class_id,
                                                 raise_exceptions=False)
        if events:
            event = choice(events)
            markets = event['event'].get('children')
            if not markets:
                self._logger.info('*** Skipping step since no active Virtual Speedway events')
                return
            selections = markets[0]['market'].get('children')
            if not selections:
                self._logger.info('*** Skipping step since no active Virtual Speedway events')
                return

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}
            events.remove(event)
            event2 = choice(events)
            selections2 = event2['event']['children'][0]['market']['children']

            selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in selections2}

            self.__class__.selection_ids_all_events_speedway = [list(selection_ids.values())[0],
                                                                list(selection_ids2.values())[1]]

            self._logger.info(f'*** Found Virtual Speedway outcomes "{self.selection_ids_all_events_speedway}"')
            self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_speedway)
            self.test_002_set_stake_for_singles2_and_multiples1_and_tap_bet_now_button()
            # not repeating 3rd step as reusing selections works the same way, no matter which sport selected
            self.test_004_click_done_button()
        else:
            self._logger.warning('*** Skipping step since no active Virtual Speedway events')
