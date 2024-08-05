import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C37568642_Verify_Interacting_with_Event_Card(Common):
    """
    TR_ID: C37568642
    NAME: Verify Interacting with Event Card
    DESCRIPTION: This test case verifies  interacting with Event Card
    DESCRIPTION: This Test Case Verifies Interacting with Greyhound Event Cards.
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://zpl.io/agBGM6Z
    DESCRIPTION: Coral:
    DESCRIPTION: https://zpl.io/aR0YNZ0
    PRECONDITIONS: Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Featured Tab is displayed by default on the Home page
    PRECONDITIONS: A Greyhounds module is present on Featured Tab
    PRECONDITIONS: The Greyhound module includes one Greyhound Event
    """
    keep_browser_open = True

    def test_001_navigate_to_the_greyhound_module_on_featured_tab(self):
        """
        DESCRIPTION: Navigate to the Greyhound module on Featured tab
        EXPECTED: User is viewing the Greyhound Event card(s)
        EXPECTED: - User see Greyhound Card which size fits within the allocated space
        EXPECTED: - User can't swipe displayed Greyhound Card to the right or the left
        """
        pass

    def test_002_emulate_that_greyhound_module_includes_2_greyhound_event(self):
        """
        DESCRIPTION: Emulate that Greyhound module includes >=2 Greyhound Event
        EXPECTED: Greyhound Card carousel is available
        EXPECTED: The first Greyhound Card is displayed wholly, the next one is displayed partially
        """
        pass

    def test_003_swipe_left(self):
        """
        DESCRIPTION: Swipe left
        EXPECTED: The 2nd Greyhound Card is displayed wholly, the previous one is displayed partially
        """
        pass

    def test_004_swipe_right(self):
        """
        DESCRIPTION: Swipe right
        EXPECTED: The first Greyhound Card is displayed wholly, the next one is displayed partially
        """
        pass
