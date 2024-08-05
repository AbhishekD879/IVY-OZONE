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
class Test_C25039117_Verify_behavior_Odds_button_on_Horse_Racing_event_card_when_price_selection_is_changed(Common):
    """
    TR_ID: C25039117
    NAME: Verify behavior Odds button on Horse Racing event card when price selection is changed
    DESCRIPTION: This test case verifies behavior Odds button on Horse Racing event card when price selection is changed
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

    def test_001_emulate_the_selection_price_change_price_up(self):
        """
        DESCRIPTION: Emulate the selection price change (Price up)
        EXPECTED: The Odds Price within Odds Button changes colour as per design
        EXPECTED: (animation' duration is 2000ms)
        EXPECTED: ![](index.php?/attachments/get/42443)
        """
        pass

    def test_002_emulate_the_selection_price_change_down(self):
        """
        DESCRIPTION: Emulate the selection price change (Down)
        EXPECTED: The Odds Price within Odds Button changes colour as per design above
        EXPECTED: (animation duration is 2000ms)
        """
        pass
