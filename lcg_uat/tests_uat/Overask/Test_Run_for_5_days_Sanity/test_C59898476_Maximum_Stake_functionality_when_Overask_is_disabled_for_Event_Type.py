import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898476_Maximum_Stake_functionality_when_Overask_is_disabled_for_Event_Type(BaseBetSlipTest):
    """
    TR_ID: C59898476
    NAME: Maximum Stake functionality when Overask is disabled for Event Type
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    PRECONDITIONS: In OB go to any sport(Ex -Football -->  Premier league ) disable BI check box at Type level
    """
    keep_browser_open = True
    min_bet = 0.1
    max_bet = 0.25
    bet_amount = 0.3
    expected_max_bet_msg = vec.Betslip.MAX_STAKE.format(max_bet)
    draw_stake_title = vec.sb.DRAW.title()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        self.__class__.selection_ids = \
            self.ob_config.add_football_event_to_special_league(min_bet=self.min_bet,
                                                                max_bet=self.max_bet).selection_ids

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow should not be triggered instead Customer should see a message showing the max stake
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.draw_stake_title])
        self.place_single_bet()
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.draw_stake_title)
        self.assertTrue(stake, msg=f'No stake with name "{self.draw_stake_title}" found')
        self.verify_user_balance(expected_user_balance=self.user_balance)
        error_message = stake.wait_for_error_message()
        self.assertEqual(error_message, self.expected_max_bet_msg,
                         msg=f'Actual message:"{error_message}" is not as expected:"{self.expected_max_bet_msg}"')
