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
@pytest.mark.open_bets
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C2644238_Verify_Extra_Place_Icon_for_Single_Bet_on_CashOut_Tab(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2644238
    NAME: Verify Extra Place icon for Single Bet on CashOut tab
    DESCRIPTION: This test case verifies that the Extra Place icon for Single Bet is displayed on the CashOut tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
        PRECONDITIONS: * User is logged in and has positive balance
        PRECONDITIONS: * Extra Place promo is available for <Race> event on Market lvl.
        PRECONDITIONS: * User has placed a Single bet on event with Extra Place promo and CashOut available
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True)

        selection_id = list(event.selection_ids.values())[0]
        self.__class__.selection = list(event.selection_ids.keys())[0]

        username = tests.settings.betplacement_user
        self.site.login(username=username, async_close_dialogs=False)
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_001_navigate_to_the_cash_out_tab(self):
        """
        DESCRIPTION: Navigate to the CashOut tab
        EXPECTED: * CashOut tab is opened
        EXPECTED: * Single bet from precondition is present on CashOut tab
        """
        self.site.open_my_bets_cashout()
        event_groups_section = self.site.cashout.tab_content.accordions_list
        bet_name, bet = event_groups_section.get_bet(bet_type='SINGLE', number_of_bets=1)
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        bet_leg_name, self.__class__.bet_leg = list(bet_legs.items())[0]
        bet_leg_name = bet_leg_name.split(' - ')[0]
        self.assertEqual(bet_leg_name, self.selection,
                         msg=f'Single bet "{self.selection}" is not present in CashOut tab')

    def test_002_verify_extra_place_icon_on_the_single_bet_for_event_with_extra_place_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Single bet for event with Extra Place promo available on Market level
        EXPECTED: * 'Extra Place' icon and label are displayed between event name and stake info
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_leg)
