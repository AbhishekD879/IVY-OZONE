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
class Test_C58421264_Verify_Unnamed_Favourite_displaying_on_Totepool_tabs(Common):
    """
    TR_ID: C58421264
    NAME: Verify "Unnamed Favourite" displaying on Totepool tabs
    DESCRIPTION: This test case verifies that "Unnamed Favourite" should be available for Quadpot, Placepot, Jackpot and Scoop 6 but NOT Win, Place, Exacta, and Trifecta
    PRECONDITIONS: Horse Racing Events with at least one UK Tote pool available (Place, Win, Exacta, Trifecta, Quadpot, Placepot, Jackpot, Scoop 6)
    PRECONDITIONS: Unnamed Favourite should be available for current Horse Racing Event.
    PRECONDITIONS: - User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: - Navigate to HR landing page
    PRECONDITIONS: - Choose the particular event from the 'Race Grid'
    PRECONDITIONS: - Select 'Tote' tab
    """
    keep_browser_open = True

    def test_001_select_win_tab(self):
        """
        DESCRIPTION: Select 'Win tab
        EXPECTED: - 'Win' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        pass

    def test_002_select_place_tab(self):
        """
        DESCRIPTION: Select 'Place' tab
        EXPECTED: - 'Place' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        pass

    def test_003_select_exacta_tab(self):
        """
        DESCRIPTION: Select 'Exacta' tab
        EXPECTED: - 'Exacta' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        pass

    def test_004_select_trifecta_tab(self):
        """
        DESCRIPTION: Select 'Trifecta' tab
        EXPECTED: - 'Trifecta' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        pass

    def test_005_select_placepot_tab(self):
        """
        DESCRIPTION: Select 'Placepot' tab
        EXPECTED: - 'Placepot' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        pass

    def test_006_select_quadpot_tab(self):
        """
        DESCRIPTION: Select 'Quadpot' tab
        EXPECTED: - 'Quadpot' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        pass

    def test_007_select_jackpot_tab(self):
        """
        DESCRIPTION: Select 'Jackpot' tab
        EXPECTED: - 'Jackpot' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        pass

    def test_008_select_scoop_6_tab(self):
        """
        DESCRIPTION: Select 'Scoop 6' tab
        EXPECTED: - 'Scoop 6' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        pass
