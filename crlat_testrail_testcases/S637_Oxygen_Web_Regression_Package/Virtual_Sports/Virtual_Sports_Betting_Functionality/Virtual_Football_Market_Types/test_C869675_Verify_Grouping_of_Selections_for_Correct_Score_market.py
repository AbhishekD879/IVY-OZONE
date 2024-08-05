import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869675_Verify_Grouping_of_Selections_for_Correct_Score_market(Common):
    """
    TR_ID: C869675
    NAME: Verify Grouping of Selections for Correct Score market
    DESCRIPTION: This test case verifies selections grouping  in Correct Score section.
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_virtual_football_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Football' sport page
        EXPECTED: 'Virtual Football' sport page is opened
        """
        pass

    def test_002_go_to_correct_score_section(self):
        """
        DESCRIPTION: Go to 'Correct Score' section
        EXPECTED: 
        """
        pass

    def test_003_verify_selectionsgrouping(self):
        """
        DESCRIPTION: Verify selections grouping
        EXPECTED: Selections are grouped by team and divided into three colums:
        EXPECTED: Team 1
        EXPECTED: ‘outcomeMeaningMinorCode’=‘H’ is a Home Win
        EXPECTED: Draw
        EXPECTED: ‘outcomeMeaningMinorCode’=‘D’ is a Draw
        EXPECTED: Team 2
        EXPECTED: ‘outcomeMeaningMinorCode’=‘A’ - is an Away Win
        """
        pass

    def test_004_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Selections are grouped by team and divided into three colums:
        EXPECTED: Team 1
        EXPECTED: ‘outcomeMeaningMinorCode’=‘H’ is a Home Win
        EXPECTED: Draw
        EXPECTED: ‘outcomeMeaningMinorCode’=‘D’ is a Draw
        EXPECTED: Team 2
        EXPECTED: ‘outcomeMeaningMinorCode’=‘A’ - is an Away Win
        """
        pass
