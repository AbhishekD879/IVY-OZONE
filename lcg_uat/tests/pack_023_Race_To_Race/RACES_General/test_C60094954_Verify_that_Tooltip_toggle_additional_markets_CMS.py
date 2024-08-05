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
class Test_C60094954_Verify_that_Tooltip_toggle_additional_markets_CMS(Common):
    """
    TR_ID: C60094954
    NAME: Verify that  Tooltip toggle- additional markets- CMS
    DESCRIPTION: Verify that Tool tip toggle is available in CMS for additional markets display in HR & GH events EDP
    PRECONDITIONS: 1: User should be able to access CMS
    """
    keep_browser_open = True

    def test_001_launch_cms_application(self):
        """
        DESCRIPTION: Launch CMS application
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_system_configuration(self):
        """
        DESCRIPTION: Click on System Configuration
        EXPECTED: User should be able to click and view System Configuration
        """
        pass

    def test_003_search_for_tooltip_toggle(self):
        """
        DESCRIPTION: Search for Tooltip toggle
        EXPECTED: 1: User should be able to view enabled/disabled options for the Tooltip toggle
        EXPECTED: 2: User should be able to Enable or disable on clicking
        EXPECTED: 3: User should be displayed Tooltip text box
        """
        pass

    def test_004_validate_enable_disable(self):
        """
        DESCRIPTION: Validate Enable /Disable
        EXPECTED: User should be able to Save the changes either by Enable or disable
        """
        pass

    def test_005_validate_tooltip_text(self):
        """
        DESCRIPTION: Validate Tooltip text
        EXPECTED: 1: User should be able to enter text in the Tool tip text box
        EXPECTED: 2: User should be able to save the changes
        EXPECTED: 3: User should be able to enter text upto 100 characters
        EXPECTED: 4: Save changes button should be disabled when user enter text more than 100 characters
        """
        pass
