import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66130507_Verify_displayed_with_the_celebrating_success_for_user_wins_the_bet(Common):
    """
    TR_ID: C66130507
    NAME: Verify displayed with the celebrating success for user  wins the bet
    DESCRIPTION: This test case verify displayed with the celebrating success for user  wins the bet
    PRECONDITIONS: User should login successfully with valid credentials
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_navigate_to_any_sportrace(self):
        """
        DESCRIPTION: Navigate to any Sport/Race
        EXPECTED: Sports/racing EDP page should be open
        """
        pass

    def test_002_click_on_the_selection_single_multiple(self):
        """
        DESCRIPTION: Click on the selection single /multiple
        EXPECTED: Selection should be added to bet slip
        """
        pass

    def test_003_enter_stake_on_single_multiples_and_click_on_place_bet_cta(self):
        """
        DESCRIPTION: Enter stake on single /multiples and click on place bet CTA
        EXPECTED: Bets should be placed successfully for singles and multiples
        """
        pass

    def test_004_navigate_to_my_bets_ampgtopen(self):
        """
        DESCRIPTION: Navigate to My Bets-&amp;gt;Open
        EXPECTED: Open tab is available with the bets
        """
        pass

    def test_005_check_for_the_bets_places(self):
        """
        DESCRIPTION: Check for the bets places
        EXPECTED: Bets should be available for singles and multiples
        """
        pass

    def test_006_tab_on_settled(self):
        """
        DESCRIPTION: Tab on settled
        EXPECTED: settled bets tab is opened
        """
        pass

    def test_007_check_for_the_above_bets_after_settled_and_its_should_be_win(self):
        """
        DESCRIPTION: Check for the above bets after settled and its should be Win
        EXPECTED: User should be displayed with "You won: &Acirc;&pound;XX.00 and with Green background as per Figma deign
        EXPECTED: **Screen**
        EXPECTED: ![](index.php?/attachments/get/26c19817-8667-406c-b10b-34561721f1cf)
        """
        pass

    def test_008_repeat_the_above_steps_for_lottos_and_pools(self):
        """
        DESCRIPTION: Repeat the above steps for Lottos and pools
        EXPECTED: 
        """
        pass
