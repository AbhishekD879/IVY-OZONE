import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C44870168_configure_new_event_market_into_Highlights_tab_and_verify_in_the_FE(Common):
    """
    TR_ID: C44870168
    NAME: configure new event /market into Highlights tab and verify in the FE
    DESCRIPTION: 
    PRECONDITIONS: Configure feature modules in CMS to be displayed on Highlights tab.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_select_featured_tab_modules_from_right_menu_and_click_on_create_featured_tab_module(self):
        """
        DESCRIPTION: Select Featured Tab Modules from right menu and click on 'Create Featured Tab Module'
        EXPECTED: Create Page is loaded. enter the details to configure a new featured tab module. This can be configured based on  EventID/ClassID/Market ID/RacetypeID/SelectionID . User should also select on which devices to publish : Desktop/Tablet/Mobile
        """
        pass

    def test_003_click_on_create_module(self):
        """
        DESCRIPTION: Click on 'Create Module'
        EXPECTED: One all the mandatory details and correct date range is selected, user should be able to save the changes and new feature module should be created.
        """
        pass

    def test_004_load_app_and_verify_the_newly_created_featured_module_on_the_fe(self):
        """
        DESCRIPTION: Load app and Verify the newly created featured module on the FE
        EXPECTED: The newly created featured module should appear on the FE, if the event is still active and falls with in the given date range.
        """
        pass
