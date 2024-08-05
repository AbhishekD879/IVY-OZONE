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
class Test_C869673_Verify_Order_of_Selections_for_Under_Over_25_market(Common):
    """
    TR_ID: C869673
    NAME: Verify Order of Selections for Under/Over 2.5 market
    DESCRIPTION: This test case verifies that selections are shown in the followin order: Under 2.5, Over 2.5 in Under/Over 2.5 section.
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

    def test_002_go_to_underover_25_section(self):
        """
        DESCRIPTION: Go to 'Under/Over 2.5' section
        EXPECTED: 
        """
        pass

    def test_003_verify_selectionsorder(self):
        """
        DESCRIPTION: Verify selections order
        EXPECTED: Selections are shown in the following order:
        EXPECTED: Under 2.5
        EXPECTED: Over 2.5
        EXPECTED: or
        EXPECTED: markets are ordered by OB market display order.
        """
        pass

    def test_004_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Selections are shown in the following order:
        EXPECTED: Under 2.5
        EXPECTED: Over 2.5
        EXPECTED: or
        EXPECTED: markets are ordered by OB market display order.
        """
        pass
