import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2553331_Banach_Format_of_Player_Markets_selection_on_dashboard(Common):
    """
    TR_ID: C2553331
    NAME: Banach. Format of Player Markets selection on dashboard
    DESCRIPTION: Test case verifies selection format of Banach Player Markets
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Player Markets examples**
    PRECONDITIONS: Player Markets: First Goalscorer, Anytime Goalscorer, Player to score 2+ goals, To be shown a card, Player to get first booking
    PRECONDITIONS: **Build Your bet (for Coral) / Bet Builder (for Ladbrokes) tab is opened**
    """
    keep_browser_open = True

    def test_001_add_selections_from_available_player_markets_to_dashboardverify_selections_name_format(self):
        """
        DESCRIPTION: Add selections from available Player Markets to dashboard
        DESCRIPTION: Verify selections name format
        EXPECTED: Selections names have the following format in dashboard
        EXPECTED: [Market name SELECTION] - for Coral
        EXPECTED: ![](index.php?/attachments/get/114303312)
        EXPECTED: [Market name - Selection] - for Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/114303313)
        """
        pass
