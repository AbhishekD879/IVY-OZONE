import re
import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # We cannot result event on hl/prod
# @pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.forecast_tricast
@pytest.mark.bet_history
@pytest.mark.silks
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C2552920_HR_Silks_displaying_for_Forecast_Tricast_Bet_on_Settled_Bets_and_Open_Bets(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C2552920
    NAME: HR Silks displaying for Forecast/Tricast Bet on Settled Bets and Open Bets
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Settled Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed Forecast/Tricast  bet on Horse Racing races with silks
    """
    keep_browser_open = True
    bet_type = 'SINGLE - FORECAST'
    silk_selection_ids = []
    selection_names = []
    expected_silk_ids = []

    @classmethod
    def custom_tearDown(cls):
        """
        DESCRIPTION: Unconfirm, set result to None and make selection active again
        """
        if cls.silk_selection_ids:
            ob_config = cls.get_ob_config()
            for selection_id in cls.silk_selection_ids:
                ob_config.settle_result(selection_id=selection_id, market_id=cls.market_id, event_id=cls.event_id,
                                        is_settle=False, wait_for_update=False)
                wait_for_result(lambda: BaseRacing().is_settled(event_id=cls.event_id,
                                                                outcome_id=selection_id) is None,
                                poll_interval=10, timeout=60,
                                name='Settle status to become "None"')
                ob_config.result_selection(selection_id=selection_id, market_id=cls.market_id, event_id=cls.event_id,
                                           result='-', wait_for_update=True)

                ob_config.change_market_state(event_id=cls.event_id, market_id=cls.market_id, displayed=True, active=True)
                ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)

    def verify_correct_silk_is_displayed_for_bet(self, bet_name):
        """
        This method verifies whether silk is displayed for bet and it has correct style (visual appearance).
        :param bet_name: name (type) of the bet (e.g., 'SINGLE- COMBINATION FORECAST - [Finger Lakes 9:57 PM]')
        """
        bet_legs = self.single_hr_forecast_combination.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'{bet_name} bet has no bet legs')
        betleg_name, betlegs = list(bet_legs.items())[0]
        betleg_outcomes = betlegs.items_as_ordered_dict
        for index, (outcome_name, outcome) in enumerate(betleg_outcomes.items()):
            self.assertIn(outcome_name, self.selection_names,
                          msg=f'Selection "{outcome_name}" cannot be found in "{self.selection_names}"')
            self.assertTrue(outcome.has_silk(expected_result=True, timeout=2),
                            msg=f'Silk is not displayed for "{outcome_name}" bet')
            self.assertIn(self.expected_silk_ids[index], outcome.silk.style,
                          msg=f'"{self.expected_silk_ids[index]}" cannot be found '
                              f'in "{outcome.silk.style}" for "{outcome_name}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User has placed Forecast/Tricast bet on Horse Racing races with silks
        """
        event_info = self.get_event_details(race_form_info=True, forecast=True, tricast=True)
        self.__class__.event_id = event_info.event_id
        ss_outcomes = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.event_id)[0]['event']['children'][0]['market']['children']
        self.__class__.market_id = ss_outcomes[0]['outcome']['marketId']

        self.ob_config.add_dividend_for_existing_event(category_id=self.ob_config.horseracing_config.category_id,
                                                       event_id=self.event_id, market_id=self.market_id)

        # event_name example '23:17 Turf Paradise'
        event_name_time_re = re.search(r'\|?(\d{1,2}:\d{1,2})?\s*([^\|]+)', event_info.event_name)
        event_name, start_time = event_name_time_re.group(2).strip(), event_info.event_date_time
        start_time_local = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                      date_time_str=start_time, ss_data=True)
        self.__class__.event_name = f'{event_name} {start_time_local}'
        self.__class__.event_name_wo_time = event_name
        racing_form_selections_info = event_info.race_form_outcomes_info

        for selection_name, selection_info in racing_form_selections_info.items():
            is_active = next(outcome['outcome']['outcomeStatusCode'] for outcome in ss_outcomes if
                             outcome['outcome']['id'] == selection_info['refRecordId']) == 'A'
            if selection_info != 'generic' and is_active:
                silk_selection_id = selection_info['refRecordId']
                self.silk_selection_ids.append(silk_selection_id)
                self.selection_names.append(selection_name)
                silk_id = next(horse['silk'].strip('.png') for horse in event_info.datafabric_data['horses'] if horse['horseName'] == selection_name)
                self.expected_silk_ids.append(silk_id)
                self._logger.info(f'\n*** Event name / ID: {self.event_name} / {self.event_id}\n'
                                  f'*** Selection name / ID: {selection_name} / {silk_selection_id}')
            if len(self.silk_selection_ids) >= 2:
                break

        self.site.login(async_close_dialogs=False)
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', forecast=True,
                                                                expected_selections=self.selection_names)
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_open_bets_tab_and_verify_that_correct_silk_is_displaying(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that correct Silk is displaying for placed Forecast/Tricast horse racing bet
        EXPECTED: * Correct silks are displayed for placed bet
        EXPECTED: * Silks are displayed on the left of each horse name
        EXPECTED: * Silks with selection names are displayed one by one in column view
        """
        self.site.open_my_bets_open_bets()
        bet_name, self.__class__.single_hr_forecast_combination = \
            self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=self.bet_type,
                                                                    event_names=self.event_name,
                                                                    number_of_bets=1)
        self.verify_correct_silk_is_displayed_for_bet(bet_name=bet_name)

    def test_002_navigate_to_settled_bets_tab_and_verify_that_correct_silk_is_displaying(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that correct Silk is displaying for placed Forecast/Tricast horse racing bet
        EXPECTED: * Correct silks are displayed for settled bet
        EXPECTED: * Silks are displayed on the left of each horse name
        EXPECTED: * Silks with selection names are displayed one by one in column view
        """
        for selection_id in self.silk_selection_ids:
            self.result_event(selection_ids=selection_id, market_id=self.market_id, event_id=self.event_id)

        self.site.open_my_bets_settled_bets()
        bet_name, self.__class__.single_hr_forecast_combination = \
            self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=self.bet_type,
                                                                      event_names=self.event_name_wo_time,
                                                                      number_of_bets=1)
        self.verify_correct_silk_is_displayed_for_bet(bet_name=bet_name)
