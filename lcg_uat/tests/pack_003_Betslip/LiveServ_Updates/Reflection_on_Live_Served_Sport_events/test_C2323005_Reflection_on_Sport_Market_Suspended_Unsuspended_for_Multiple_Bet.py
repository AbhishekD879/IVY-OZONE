import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.high
@vtest
class Test_C2323005_Betslip_Reflection_on_Sport_Market_Suspended_Unsuspended_for_Multiple_Bet(BaseBetSlipTest):
    """
    TR_ID: C2323005
    NAME: Betslip Reflection on <Sport> Market Suspended/Unsuspended for Multiple Bet
    DESCRIPTION: This test case verifies Betslip reflection for Multiples section when Market is Suspended.
    PRECONDITIONS: Access to OB TI is required
    """
    keep_browser_open = True

    def test_001_add_a_few_selections_from_different_active_events(self):
        """
        DESCRIPTION: Add a few selections from different active events
        EXPECTED: 'Multiples' section is shown on the Betslip
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.eventID = event.event_id
        self.__class__.marketID = self.ob_config.market_ids[event.event_id][market_short_name]
        self.__class__.team1 = event.team1

        event2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID_2 = event2.event_id
        self.__class__.marketID_2 = self.ob_config.market_ids[event2.event_id][market_short_name]
        self.__class__.team2 = event2.team2

        self.open_betslip_with_selections(selection_ids=(event.selection_ids[self.team1],
                                                         event2.selection_ids[self.team2]))
        self.__class__.multiples_section = self.get_betslip_sections(multiples=True).Multiples

    def test_002_suspend_market_for_one_of_the_events(self):
        """
        DESCRIPTION: Suspend market for one of the events:
        DESCRIPTION: **marketStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages/labels are displayed for active selections
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(all(selection in singles_section for selection in (self.team1, self.team2)),
                        msg=f'"{self.team1}" & "{self.team2}" was not found in "{singles_section}"')
        stake = singles_section[self.team1]

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)

        self.verify_betslip_is_suspended(stakes=[stake], verify_overlay_message=False)

        active_stake = singles_section[self.team2]
        stake_error_message = active_stake.wait_for_error_message(expected_result=False)
        self.assertFalse(stake_error_message,
                         msg=f'Stake error message "{stake_error_message}" for "{self.team2}" is shown')
        self.assertFalse(active_stake.is_suspended(expected_result=False), msg=f'Stake "{self.team2}" is suspended')
        self.__class__.singles_section = singles_section

    def test_003_unsuspend_the_same_market(self):
        """
        DESCRIPTION: Unsuspend the same market:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)

        stake = self.singles_section[self.team1]

        self.verify_betslip_is_active(stakes=[stake], is_stake_filled=False)

    def test_004_enter_stake_for_the_multiple_bet(self):
        """
        DESCRIPTION: Enter Stake for the Multiple bet
        EXPECTED:
        """
        stake = self.multiples_section.get(vec.betslip.DBL)
        self.assertTrue(stake, msg=f'"{vec.betslip.DBL}" stake '
                                   f'is not found in "{self.multiples_section.keys()}"')
        stake.amount_form.input.value = self.bet_amount
        self.__class__.stake = stake

    def test_005_suspend_two_markets_for_two_events(self):
        """
        DESCRIPTION: Suspend two markets for two events:
        DESCRIPTION: **marketStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages are displayed for active selections
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware some of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Some of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'Some of your selections have been suspended' with duration: 5s
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)
        self.ob_config.change_market_state(event_id=self.eventID_2, market_id=self.marketID_2, displayed=True)

        self.verify_betslip_is_suspended(stakes=self.singles_section.values())

    def test_006_unsuspend_the_same_market(self):
        """
        DESCRIPTION: Unsuspend the same market:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.ob_config.change_market_state(event_id=self.eventID_2, market_id=self.marketID_2,
                                           displayed=True, active=True)

        self.verify_betslip_is_active(stakes=self.singles_section.values(), is_stake_filled=True)
