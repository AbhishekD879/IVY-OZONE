import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot result event on PROD/HL
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.login
@pytest.mark.my_bets
@pytest.mark.mobile_only
@pytest.mark.bet_history_open_bets
@vtest
class Test_C16408294_Verify_My_Bets_counter_after_Open_Bet_becomes_Settled_Bet(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C16408294
    VOL_ID: C58695430
    NAME: Verify My Bets counter after Open Bet becomes Settled Bet
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after Open Bet becomes Settled Bet
    PRECONDITIONS: - Make sure My bets counter config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - OB TI tool:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Oxygen/Roxanne Application and login
        """
        self.check_my_bets_counter_enabled_in_cms()

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.marketID = event_params.market_id
        self.__class__.eventID = event_params.event_id

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.username)

    def test_001_place_a_bet_for_sports_racing_event(self):
        """
        DESCRIPTION: Place a bet for sports/racing event
        EXPECTED: * Bet is placed
        EXPECTED: * Bet counter on 'My Bets' Footer menu is increased by one
        """
        self.__class__.initial_counter = int(self.get_my_bets_counter_value_from_footer())

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, self.initial_counter + 1,
                         msg=f'My bets counter "{counter_value}" is not the same '
                             f'as expected "{self.initial_counter + 1}"')

    def test_002_in_ob_ti_settle_event(self):
        """
        DESCRIPTION: In OB TI settle event
        EXPECTED: Event is settled
        """
        self.result_event(event_id=self.eventID, market_id=self.marketID, selection_ids=self.selection_id)

    def test_003_check_my_bets_counter_on_footer(self):
        """
        DESCRIPTION: Check My bets counter on Footer
        EXPECTED: My bets counter on Footer Menu remains the same
        """
        counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, self.initial_counter + 1,
                         msg=f'My bets counter "{counter_value}" is not the same '
                             f'as expected "{self.initial_counter + 1}"')

    def test_004_refresh_the_page_and_check_my_bets_counter_on_footer(self):
        """
        DESCRIPTION: Refresh the page and check My bets counter on Footer
        EXPECTED: My bets counter is decreased by one on 'My Bets' Footer menu
        EXPECTED: NOTE: If there are 0 open bets, My Bets counter is NOT displayed, only My bets Footer Menu without counter
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='Homepage', timeout=15)

        counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, self.initial_counter,
                         msg=f'My bets counter "{counter_value}" is not the same '
                             f'as expected "{self.initial_counter}"')

    def test_005_repeat_steps_2_4_navigate_to_my_bets_page_on_mobile_and_cash_out_my_bets_tab_on_tablet(self):
        """
        DESCRIPTION: * Repeat steps #2-4
        DESCRIPTION: * Navigate to My Bets page on Mobile and Cash out/My Bets tab on Tablet
        EXPECTED: My bets counter is decreased by one
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.marketID = event_params.market_id
        self.__class__.eventID = event_params.event_id

        self.site.open_my_bets_open_bets()
        self.test_001_place_a_bet_for_sports_racing_event()
        self.test_002_in_ob_ti_settle_event()
        self.test_003_check_my_bets_counter_on_footer()
        self.test_004_refresh_the_page_and_check_my_bets_counter_on_footer()
