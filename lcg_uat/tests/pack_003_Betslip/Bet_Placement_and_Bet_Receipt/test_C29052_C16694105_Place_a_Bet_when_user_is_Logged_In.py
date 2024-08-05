import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_promo_2
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29052_C16694105_Place_a_Bet_when_user_is_Logged_In(BaseBetSlipTest):
    """
    TR_ID: C29052
    TR_ID: C16694105
    NAME: Place a Bet when user is Logged In.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Add test event, PROD: Find active football event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'Found Football event with outcomes "{self.selection_ids}"')
            self.__class__.team1, self.__class__.team2 = list(self.selection_ids.keys())[0], list(self.selection_ids.keys())[-1]
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
            self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
            self.__class__.selection_ids = event_params.selection_ids

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that have enough money to place bet
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_make_selection(self):
        """
        DESCRIPTION: Add selection to betslip. Betslip counter is increased to value which is equal to quantity of added selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team2])

    def test_003_go_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Verify Betslip with bets details is opened
        """
        bet_info = self.place_and_validate_single_bet()
        expected_user_balance = self.user_balance - bet_info['total_stake']
        page = 'betreceipt' if self.device_type in ['mobile', 'tablet'] else 'all'
        self.verify_user_balance(expected_user_balance=expected_user_balance, page=page, timeout=5)

        self.check_bet_receipt_is_displayed()
        self.check_bet_receipt(betslip_info=bet_info)
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0

    def test_004_go_to_settings_switch_odds_format_to_decimal_and_go_back_to_bet_receipt_page(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format to Decimal and go back to Bet Receipt page
        EXPECTED: Odds are shown in Decimal format
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

    def test_005_add_again_selections_to_the_bet_slip_and_open_betslip(self):
        """
        DESCRIPTION: Tap 'Reuse Selection' button on Bet Receipt page
        EXPECTED: User is returned to the Betslip to initiate bet placement again on the same selections
        """
        self.test_002_make_selection()

    def test_006_place_bet_and_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify 'Done' button on Bet Receipt page
        EXPECTED: Bet Slip slider closes
        EXPECTED: User stays on the same age
        """
        self.test_003_go_to_betslip_and_place_bet()
