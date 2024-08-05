import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.extra_place_icon
@pytest.mark.open_bets
@pytest.mark.bet_history
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C2644242_Verify_Extra_Place_Icon_for_Multiple_Bet_on_OpenBetsBetHistory_tabs(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2644242
    NAME: Verify Extra Place icon for Multiple Bet on OpenBets/Settled Bets tabs
    DESCRIPTION: This test case verifies that the Extra Place icon for Multiple Bet is displayed on the OpenBets/Settled Bets tabs
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed the following bets:
    PRECONDITIONS: OPEN BETS:
    PRECONDITIONS: (1) Multiple bet for events with Extra Place promo available on **Market level**
    PRECONDITIONS: (2) Multiple bet which consists of the following selections:
    PRECONDITIONS: - event with Extra Place promo available on any level
    PRECONDITIONS: - event without Extra Place promo
    PRECONDITIONS: ALREADY SETTLED BET:
    PRECONDITIONS: (1) Multiple bet for events with Extra Place promo available on **Market level**
    PRECONDITIONS: (2) Multiple bet which consists of the following selections:
    PRECONDITIONS: - event with Extra Place promo available on any level
    PRECONDITIONS: - event without Extra Place promo
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Signposting toggle is Turn ON in the CMS
        DESCRIPTION: User is logged in
        DESCRIPTION: User has placed the following bets:
        DESCRIPTION: (1) Multiple bet for events with Extra Place promo available on Market level
        DESCRIPTION: (2) Multiple bet which consists of the following selections:
        DESCRIPTION:    - event with Extra Place promo available on any level
        DESCRIPTION:    - event without Extra Place promo
        """
        events = [self.ob_config.add_UK_racing_event(market_extra_place_race=True),
                  self.ob_config.add_UK_racing_event(market_extra_place_race=True),
                  self.ob_config.add_UK_racing_event(market_extra_place_race=True),
                  self.ob_config.add_UK_racing_event()]

        selection_ids = [[list(events[0].selection_ids.values())[0], list(events[1].selection_ids.values())[0]],
                         [list(events[2].selection_ids.values())[0], list(events[3].selection_ids.values())[0]]]

        self.__class__.selections = []
        for index in range(len(events)):
            self.__class__.selections.append(list(events[index].selection_ids.keys())[0])

        self.__class__.event_params = []
        for index in range(len(events)):
            self.event_params.append((list(events[index].selection_ids.values())[0],
                                      events[index].market_id, events[index].event_id))

        self.site.login()
        for ids in selection_ids:
            self.open_betslip_with_selections(selection_ids=ids)
            self.place_multiple_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.done_button.click()
            self.__class__.expected_betslip_counter_value = 0

    def test_001_navigate_to_the_open_bets_tab_verify_extra_place_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the Open Bets tab
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (1)** from Preconditions
        EXPECTED: * 'Extra Place' icon and label are displayed below each selection
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        self.site.open_my_bets_open_bets()
        self.__class__.bet_legs = self.verify_selections_displayed(tab=self.site.open_bets,
                                                                   selections=self.selections)
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[0]])
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[1]])

    def test_002_verify_extra_place_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (2)** from Preconditions
        EXPECTED: * 'Extra Place' and label are displayed only below selection from event with Extra Place promo available
        EXPECTED: * There is no 'Extra Place' icon or and label under the another selection
        """
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[2]])
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[3]], expected=False)

    def test_003_navigate_to_settled_bets_tabverify_extra_place_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Settled Bets tab
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (1)** from Preconditions
        EXPECTED: * 'Extra Place' icon and label are displayed below each selection
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        for selection in self.event_params:
            self.result_event(selection_ids=selection[0], market_id=selection[1],
                              event_id=selection[2])
        self.site.open_my_bets_settled_bets()
        self.__class__.bet_legs = self.verify_selections_displayed(tab=self.site.bet_history,
                                                                   selections=self.selections)
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[0]])
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[1]])

    def test_004_verify_extra_place_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (2)** from Preconditions
        EXPECTED: * 'Extra Place' and label are displayed only under selection from event with Extra Place promo available
        EXPECTED: * There is no 'Extra Place' icon or and label under the another selection
        """
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[2]])
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[3]], expected=False)
