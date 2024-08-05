from random import choice

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter
from deepdiff import DeepDiff

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.virtual_sports
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
class Test_C869684_Bet_Placement_on_Virtual_Racing(BaseBetSlipTest):
    """
    TR_ID: C869684
    NAME: Bet Placement on Virtual Racing
    DESCRIPTION: This test case verifies bet placement on  Virtual Racing
    PRECONDITIONS: Login with user account that has positive balance
    """
    keep_browser_open = True
    number_of_events = 1
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find Virtual Sports events
        DESCRIPTION: Login as user that has enough money to place few bets
        """
        additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CF,TC')), \
            exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)), \
            simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_horseracing.class_id,
                                                 additional_filters=additional_filter, raise_exceptions=False)
        if events is None:
            events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.pt_virtual_horseracing.class_id,
                                                     additional_filters=additional_filter)

        event = choice(events)
        selections = next(((market['market'].get('children')) for market in event['event']['children'] if
                           event['event'].get('children')), None)
        if not selections:
            raise SiteServeException('There are no available selections')

        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}
        self.__class__.selection_ids_all_events_hr = [selection_id for selection_id in list(selection_ids.values())[:2]]
        self._logger.info(f'*** Found Virtual HR outcomes "{self.selection_ids_all_events_hr}"')

        self.site.login()

    def test_001_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: - Selections with bet details is displayed in the Betslip
        EXPECTED: - Selections are present in Section 'Singles (2)'
        EXPECTED: - 'Forecast/Tricast' section contains multiples calculated based on added selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_hr)
        self.get_betslip_sections()

    def test_002_set_stake_for_singles2_and_forecast_tricast_and_click_bet_now_button(self):
        """
        DESCRIPTION: Set 'Stake' for 'Singles(2)' and 'Forecast/Tricast' and click 'Bet Now' button
        EXPECTED: - Bet is placed
        EXPECTED: - Bet receipt appears in Betslip
        EXPECTED: - 'Reuse selections' and 'Done' buttons are present in footer
        """
        self.__class__.bet_info_1st_try = self.place_bet_on_all_available_stakes()
        self._logger.info(f'*** Bet info on the 1st try"{self.bet_info_1st_try}"')
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(), msg='Done button is not found in Bet Receipt')
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Reuse selection button is not found in Bet Receipt')

    def test_003_click_reuse_selections_button(self):
        """
        DESCRIPTION: Click 'Reuse selections' button
        EXPECTED: - Betslip contains all the same selections
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()

        bet_info_2nd_try = self.place_bet_on_all_available_stakes()
        self._logger.info(f'*** Bet info on the 2nd try "{bet_info_2nd_try}"')
        result = DeepDiff(bet_info_2nd_try, self.bet_info_1st_try, ignore_order=True)
        self.assertFalse(bool(result), msg=f'Diff is not empty {result}')

    def test_004_click_done_button(self):
        """
        DESCRIPTION: Click 'Done' button
        EXPECTED: - Betslip is empty with no selections
        """
        self.site.bet_receipt.close_button.click()
        if self.device_type == 'mobile':
            result = self.site.has_betslip_opened(expected_result=False, timeout=5)
            self.assertFalse(result, msg='Betslip/Bet Receipt overlay is not closed after closing Bet Receipt')

        self.__class__.bet_info_1st_try = None
        self.__class__.expected_betslip_counter_value = 0

    def test_005_repeat_this_test_case_for_virtual_motorsports(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: Virtual Motorsports (Class ID 288)
        """
        additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CF,TC')), \
            exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)), \
            simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_motorsport.class_id,
                                                 additional_filters=additional_filter,
                                                 raise_exceptions=False)
        if events:
            event = choice(events)
            selections = next(((market['market'].get('children')) for market in event['event']['children'] if
                               event['event'].get('children')), None)
            if not selections:
                raise SiteServeException('There are no available selections')
            markets = event['event'].get('children')
            if not markets:
                self._logger.info('*** Skipping step since no active Virtual Motorsports events')
                return
            selections = markets[0]['market'].get('children')
            if not selections:
                self._logger.info('*** Skipping step since no active Virtual Motorsports events')
                return

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}
            self.__class__.selection_ids_all_events_motorsports = [selection_id for selection_id in
                                                                   list(selection_ids.values())[:2]]
            self._logger.info(f'*** Found Virtual Motorsports outcomes "{self.selection_ids_all_events_motorsports}"')

            self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_motorsports)
            self.get_betslip_sections()
            self.test_002_set_stake_for_singles2_and_forecast_tricast_and_click_bet_now_button()
            self.test_004_click_done_button()
        else:
            self._logger.warning('*** Skipping step since no active Virtual Motorsports events')

    def test_006_repeat_this_test_case_for_virtual_cycling(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: Virtual Cycling (Class ID 290)
        """
        additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CF,TC')), \
            exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)), \
            simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_cycling.class_id,
                                                 additional_filters=additional_filter, raise_exceptions=False)
        if events:
            event = choice(events)
            markets = event['event'].get('children')
            if not markets:
                self._logger.info('*** Skipping step since no active Virtual Cycling events')
                return
            selections = markets[0]['market'].get('children')
            if not selections:
                self._logger.info('*** Skipping step since no active Virtual Cycling events')
                return

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}
            self.__class__.selection_ids_all_events_cycling = [selection_id for selection_id in
                                                               list(selection_ids.values())[:2]]
            self._logger.info(f'*** Found Virtual Cycling outcomes "{self.selection_ids_all_events_cycling}"')

            self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_cycling)
            self.get_betslip_sections()
            self.test_002_set_stake_for_singles2_and_forecast_tricast_and_click_bet_now_button()
            self.test_004_click_done_button()
        else:
            self._logger.warning('*** Skipping step since no active Virtual Cycling events')

    def test_007_repeat_this_test_case_for_virtual_greyhound_racing(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: Virtual Greyhound Racing (Class ID 286)
        """
        # Virtual Greyhound Racing (Class ID 286)
        additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CF,TC')), \
            exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)), \
            simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_greyhounds.class_id,
                                                 additional_filters=additional_filter, raise_exceptions=False)
        if events is None:
            events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.pt_virtual_greyhounds.class_id,
                                                     additional_filters=additional_filter)
        if events:
            event = choice(events)
            markets = event['event'].get('children')
            if not markets:
                self._logger.info('*** Skipping step since no active Virtual Greyhound Racing events')
                return
            selections = markets[0]['market'].get('children')
            if not selections:
                self._logger.info('*** Skipping step since no active Virtual Greyhound Racing events')
                return

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}
            self.__class__.selection_ids_all_events_greyhounds = [selection_id for selection_id in
                                                                  list(selection_ids.values())[:2]]
            self._logger.info(f'*** Found Virtual Greyhounds outcomes "{self.selection_ids_all_events_greyhounds}"')

            self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_greyhounds)
            self.get_betslip_sections()
            self.test_002_set_stake_for_singles2_and_forecast_tricast_and_click_bet_now_button()
            self.test_004_click_done_button()
        else:
            self._logger.warning('*** Skipping step since no active Virtual Greyhound Racing events')

    def test_008_repeat_this_test_case_for_virtual_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: Virtual Grand National (Class ID 26604)
        """
        additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CF,TC')), \
            exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)), \
            simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_grand_national.class_id,
                                                 additional_filters=additional_filter, raise_exceptions=False)
        if events:
            event = choice(events)
            markets = event['event'].get('children')
            if not markets:
                self._logger.info('*** Skipping step since no active Virtual Grand National events')
                return
            selections = markets[0]['market'].get('children')
            if not selections:
                self._logger.info('*** Skipping step since no active Virtual Grand National events')
                return

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}
            self.__class__.selection_ids_all_events_grand_national = [selection_id for selection_id in
                                                                      list(selection_ids.values())[:2]]
            self._logger.info(f'*** Found Virtual Greyhounds outcomes "{self.selection_ids_all_events_grand_nationa}"')

            self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_grand_national)
            self.get_betslip_sections()
            self.test_002_set_stake_for_singles2_and_forecast_tricast_and_click_bet_now_button()
            self.test_004_click_done_button()
        else:
            self._logger.warning('*** Skipping step since no active Virtual Grand National events')
