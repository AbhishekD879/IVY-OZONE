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
class Test_C2320899_Verify_CMS_configuration_for_UK_Tote(Common):
    """
    TR_ID: C2320899
    NAME: Verify CMS configuration for UK Tote
    DESCRIPTION: This test case verifies CMS configuration for UK Tote
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-27761 UK Tote : Totepool ON/OFF CMS config] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-27761
    PRECONDITIONS: * Horse Racing Events with at least one UK Tote pool are available (Exacta, Trifecta, Quadpot, Placepot, Jackpot, Scoop 6)
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tote" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Totepool are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (Tote Pools->Enable_ UK_ Totepools) (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_navigate_to_the_hr_edpbuild_your_racecard_page_with_uk_tote_pools_available(self):
        """
        DESCRIPTION: Navigate to the HR EDP/Build Your Racecard page with UK Tote pools available
        EXPECTED: * "Totepools" tab is available
        EXPECTED: * "Totepools" tab is displayed after main market tabs
        """
        pass

    def test_002_disable_uk_tote_feature_in_cms_uncheck_the_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Disable UK Tote feature in CMS (uncheck the checkbox) and save changes
        EXPECTED: * Checkbox is unchecked
        EXPECTED: * Changes saved successfully
        """
        pass

    def test_003_navigate_to_the_hr_edpbuild_your_racecard_page_with_uk_tote_pools_available(self):
        """
        DESCRIPTION: Navigate to the HR EDPBuild Your Racecard page with UK Tote pools available
        EXPECTED: * "Totepools" tab is NOT available
        EXPECTED: * "Totepools" tab is NOT displayed after main market tabs
        """
        pass
