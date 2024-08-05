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
class Test_C37568644_Verify_Tapping_on_Odds_button(Common):
    """
    TR_ID: C37568644
    NAME: Verify Tapping on Odds button
    DESCRIPTION: This test case verifies the behavior of 'Odds' button on Greyhound Event card when a user taps on it
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://zpl.io/agBGM6Z
    DESCRIPTION: Coral:
    DESCRIPTION: https://zpl.io/aR0YNZ0
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - The Greyhound module is present on Featured Tab
    PRECONDITIONS: - The Greyhound Racing module includes one or more Greyhound Events
    """
    keep_browser_open = True

    def test_001_user_taps_on_an_odds_button_on_greyhound_event_card(self):
        """
        DESCRIPTION: User taps on an Odds Button on Greyhound Event card
        EXPECTED: Odds button must be highlighted in color
        EXPECTED: ![](index.php?/attachments/get/45687931)
        """
        pass

    def test_002_the_user_taps_the_selected_odds_again(self):
        """
        DESCRIPTION: The user taps the selected Odds again
        EXPECTED: Odds button returns to the original color
        EXPECTED: ![](index.php?/attachments/get/45687940)
        """
        pass
