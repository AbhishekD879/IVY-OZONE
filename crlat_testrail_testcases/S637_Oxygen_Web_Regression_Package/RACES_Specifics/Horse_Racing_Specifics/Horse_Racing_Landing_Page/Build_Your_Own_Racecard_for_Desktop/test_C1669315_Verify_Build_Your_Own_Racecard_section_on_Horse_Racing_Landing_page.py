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
class Test_C1669315_Verify_Build_Your_Own_Racecard_section_on_Horse_Racing_Landing_page(Common):
    """
    TR_ID: C1669315
    NAME: Verify 'Build Your Own Racecard' section on 'Horse Racing' Landing page
    DESCRIPTION: This test case verifies 'Build Your Own Racecard' section on 'Horse Racing' Landing page.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page___featured_tab(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page -> 'Featured' tab
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is selected by default
        EXPECTED: * 'Build Your Own Racecard' section with text block and 'Build a Racecard' button is displayed at the top of the main content area and below the tabs
        """
        pass

    def test_002_verify_text_block(self):
        """
        DESCRIPTION: Verify text block
        EXPECTED: Text says: "Begin to Build Your Own Racecard. Select up to 10 races from any UK, IRE and International meetings"
        """
        pass

    def test_003_click_on_build_a_racecard_button(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button
        EXPECTED: * 'Build a Racecard' button is clickable
        EXPECTED: * 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        EXPECTED: * Text at 'Build Your Own Racecard' section remains the same
        """
        pass

    def test_004_click_on_exit_builder_button(self):
        """
        DESCRIPTION: Click on 'Exit Builder' button
        EXPECTED: * 'Exit Builder' button is clickable
        EXPECTED: * 'Exit Builder' button with 'Close' icon is replaced by 'Build a Racecard'
        EXPECTED: * Text at 'Build Your Own Racecard' section remains the same
        """
        pass

    def test_005_click_on_build_a_racecard_button_again(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button again
        EXPECTED: 
        """
        pass

    def test_006_click_on_close_icon(self):
        """
        DESCRIPTION: Click on 'Close' icon
        EXPECTED: * 'Close' icon is clickable
        EXPECTED: * 'Exit Builder' button with 'Close' icon is replaced by 'Build a Racecard' button
        EXPECTED: * Text at 'Build Your Own Racecard' section remains the same
        """
        pass
