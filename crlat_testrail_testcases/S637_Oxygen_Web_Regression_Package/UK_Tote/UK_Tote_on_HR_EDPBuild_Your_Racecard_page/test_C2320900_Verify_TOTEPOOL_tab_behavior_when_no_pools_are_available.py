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
class Test_C2320900_Verify_TOTEPOOL_tab_behavior_when_no_pools_are_available(Common):
    """
    TR_ID: C2320900
    NAME: Verify TOTEPOOL tab behavior when no pools are available
    DESCRIPTION: This test case verifies the presence of the UK Tote tab & navigation through available tote types using the switcher
    PRECONDITIONS: * Horse Racing Events **with** at least one UK Tote pool available (Exacta, Trifecta, Quadpot, Placepot, Jackpot, Scoop 6)
    PRECONDITIONS: * Horse Racing Events **without** UK Tote pool available (Exacta, Trifecta, Quadpot, Placepot, Jackpot, Scoop 6)
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tote" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Totepool are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    PRECONDITIONS: Enable UK Tote feature in CMS (check the checkbox) and save changes
    """
    keep_browser_open = True

    def test_001_navigate_to_the_hr_edpbuild_your_racecard_page_with_at_least_one_uk_tote_pool_available(self):
        """
        DESCRIPTION: Navigate to the HR EDP/Build Your Racecard page **with** at least one UK Tote pool available
        EXPECTED: * "Totepools" tab is available
        EXPECTED: * "Totepools" tab is displayed after main market tabs
        """
        pass

    def test_002_navigate_to_the_hr_edpbuild_your_racecard_page_without_uk_tote_pool_are_available(self):
        """
        DESCRIPTION: Navigate to the HR EDP/Build Your Racecard page **without** UK Tote pool are available
        EXPECTED: * "Totepools" tab is **NOT** available
        EXPECTED: * "Totepools" tab is **NOT** displayed after main market tabs
        """
        pass
