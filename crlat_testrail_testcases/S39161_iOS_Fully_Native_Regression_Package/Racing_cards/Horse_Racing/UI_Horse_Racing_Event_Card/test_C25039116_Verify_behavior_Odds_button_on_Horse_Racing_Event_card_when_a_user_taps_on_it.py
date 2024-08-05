import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C25039116_Verify_behavior_Odds_button_on_Horse_Racing_Event_card_when_a_user_taps_on_it(Common):
    """
    TR_ID: C25039116
    NAME: Verify behavior Odds button on Horse Racing Event card when a user taps on it
    DESCRIPTION: This test case behavior Odds button on Horse Racing Event card when a user taps on it
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d7766d3cba5d54eb5d8fad3
    DESCRIPTION: Coral:
    DESCRIPTION: https://app.zeplin.io/project/5da04022f2c331081a4c9961/screen/5da0531c74c7950852a0e0dd
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default
    PRECONDITIONS: * The Horse Racing module is present on Featured Tab
    PRECONDITIONS: * The Horse Racing module includes one ore more Horse Racing Events
    """
    keep_browser_open = True

    def test_001_user_taps_on_an_odds_button_on_horse_racing_event_card(self):
        """
        DESCRIPTION: User taps on an Odds Button on Horse Racing Event card
        EXPECTED: Odds button must be highlighted in Colour
        EXPECTED: ![](index.php?/attachments/get/42440)
        """
        pass

    def test_002_user_taps_the_selected_odds_again(self):
        """
        DESCRIPTION: User taps the selected Odds again
        EXPECTED: Odds button returns to original colour
        EXPECTED: ![](index.php?/attachments/get/45599)
        """
        pass
