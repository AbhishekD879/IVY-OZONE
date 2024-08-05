import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.extra_place_icon
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C2644240_Verify_Extra_Place_icon_for_Multiple_Bet_on_CashOut_tab(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2644240
    NAME: Verify Extra Place icon for Multiple Bet on CashOut tab
    DESCRIPTION: This test case verifies that the Extra Place icon for Multiple Bet is displayed on the CashOut tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Signposting toggle is Turn ON in the CMS
        DESCRIPTION: User is logged in
        DESCRIPTION: User has placed the following bets:
        DESCRIPTION: (1) Multiple bet for events with Extra Place promo available on Market level
        DESCRIPTION: (2) Multiple bet which consists of the following selections:
        DESCRIPTION:   - event with Extra Place promo available on Market level
        DESCRIPTION:   - event without Extra Place promo
        """
        events = [self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True),
                  self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True),
                  self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True),
                  self.ob_config.add_UK_racing_event(number_of_runners=1)]

        start_times = [self.convert_time_to_local(date_time_str=event.event_date_time) for event in events]

        self.__class__.event_names = [f'{self.horseracing_autotest_uk_name_pattern} {start_time}'
                                      for start_time in start_times]

        selection_ids = [[list(events[0].selection_ids.values())[0], list(events[1].selection_ids.values())[0]],
                         [list(events[2].selection_ids.values())[0], list(events[3].selection_ids.values())[0]]]

        self.__class__.selections = [list(event.selection_ids.keys())[0] for event in events]

        username = tests.settings.betplacement_user
        self.site.login(username=username)
        for ids in selection_ids:
            self.open_betslip_with_selections(selection_ids=ids)
            self.place_multiple_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.done_button.click()
            self.__class__.expected_betslip_counter_value = 0

    def test_001_navigate_to_the_cashout_tab(self):
        """
        DESCRIPTION: Navigate to the CashOut tab
        EXPECTED: * CashOut tab is opened
        EXPECTED: * Multiple bet from precondition is present on CashOut tab
        """
        self.site.open_my_bets_cashout()
        event_groups_section = self.site.cashout.tab_content.accordions_list
        bet_name_1, multiple_bet_1 = event_groups_section.get_bet(event_names=self.event_names[0:2], bet_type='DOUBLE',
                                                                  number_of_bets=4)
        self.assertTrue(multiple_bet_1, msg=f'Bet "{bet_name_1}" is not displayed')
        self.__class__.bet_legs_1 = multiple_bet_1.items_as_ordered_dict
        self.assertTrue(self.bet_legs_1, msg=f'No one bet leg was found for bet: "{bet_name_1}"')

        bet_name_2, multiple_bet_2 = event_groups_section.get_bet(event_names=self.event_names[2:4], bet_type='DOUBLE',
                                                                  number_of_bets=4)
        self.assertTrue(multiple_bet_2, msg=f'Bet "{bet_name_2}" is not displayed')
        self.__class__.bet_legs_2 = multiple_bet_2.items_as_ordered_dict
        self.assertTrue(self.bet_legs_2, msg=f'No one bet leg was found for bet: "{bet_name_2}"')

    def test_002_verify_extra_place_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Multiple bet (1) from Preconditions
        EXPECTED: * 'Extra Place' icon is displayed under each selection
        EXPECTED: * 'Extra Place' icon is aligned to the left
        """
        bet_legs_1 = [bet_leg for bet_leg in self.bet_legs_1.values()]
        self.verify_extra_place_icon_displayed(bet_leg=bet_legs_1[0])
        self.verify_extra_place_icon_displayed(bet_leg=bet_legs_1[1])

    def test_003_verify_extra_place_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Multiple bet (2) from Preconditions
        EXPECTED: * 'Extra Place' and label are displayed only under selection from event with Extra Place promo available
        EXPECTED: * There is no 'Extra Place' icon or and label under the another selection
        """
        bet_legs_2 = [bet_leg for bet_leg in self.bet_legs_2.values()]
        self.verify_extra_place_icon_displayed(bet_leg=bet_legs_2[0])
        self.verify_extra_place_icon_displayed(bet_leg=bet_legs_2[1], expected=False)
