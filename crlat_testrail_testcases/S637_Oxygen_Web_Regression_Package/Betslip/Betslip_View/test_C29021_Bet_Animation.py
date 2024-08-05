import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29021_Bet_Animation(Common):
    """
    TR_ID: C29021
    NAME: Bet Animation
    DESCRIPTION: This test case verifies animation of bet that is moving to Betslip
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-6826 Animation of bet moving to betslip
    DESCRIPTION: *   BMA-36841 Betslip animation and full page coverage
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_coral_and_ladbrokes_add_selection_to_betslip(self):
        """
        DESCRIPTION: Coral and Ladbrokes: Add selection to Betslip
        EXPECTED: *   Betslip counter is increased by 1
        EXPECTED: *   Selection is added to Betslip with animation for Coral
        EXPECTED: *   Selection is added to Betslip with animation for Ladbrokes (Selections counter is blinking for two times)
        """
        pass

    def test_003_verify_animation_presence_across_app(self):
        """
        DESCRIPTION: Verify animation presence across app
        EXPECTED: Animation works for all sections on all pages
        """
        pass

    def test_004_coral_unselectchosen_selection(self):
        """
        DESCRIPTION: Coral: Unselect chosen selection
        EXPECTED: *   Betslip counter is decreased by 1
        EXPECTED: *   Animation does not work while user unselects selection
        """
        pass

    def test_005_ladbrokes_unselectchosen_selection(self):
        """
        DESCRIPTION: Ladbrokes: Unselect chosen selection
        EXPECTED: *   Betslip counter is decreased by 1
        EXPECTED: *   Animation is displayed while user unselects selection (Selections counter is blinking for two times)
        """
        pass
