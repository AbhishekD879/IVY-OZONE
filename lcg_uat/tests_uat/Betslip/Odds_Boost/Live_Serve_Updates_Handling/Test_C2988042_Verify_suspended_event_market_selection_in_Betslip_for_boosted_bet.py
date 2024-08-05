import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C2988042_Verify_suspended_event_market_selection_in_Betslip_for_boosted_bet(BaseBetSlipTest):
    """
    TR_ID: C2988042
    NAME: Verify suspended event/market/selection in Betslip for boosted bet
    DESCRIPTION: This test case verifies suspended event/market/selection in Betslip for boosted bet
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to Betslip
    PRECONDITIONS: Tap 'Boost' button
    """
    keep_browser_open = True
    username = tests.settings.betplacement_user

    def test_000_pre_conditions(self):
        event = self.ob_config.add_football_event_to_england_premier_league()
        self.__class__.event_id = event.event_id
        self.__class__.selection_name = event.team1
        selection_ids = event.selection_ids[event.team1]
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection')
        self.site.login(username=self.username)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.site.wait_content_state_changed()
        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()

    def test_001_make_eventmarketselection_suspended_for_added_selection_from_precondition_in_httpsbackoffice_tst2coralcoukti(self):
        """
        DESCRIPTION: Make event/market/selection suspended (for added selection from precondition) in https://backoffice-tst2.coral.co.uk/ti
        EXPECTED: Suspension overlay is displayed
        """
        self.ob_config.change_event_state(event_id=self.event_id, displayed=True, active=False)
        if self.brand == 'bma':
            self.device.refresh_page()
            self.site.open_betslip()

    def test_002_verify_the_overlay_content_for_suspendedselectionmarketevent(self):
        """
        DESCRIPTION: Verify the overlay content for suspended:
        DESCRIPTION: /selection/market/event
        EXPECTED: **Before OX99**
        EXPECTED: - Odds, Stake, Est. Returns are disabled
        EXPECTED: - Sorry, the outcome has been suspended/
        EXPECTED: Sorry, the market has been suspended/
        EXPECTED: Sorry, the event has been suspended
        EXPECTED: - Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **From OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.__class__.single_section = self.get_betslip_sections().Singles
        stake = self.single_section.get(self.selection_name)
        self.assertTrue(stake, msg=f'Stake: "{self.selection_name}" section not found')
        self.verify_betslip_is_suspended(stakes=[stake])

    def test_003_verify_that_the_boost_remain_selected_when_the_suspension_ends(self):
        """
        DESCRIPTION: Verify that the boost remain selected when the suspension ends
        EXPECTED: When the suspension ends the boost remains selected
        """
        self.ob_config.change_event_state(event_id=self.event_id, displayed=True, active=True)
        stake_name, stake = list(self.single_section.items())[0]
        self.assertFalse(stake.has_boosted_odds, msg=f'for "{stake_name}" Boosted odds is showing up')
