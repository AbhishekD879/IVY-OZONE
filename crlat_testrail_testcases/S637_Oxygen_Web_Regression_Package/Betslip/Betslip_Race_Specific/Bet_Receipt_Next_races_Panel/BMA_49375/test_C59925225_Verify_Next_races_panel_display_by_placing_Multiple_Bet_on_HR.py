import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59925225_Verify_Next_races_panel_display_by_placing_Multiple_Bet_on_HR(Common):
    """
    TR_ID: C59925225
    NAME: Verify Next races panel display by placing Multiple Bet on HR
    DESCRIPTION: Verify Next races Panel should not be displayed in the Bet receipt when user places multiple Bet on HR
    PRECONDITIONS: 1: Racing Post Tip should not be available and displayed
    PRECONDITIONS: 2: User should **NOT place single Bet** on Horse racing
    PRECONDITIONS: 3: User should place multiple bet on Horse racing
    PRECONDITIONS: 4: Next races should be available
    PRECONDITIONS: 5: Next Races toggle should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokescoral_app(self):
        """
        DESCRIPTION: Login to Ladbrokes/Coral App
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_mobile__desktop_navigate_to_horse_racing_add_two_or_more_selection_from_any_horse_racing_events_to_bet_slip(self):
        """
        DESCRIPTION: **Mobile & Desktop**
        DESCRIPTION: * Navigate to Horse Racing
        DESCRIPTION: * Add two or more selection from any Horse Racing events to Bet slip
        EXPECTED: * Selections should be added to Betslip
        """
        pass

    def test_003_place_accumulator_or_complex_bet(self):
        """
        DESCRIPTION: Place Accumulator or Complex bet
        EXPECTED: * User should be able to Place bet successfully
        EXPECTED: * Bet Receipt should be generated
        """
        pass

    def test_004_verify_next_races_panel_display(self):
        """
        DESCRIPTION: Verify Next races Panel display
        EXPECTED: Next races panel should bot be displayed
        """
        pass

    def test_005_mobile__desktop_navigate_to_horse_racing_add_two_or_more_selection_from_any_horse_racing_events_to_bet_slip(self):
        """
        DESCRIPTION: **Mobile & Desktop**
        DESCRIPTION: * Navigate to Horse Racing
        DESCRIPTION: * Add two or more selection from any Horse Racing events to Bet slip
        EXPECTED: * Selections should be added to Betslip
        """
        pass

    def test_006_place_multiple_single_bets(self):
        """
        DESCRIPTION: Place Multiple Single Bets
        EXPECTED: * User should be able to Place bet successfully
        EXPECTED: * Bet Receipt should be generated
        """
        pass

    def test_007_verify_next_races_panel_display(self):
        """
        DESCRIPTION: Verify Next races Panel display
        EXPECTED: Next races panel should bot be displayed
        """
        pass

    def test_008_only_mobilerepeat_above_steps_via_quick_bet(self):
        """
        DESCRIPTION: **ONLY MOBILE**
        DESCRIPTION: Repeat above steps via Quick Bet
        EXPECTED: Next races panel should bot be displayed
        """
        pass
