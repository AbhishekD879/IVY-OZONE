import re
import pytest

from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.failure_exception import TestFailure
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


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
class Test_C2552919_HR_Silks_displaying_for_Multiple_Bet_on_Bet_History_and_Open_Bets(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C2552919
    NAME: HR Silks displaying for Multiple Bet on Settled Bets and Open Bets
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Settled Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed Multiple bet on Horse Racing races with silks
    """
    keep_browser_open = True
    silk_selection_ids = []
    expected_silk_ids = []
    selection_names = []

    @classmethod
    def custom_tearDown(cls):
        """
        DESCRIPTION: Unconfirm, set result to None and make selection active again
        """
        if cls.silk_selection_ids:
            ob_config = cls.get_ob_config()
            for index, selection_id in enumerate(cls.silk_selection_ids):
                ob_config.settle_result(selection_id=selection_id, market_id=cls.market_ids[index],
                                        event_id=cls.event_ids[index], is_settle=False, wait_for_update=False)
                wait_for_result(lambda: BaseRacing().is_settled(event_id=cls.event_ids[index],
                                                                outcome_id=selection_id) is None,
                                poll_interval=10, timeout=60,
                                name='Settle status to become "None"')
                ob_config.result_selection(selection_id=selection_id, market_id=cls.market_ids[index],
                                           event_id=cls.event_ids[index], result='-', wait_for_update=True)
                ob_config.change_market_state(event_id=cls.event_ids[index], market_id=cls.market_ids[index],
                                              displayed=True, active=True)
                ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)

    def verify_correct_silk_is_displayed_for_bet(self, bet_name):
        """
        This method verifies whether silk is displayed for bet and it has correct style (visual appearance).
        :param bet_name: name (type) of the bet (e.g., 'DOUBLE - [Finger Lakes 9:57 PM, Autotest - UK 1:50 PM]')
        """
        is_silk_displayed = False
        bet_legs = self.multiple_hr_bet_section.items_as_ordered_dict
        for index, (betleg_name, betleg) in enumerate(bet_legs.items()):
            if self.event_names_wo_time[index] in betleg_name:
                betleg.scroll_to()
                self.assertIn(betleg.outcome_name, self.selection_names,
                              msg=f'"{betleg.outcome_name}" cannot be found in "{self.selection_names}"')
                self.assertTrue(betleg.has_silk(expected_result=True, timeout=2),
                                msg=f'Silk is not displayed for "{betleg_name}" bet')
                self.assertIn(self.expected_silk_ids[index], betleg.silk.style,
                              msg=f'"{self.expected_silk_ids[index]}" cannot be '
                                  f'found in "{betleg.silk.style}" for "{betleg_name}"')
                is_silk_displayed = True
            else:
                raise TestFailure(f'No betleg "{self.event_names[index]}" found')

        self.assertTrue(is_silk_displayed, msg=f'Could not find silks inside of "{bet_name}" bet')

    def test_000_preconditions(self):
        """
        DESCRIPTION: User is logged in
        DESCRIPTION: User has placed Multiple bet on Horse Racing races with silks
        """
        # Get HR event with silks
        event_info = self.get_event_details(race_form_info=True)

        event_name_time_re = re.search(r'\|?(\d{1,2}:\d{1,2})?\s*([^\|]+)', event_info.event_name)
        event_name, start_time = event_name_time_re.group(2).strip(), event_info.event_date_time
        start_time_local = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                      date_time_str=start_time, ss_data=True)

        self.__class__.event_id = event_info.event_id
        self.__class__.event_name = f'{event_name} {start_time_local}'
        self.__class__.silk_settled_event_name = event_name
        self.__class__.racing_form_selections_info_1 = event_info.race_form_outcomes_info
        ss_outcomes = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.event_id)[0]['event']['children'][0]['market']['children']
        self.__class__.silk_market_id = ss_outcomes[0]['outcome']['marketId']

        self.ob_config.add_dividend_for_existing_event(category_id=self.ob_config.horseracing_config.category_id,
                                                       event_id=self.event_id, market_id=self.silk_market_id)

        for selection_name, selection_info in self.racing_form_selections_info_1.items():
            is_active = next(outcome['outcome']['outcomeStatusCode'] for outcome in ss_outcomes if
                             outcome['outcome']['id'] == selection_info['refRecordId']) == 'A'
            if selection_info != 'generic' and is_active:
                silk_selection_id = selection_info['refRecordId']
                expected_silk_id = next(
                    horse['silk'].strip('.png') for horse in event_info.datafabric_data['horses'] if horse['horseName'] == selection_name)
                self.selection_names.append(selection_name)
                self.silk_selection_ids.append(silk_selection_id)
                self.expected_silk_ids.append(expected_silk_id)
                self._logger.info(f'\n*** First Event name / ID: {self.event_name} / {self.event_id}\n'
                                  f'*** First Selection name / ID: {selection_name} / {silk_selection_id}')
                break

        # Get second HR event with silks
        event_info_2 = self.get_event_details(race_form_info=True)
        self.__class__.event_id_2 = event_info_2.event_id
        if self.event_id_2 == self.event_id:
            raise SiteServeException('There is only one silk event')

        event_name_time_re_2 = re.search('\|?(\d{1,2}:\d{1,2})?\s*([^\|]+)', event_info_2.event_name)
        event_name_2, start_time_2 = event_name_time_re_2.group(2).strip(), event_info_2.event_date_time
        start_time_local_2 = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                        date_time_str=start_time_2, ss_data=True)
        self.__class__.event_name_2 = f'{event_name_2} {start_time_local_2}'

        ss_outcomes_2 = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.event_id_2)[0]['event']['children'][0]['market']['children']
        self.__class__.silk_market_id_2 = ss_outcomes_2[0]['outcome']['marketId']

        self.ob_config.add_dividend_for_existing_event(category_id=self.ob_config.horseracing_config.category_id,
                                                       event_id=self.event_id_2, market_id=self.silk_market_id_2)

        racing_form_selections_info_2 = event_info_2.race_form_outcomes_info

        for selection_name, selection_info in racing_form_selections_info_2.items():
            is_active = next(outcome['outcome']['outcomeStatusCode'] for outcome in ss_outcomes_2 if
                             outcome['outcome']['id'] == selection_info['refRecordId']) == 'A'
            if selection_info != 'generic' and is_active:
                silk_selection_id = selection_info['refRecordId']
                expected_silk_id = next(
                    horse['silk'].strip('.png') for horse in event_info_2.datafabric_data['horses'] if horse['horseName'] == selection_name)
                self.selection_names.append(selection_name)
                self.silk_selection_ids.append(silk_selection_id)
                self.expected_silk_ids.append(expected_silk_id)
                self._logger.info(f'\n*** Second Event name / ID: {event_name_2} / {self.event_id_2}\n'
                                  f'*** Second Selection name / ID: {selection_name} / {silk_selection_id}')
                break

        self.__class__.event_names = f'{self.event_name}, {self.event_name_2}'
        self.__class__.event_names_wo_time = [event_name, event_name_2]
        self.__class__.market_ids = [self.silk_market_id, self.silk_market_id_2]
        self.__class__.event_ids = [self.event_id, self.event_id_2]

        self.site.login(async_close_dialogs=False)
        self.open_betslip_with_selections(selection_ids=self.silk_selection_ids)
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('Homepage')

    def test_001_navigate_to_open_bets_tab_and_verify_that_silk_is_displaying(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for placed Multiple horse racing bet
        EXPECTED: Correct silks are displayed for placed bet
        EXPECTED: Silks are displayed on the left of each horse name
        """
        self.site.open_my_bets_open_bets()

        bet_name, self.__class__.multiple_hr_bet_section = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_names)
        self.verify_correct_silk_is_displayed_for_bet(bet_name=bet_name)

    def test_002_navigate_to_settled_bets_tab_and_verify_that_silk_is_displaying(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for settled Multiple horse racing bet
        EXPECTED: Correct silks are displayed for settled bet
        EXPECTED: Silks are displayed on the left of each horse name
        """
        self.result_event(selection_ids=self.silk_selection_ids[0], market_id=self.silk_market_id,
                          event_id=self.event_id)
        self.result_event(selection_ids=self.silk_selection_ids[1], market_id=self.silk_market_id_2,
                          event_id=self.event_id_2)

        self.site.open_my_bets_settled_bets()

        self.__class__.silk_event_name = self.silk_settled_event_name
        bet_name, self.__class__.multiple_hr_bet_section = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=', '.join(self.event_names_wo_time))
        self.verify_correct_silk_is_displayed_for_bet(bet_name=bet_name)
