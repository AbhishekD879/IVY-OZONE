import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.high
@pytest.mark.desktop
@vtest
class Test_C29063_Reflection_on_Sport_Market_Suspended_Unsuspended_for_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C29063
    NAME: Reflection on Sport Market Suspended/Unsuspended for Single Bet
    DESCRIPTION: This test case verifies Betslip reflection for Single bet when its Market is Suspended
    PRECONDITIONS: Access to OB TI is required
    """
    keep_browser_open = True

    def test_001_add_single_sport_bet_to_the_betslip(self):
        """
        DESCRIPTION: Add single <Sport> bet to the Betslip
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.eventID = event.event_id
        self.__class__.team1 = event.team1
        self.__class__.marketID = self.ob_config.market_ids[event.event_id][market_short_name]
        self.open_betslip_with_selections(selection_ids=event.selection_ids[self.team1])

    def test_002_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is opened, selection is displayed
        """
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'Stake "{self.team1}" was not found')
        self.__class__.stake = stake

    def test_003_enter_stake(self):
        """
        DESCRIPTION: Enter Stake
        """
        self.stake.amount_form.input.value = self.bet_amount

    def test_004_trigger_suspension_of_the_market(self):
        """
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)

        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_005_make_the_market_active_again(self):
        """
        DESCRIPTION: Make the market active again:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * Selection become enabled
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button enabled
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, active=True, displayed=True)

        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=True)
