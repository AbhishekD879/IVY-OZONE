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
class Test_C25047447_Verify_behavior_Odds_button_on_Horse_Racing_Event_card_when_selection_is_unavailable(Common):
    """
    TR_ID: C25047447
    NAME: Verify behavior Odds button on Horse Racing Event card when selection is unavailable
    DESCRIPTION: This test case verifies behavior Odds button on Horse Racing Card event when selection is suspended.
    DESCRIPTION: Design
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

    def test_001_the_selection_unavailable_case_was_emulated_for_the_horse_racing_event(self):
        """
        DESCRIPTION: The selection unavailable case was emulated for the Horse Racing Event
        EXPECTED: * selection on the Horse Racing Event card is unavailable
        EXPECTED: * 'N/A' title within Odds button is displayed as per design:
        EXPECTED: ![](index.php?/attachments/get/42446)
        """
        pass
