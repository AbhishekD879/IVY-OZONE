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
class Test_C59925224_Verify_Next_race_Panel_display_by_placing_bet_on_any_other_sport_but_not_HR(Common):
    """
    TR_ID: C59925224
    NAME: Verify Next race Panel display by placing  bet on any other sport but not HR
    DESCRIPTION: Verify that Next races Panel is not displayed in the Bet receipt when User places bet on sports and Grey Hound racing
    PRECONDITIONS: 1: Racing Post Tip should not be available and displayed
    PRECONDITIONS: 2: User should **NOT** place single Bet on Horse racing
    PRECONDITIONS: 3: Next races should be available
    PRECONDITIONS: 4: Next Races toggle should be enabled in CMS
    PRECONDITIONS: Note: Racing post tip & Next Races should never be displayed at the same time.
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokescoral_app(self):
        """
        DESCRIPTION: Login to Ladbrokes/Coral App
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_mobile__desktop_navigate_to_any_sport_footballvolleyballtennis_add_one_selection_from_any_sport_event_to_bet_slip_and_place_bet(self):
        """
        DESCRIPTION: **Mobile & Desktop**
        DESCRIPTION: * Navigate to ANY Sport (Football/Volleyball/Tennis....)
        DESCRIPTION: * Add one selection from any sport event to Bet slip and Place Bet
        EXPECTED: Bet receipt should be generated
        """
        pass

    def test_003_validate_next_races_panel_display(self):
        """
        DESCRIPTION: Validate Next races Panel display
        EXPECTED: Next races panel should not be displayed
        """
        pass

    def test_004_mobile__desktop_navigate_to_grey_hound_racing_add_one_selection_from_any_grey_hound_racing_to_bet_slip_and_place_bet(self):
        """
        DESCRIPTION: **Mobile & Desktop**
        DESCRIPTION: * Navigate to Grey Hound Racing
        DESCRIPTION: * Add one selection from any Grey Hound Racing to Bet slip and Place Bet
        EXPECTED: Bet receipt should be generated
        """
        pass

    def test_005_validate_next_races_panel_display(self):
        """
        DESCRIPTION: Validate Next races Panel display
        EXPECTED: Next races panel should not be displayed
        """
        pass

    def test_006_only_mobilerepeat_step_23_4__5_via_quick_bet(self):
        """
        DESCRIPTION: **ONLY MOBILE**
        DESCRIPTION: Repeat Step 2,3, 4 & 5 via Quick Bet
        EXPECTED: Next races panel should not be displayed
        """
        pass
