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
class Test_C25039115_Verify_selections_design_on_Horse_Racing_Event_card(Common):
    """
    TR_ID: C25039115
    NAME: Verify selections design on Horse Racing Event card
    DESCRIPTION: This test case verifies selections design on Horse Racing Event card when amount of the selections are different (min 2, max 4 selections)
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d7766d3cba5d54eb5d8fad3
    DESCRIPTION: Coral:
    DESCRIPTION: https://app.zeplin.io/project/5da04022f2c331081a4c9961/screen/5da0531c74c7950852a0e0dd
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default on Home page
    PRECONDITIONS: * A Horse Racing module is present on Featured Tab
    PRECONDITIONS: * The Horse Racing module includes one ore more Horse Racing Events
    """
    keep_browser_open = True

    def test_001_navigate_to_the_horse_racing_module_on_featured_tab(self):
        """
        DESCRIPTION: Navigate to the Horse Racing module on Featured tab
        EXPECTED: User is viewing the Horse Racing Event card(s)
        """
        pass

    def test_002_emulate_case_when_horse_racing_event_cards_has_only_2_selections(self):
        """
        DESCRIPTION: Emulate case when Horse Racing Event card(s) has only 2 selections
        EXPECTED: The Horse Racing Event card(s) with 2 selections should correspond the design:
        EXPECTED: ![](index.php?/attachments/get/79445)
        """
        pass

    def test_003_emulate_case_when_horse_racing_event_cards_has_more_than2_selections(self):
        """
        DESCRIPTION: Emulate case when Horse Racing Event card(s) has more than
        DESCRIPTION: 2 selections
        EXPECTED: The Horse Racing Event card(s) with more than 2 selections should correspond the design:
        EXPECTED: Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/79446)
        EXPECTED: Coral
        EXPECTED: ![](index.php?/attachments/get/79447)
        """
        pass
