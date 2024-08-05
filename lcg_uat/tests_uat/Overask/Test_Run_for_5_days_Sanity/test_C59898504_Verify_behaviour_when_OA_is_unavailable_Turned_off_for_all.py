import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898504_Verify_behaviour_when_OA_is_unavailable_Turned_off_for_all(BaseBetSlipTest):
    """
    TR_ID: C59898504
    NAME: Verify behaviour when OA is unavailable (Turned off for all)
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is disabled(Turned off for all) for logged in user
    PRECONDITIONS: OpenBet TI--> Home --> BI Settings --> Disable Betting
    """
    keep_browser_open = True
    max_bet = 0.25
    bet_amount = 1.0
    expected_max_bet_msg = vec.betslip.MAX_STAKE.format(max_bet)
    draw_stake_title = vec.sb.DRAW.title()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet,
                                                                                 max_mult_bet=self.max_bet)
        self.__class__.selection_ids = event_params.selection_ids

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: All max bet messages should be returned and no customer should be passed into the flow
        """
        self.site.login(username=tests.settings.disabled_overask_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.draw_stake_title])
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertFalse(overask, msg='Overask is triggered for the User')
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        sleep(5)
        error_message = stake.wait_for_error_message()
        self.assertEqual(error_message, self.expected_max_bet_msg,
                         msg=f'\nActual message: \n"{error_message}" '
                             f'\nis not as expected: \n"{self.expected_max_bet_msg}"')
        self.get_betslip_content().remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()
