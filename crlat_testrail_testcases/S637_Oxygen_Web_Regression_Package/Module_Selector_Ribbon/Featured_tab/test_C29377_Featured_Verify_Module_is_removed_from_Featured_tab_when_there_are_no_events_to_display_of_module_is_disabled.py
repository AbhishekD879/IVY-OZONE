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
class Test_C29377_Featured_Verify_Module_is_removed_from_Featured_tab_when_there_are_no_events_to_display_of_module_is_disabled(Common):
    """
    TR_ID: C29377
    NAME: Featured: Verify Module is removed from Featured tab when there are no events to display of module is disabled
    DESCRIPTION: This test case verifies that Module is not present if there are no available events to display or if 'Enabled' field in CMS is unchecked.
    DESCRIPTION: To be run on mobile, tablet and desktop
    PRECONDITIONS: 1) 2 Featured Modules with at least 2 events in each created in CMS. Modules are Active and are displayed on Featured tab in app.
    PRECONDITIONS: 2) CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_uncheck_enabled_for_the_first_module__gt_click_save_button(self):
        """
        DESCRIPTION: Go to CMS and uncheck 'Enabled' for the first Module -&gt; click 'Save' button
        EXPECTED: 
        """
        pass

    def test_002_verify_module_area_in_app(self):
        """
        DESCRIPTION: Verify Module Area in app
        EXPECTED: Module is removed from Featured tab
        """
        pass

    def test_003_go_to_cms_and_click_remove_all_in_events_in_module_section_for_second_module__gt_click_save_button(self):
        """
        DESCRIPTION: Go to CMS and click 'Remove all in 'Events in Module section' for second Module -&gt; click 'Save' button
        EXPECTED: 
        """
        pass

    def test_004_verify_module_area_in_app(self):
        """
        DESCRIPTION: Verify Module Area in app
        EXPECTED: Module is removed from Featured tab
        """
        pass
