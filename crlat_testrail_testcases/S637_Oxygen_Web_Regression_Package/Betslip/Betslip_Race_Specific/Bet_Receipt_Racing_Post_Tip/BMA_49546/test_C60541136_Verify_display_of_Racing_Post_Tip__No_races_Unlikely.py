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
class Test_C60541136_Verify_display_of_Racing_Post_Tip__No_races_Unlikely(Common):
    """
    TR_ID: C60541136
    NAME: Verify display of Racing Post Tip - No races (Unlikely)
    DESCRIPTION: This test case verifies that **NO** Racing post Tip is displayed when there are no races at all (Highly Unlikely Scenario)
    PRECONDITIONS: 1: Racing Post Tip should be enabled in CMS (Main Bet Receipt and Quick Bet Receipt)
    PRECONDITIONS: 2: No Races should be available
    PRECONDITIONS: **Rules for Tip Display**
    PRECONDITIONS: 1: User should place only single Horse racing Bet
    PRECONDITIONS: Racing Post Tip Display
    PRECONDITIONS: If there is a UK & Ireland race starting in the next 15 minutes, then the Next UK & Ireland race tip will be displayed (ONLY)
    PRECONDITIONS: IF there are no UK & Ireland races available in the next 15 minutes, then the next International race tip will be displayed (ONLY)
    PRECONDITIONS: IF there are no UK & Ireland OR International races TODAY, then the next race (Tomorrow) will be displayed in Racing Post Tip
    PRECONDITIONS: IF there are no races at all (unlikely) - then Racing Post Tip will not be displayed
    PRECONDITIONS: IF a tip for a specific race has already been displayed to a user, then the same tip will NOT be displayed again (a specific race tip is displayed only once per customer)
    PRECONDITIONS: Note: Only ACTIVE selections will be displayed. e.g. Non Runners will not be displayed within the Racing Post Tips
    PRECONDITIONS: Note: Races that a user has already bet on will not display within Racing Post Tip
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_coral(self):
        """
        DESCRIPTION: Login to Ladbrokes /Coral
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_mobile__desktop_navigate_to_horse_racing_add_one_selection_from_any_horse_racing_event_to_bet_slip(self):
        """
        DESCRIPTION: **Mobile & Desktop**
        DESCRIPTION: * Navigate to Horse Racing
        DESCRIPTION: * Add one selection from any Horse Racing event to Bet slip
        EXPECTED: * User should be navigated to Horse Racing landing page
        EXPECTED: * Selection should be added successfully to Main Bet slip
        """
        pass

    def test_003__enter_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: * Enter Stake and click on Place Bet
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Bet Receipt should be displayed
        """
        pass

    def test_004_validate_the_display_of_racing_post_tipno_races_are_available_both_uk__irish__internationalorall_tips_are_already_displayed_to_the_user(self):
        """
        DESCRIPTION: Validate the display of Racing Post Tip
        DESCRIPTION: **No Races are available both UK & Irish , International**
        DESCRIPTION: [OR]
        DESCRIPTION: **All Tips are already displayed to the User**
        EXPECTED: * Racing Post Tip should not be displayed as there are no races available
        EXPECTED: * Racing Post Tip should not be displayed as all the tips are already displayed to the user (No Tips should be repeated to User)
        """
        pass

    def test_005_only_mobileplace_quick_bet_and_validate_the_same(self):
        """
        DESCRIPTION: **Only Mobile**
        DESCRIPTION: Place Quick Bet and validate the same
        EXPECTED: 
        """
        pass
