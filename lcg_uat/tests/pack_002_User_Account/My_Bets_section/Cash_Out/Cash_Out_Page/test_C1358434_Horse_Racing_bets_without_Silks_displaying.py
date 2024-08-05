import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.silks
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.cash_out
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C1358434_Horse_Racing_bets_without_Silks_displaying(BaseCashOutTest, BaseRacing):
    """
    TR_ID: C1358434
    NAME: Horse Racing bets without Silks displaying
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Racing event and place bet
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1)
        start_time, selection_ids = event_params.event_date_time, event_params.selection_ids
        start_time_local = self.convert_time_to_local(date_time_str=start_time)
        self.__class__.event_name = f'{event_params.event_off_time} {self.horseracing_autotest_uk_name_pattern} ' \
            f'{start_time_local}'

        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state('HomePage')

    def test_001_navigate_to_cashout_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Cashout' tab on 'My Bets' page
        EXPECTED: 'Cash out' tab has opened
        """
        self.site.open_my_bets_cashout()

    def test_002_verify_single_horse_racing_bet_available(self):
        """
        DESCRIPTION: Verify Single horse racing bet available
        EXPECTED: No silks are displayed for placed bets
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=self.event_name,
                                                                              bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                              number_of_bets=1)
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for "{bet_name}"')
        betleg_name, betleg = list(betlegs.items())[0]
        self.assertFalse(betleg.has_silk(expected_result=False),
                         msg=f'Silk is shown for event "{bet_name}" without silks available')
