import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1502178_Displaying_of_Knockout_Rounds_sections(Common):
    """
    TR_ID: C1502178
    NAME: Displaying of Knockout Rounds sections
    DESCRIPTION: This test case verifies displaying of Knockout Rounds skeleton which is configured in CMS
    PRECONDITIONS: - Big Competition > Competition (e.g. World Cup) is configured in CMS
    PRECONDITIONS: - All Knockout Rounds (Round of 16, Quarterfinals, Semifinals, Finals) are correctly configured in CMS. Use test case:  https://ladbrokescoral.testrail.com/index.php?/cases/view/1473948
    PRECONDITIONS: - Coral app is opened
    PRECONDITIONS: - To check MS response go to Network > {tab ID} (response) > "competitionModules" >"rounds"
    """
    keep_browser_open = True

    def test_001_navigate_to_competition_eg_world_cup__tab_eg_knockouts(self):
        """
        DESCRIPTION: Navigate to Competition (e.g. World Cup) > Tab (e.g. 'Knockouts')
        EXPECTED: Knockouts tab is opened
        """
        pass

    def test_002_verify_displaying_of_knockout_rounds_section(self):
        """
        DESCRIPTION: Verify displaying of Knockout Rounds section
        EXPECTED: - Sections are available and displayed in order:
        EXPECTED: * 'Round of 16'
        EXPECTED: * 'Quarterfinals'
        EXPECTED: * 'Semifinals'
        EXPECTED: * 'Finals'
        EXPECTED: (taken from "name" object in MS response)
        """
        pass

    def test_003_verify_round_of_16_section(self):
        """
        DESCRIPTION: Verify 'Round of 16' section
        EXPECTED: * 8 cards (matches) are available in 'Round of 16' section (taken from "number" in MS response)
        EXPECTED: * All cards (matches) are displayed in 2 columns > one card (match) per column
        EXPECTED: * Each pair of cards (matches) are aligned by 'round winner circle icon' (4 pairs/winners) (depends on the "number" of cards in the next section)
        """
        pass

    def test_004_verify_quarterfinals_section(self):
        """
        DESCRIPTION: Verify 'Quarterfinals' section
        EXPECTED: * 4 cards (matches) are available in 'Quarterfinals' section (taken from "number" in MS response)
        EXPECTED: * All cards (matches) are displayed in 2 columns > one card (match) per column
        EXPECTED: * Each pair of cards (matches) are aligned by 'round winner circle icon' (2 pairs/winners) (depends on the "number" of cards in the next section)
        """
        pass

    def test_005_verify_semifinals_section(self):
        """
        DESCRIPTION: Verify 'Semifinals' section
        EXPECTED: * 2 cards (matches) are available in 'Semifinals' section (taken from "number" in MS response)
        EXPECTED: * Cards (matches) are displayed in 2 columns > one card (match) per column
        EXPECTED: * A pair of cards (matches) are aligned by 'round winner circle icon' (1 pair/winner) (depends on the "number" of cards in in the next section)
        """
        pass

    def test_006_verify_finals_section(self):
        """
        DESCRIPTION: Verify 'Finals' section
        EXPECTED: 1 card (match) is available in 'Finals' section (taken from "number" in MS response)
        """
        pass
