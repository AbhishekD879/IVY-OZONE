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
class Test_C869671_Verify_Order_of_Selections_for_Double_Chance_market(Common):
    """
    TR_ID: C869671
    NAME: Verify Order of Selections for Double Chance market
    DESCRIPTION: This test case verifies that selections are shown in the followin order: Team1 or Draw, Team2 or Draw, Team1 or Team2 in Double Chance section.
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_virtual_football_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Football' sport page
        EXPECTED: 
        """
        pass

    def test_002_go_to_double_chance_section(self):
        """
        DESCRIPTION: Go to 'Double Chance' section
        EXPECTED: 
        """
        pass

    def test_003_verify_selectionsorder(self):
        """
        DESCRIPTION: Verify selections order
        EXPECTED: Selections are shown in the following order:
        EXPECTED: Team 1 or Draw, Team2 or Draw, Team1 or Team2
        EXPECTED: or
        EXPECTED: markets are ordered by OB market display order.
        """
        pass

    def test_004_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Selections are shown in the following order:
        EXPECTED: Team 1 or Draw, Team2 or Draw, Team1 or Team2
        EXPECTED: or
        EXPECTED: markets are ordered by OB market display order.
        """
        pass
