import re
import pytest

from tests.base_test import vtest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # We cannot result event on hl/prod
# @pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.bet_history
@pytest.mark.silks
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C1388579_HR_Silks_displaying_for_Single_Bet_on_Settled_Bets_and_Open_Bets(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C1388579
    NAME: HR Silks displaying for Single Bet on Settled Bets and Open Bets
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Settled Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed Single bet on Horse Racing races with silks
    """
    keep_browser_open = True
    silk_selection_id = []

    @classmethod
    def custom_tearDown(cls):
        """
        DESCRIPTION: Unconfirm, set result to None and make selection active again
        """
        if cls.silk_selection_id:
            ob_config = cls.get_ob_config()

            ob_config.settle_result(selection_id=cls.silk_selection_id, market_id=cls.market_id, event_id=cls.event_id,
                                    is_settle=False, wait_for_update=False)
            wait_for_result(lambda: BaseRacing().is_settled(event_id=cls.event_id,
                                                            outcome_id=cls.silk_selection_id) is None,
                            poll_interval=10, timeout=60,
                            name='Settle status to become "None"')
            ob_config.result_selection(selection_id=cls.silk_selection_id, market_id=cls.market_id,
                                       event_id=cls.event_id, result='-', wait_for_update=True)

            ob_config.change_market_state(event_id=cls.event_id, market_id=cls.market_id, displayed=True, active=True)
            ob_config.change_selection_state(selection_id=cls.silk_selection_id, displayed=True, active=True)

    def verify_correct_silk_is_displayed_for_bet(self, bet_name):
        """
        This method verifies whether silk is displayed for bet and it has correct style (visual appearance).
        :param bet_name: name (type) of the bet (e.g., 'SINGLE - [Finger Lakes 9:57 PM]')
        """
        bet_legs = self.single_hr_bet_section.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'{bet_name} bet has no bet legs')
        betleg_name, betleg = list(bet_legs.items())[0]

        self.assertIn(betleg.outcome_name, self.racing_form_selections_info.keys(),
                      msg=f'"{betleg.outcome_name}" cannot be found in "{self.racing_form_selections_info.keys()}"')
        self.assertTrue(betleg.has_silk(expected_result=True, timeout=2),
                        msg=f'Silk is not displayed for "{betleg_name}" bet')
        self.assertIn(self.expected_silk_id, betleg.silk.style,
                      msg=f'"{self.expected_silk_id}" cannot be found in "{betleg.silk.style}" for "{betleg_name}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: User is logged in
        DESCRIPTION: User has placed Single bet on Horse Racing races with silks
        """
        event_info = self.get_event_details(race_form_info=True, forecast=True, tricast=True)
        # event_name example '19:15 Chelmsford'
        event_name_time_re = re.search(r'\|?(\d{1,2}:\d{1,2})?\s*([^\|]+)', event_info.event_name)
        self.__class__.event_name, start_time = event_name_time_re.group(2).strip(), event_info.event_date_time
        start_time_local = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                      date_time_str=start_time, ss_data=True)
        self.__class__.event_name_and_time = f'{self.event_name} {start_time_local}'
        self.__class__.racing_form_selections_info = event_info.race_form_outcomes_info
        self.__class__.event_id = event_info.event_id
        ss_outcomes = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.event_id)[0]['event']['children'][0]['market']['children']
        self.__class__.market_id = ss_outcomes[0]['outcome']['marketId']

        self.ob_config.add_dividend_for_existing_event(category_id=self.ob_config.horseracing_config.category_id,
                                                       event_id=self.event_id, market_id=self.market_id)

        for selection_name, selection_info in self.racing_form_selections_info.items():
            is_active = next(outcome['outcome']['outcomeStatusCode'] for outcome in ss_outcomes if
                             outcome['outcome']['id'] == selection_info['refRecordId']) == 'A'
            if selection_info != 'generic' and is_active:
                self.__class__.silk_selection_id = selection_info['refRecordId']

                self.__class__.expected_silk_id = next(
                    horse['silk'].strip('.png') for horse in event_info.datafabric_data['horses'] if horse['horseName'] == selection_name)
                self._logger.info(f'\n*** Event name / ID: {self.event_name} / {self.event_id}\n'
                                  f'*** Selection name / ID: {selection_name} / {self.silk_selection_id}')
                break

        self.site.login(async_close_dialogs=False)
        self.open_betslip_with_selections(selection_ids=self.silk_selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_open_bets_tab_and_verify_that_silk_is_displaying(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for Single horse racing bet
        EXPECTED: Correct silk is displayed for placed bet to the left of a horse name
        """
        self.site.open_my_bets_open_bets()

        bet_name, self.__class__.single_hr_bet_section = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name_and_time, number_of_bets=1)
        self.verify_correct_silk_is_displayed_for_bet(bet_name=bet_name)

    def test_002_navigate_to_settled_bets_tab_and_verify_that_silk_is_displaying(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for Single horse racing settled bet
        EXPECTED: Correct silk is displayed for placed bet to the left of a horse name
        """
        self.result_event(selection_ids=self.silk_selection_id, market_id=self.market_id, event_id=self.event_id)

        self.site.open_my_bets_settled_bets()

        bet_name, self.__class__.single_hr_bet_section = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        self.verify_correct_silk_is_displayed_for_bet(bet_name=bet_name)
