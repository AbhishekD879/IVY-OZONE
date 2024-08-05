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
class Test_C25039113_Verify_Information_displayed_on_Horse_Racing_Card_according_to_design(Common):
    """
    TR_ID: C25039113
    NAME: Verify Information displayed on Horse Racing Card according to design
    DESCRIPTION: This test case verifies UI of information displayed on Horse Racing Card when user is viewing an Horse Racing Event
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d7766d3cba5d54eb5d8fad3
    DESCRIPTION: Coral:
    DESCRIPTION: https://app.zeplin.io/project/5da04022f2c331081a4c9961/screen/5da0531c74c7950852a0e0dd
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default on Home page
    PRECONDITIONS: * A Horse Racing module is present on Featured Tab
    PRECONDITIONS: Scope:
    PRECONDITIONS: IN:
    PRECONDITIONS: * UI
    PRECONDITIONS: * Event Card
    PRECONDITIONS: * Horse Racing
    PRECONDITIONS: OUT:
    PRECONDITIONS: * Other sports
    PRECONDITIONS: * Live Price Updates
    PRECONDITIONS: * Live State Updates
    PRECONDITIONS: * Sign-Posting
    """
    keep_browser_open = True

    def test_001_navigate_to_a_horse_racing_module_on_featured_tab(self):
        """
        DESCRIPTION: Navigate to a Horse Racing Module on Featured Tab
        EXPECTED: User is viewing the Horse Racing Event cards in the carousel
        """
        pass

    def test_002_verify_information_displayed_on_the_horse_racingcard(self):
        """
        DESCRIPTION: Verify Information displayed on the Horse Racing
        DESCRIPTION: Card
        EXPECTED: Horse Racing Event card must contain the following information:
        EXPECTED: * Event Name (E.G 14.20 Redcar)
        EXPECTED: * Race Type (E.G Flat Turf)
        EXPECTED: * Ground Condition (E.G Good To Firm)
        EXPECTED: * Distance (E.G 5f)
        EXPECTED: * Countdown Timer (E.G Starts in 15:00)
        EXPECTED: * Each Way Terms (E.G E/W 1/4 Places 1-2-3)
        EXPECTED: * Horse Number
        EXPECTED: * Stall Number (E.G (6) if applicable)
        EXPECTED: * Jockey Silks
        EXPECTED: * Horse Name
        EXPECTED: * Trainer Name (First Name initial followed by Surname)
        EXPECTED: * Jockey Name
        EXPECTED: * If for above any text runs out of space then must truncate text
        EXPECTED: Form
        EXPECTED: * Odds Button
        EXPECTED: * Previous Price
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/58192)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/58194)
        """
        pass
