import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726402_Event_hub_Verify_displaying_of_Quick_Links_with_enabled_disabled_Feature_toggle_in_CMS(Common):
    """
    TR_ID: C9726402
    NAME: Event hub: Verify displaying of Quick Links with enabled/disabled Feature toggle in CMS
    DESCRIPTION: This test case verifies displaying of Quick Links depending on Feature toggle enabled/disabled  in CMS
    PRECONDITIONS: 1. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 2. There is at least 1 Quick Link for Event hub in CMS and it is active.
    PRECONDITIONS: 4. Sports Quick Links system config created in CMS > System Configuration.
    """
    keep_browser_open = True

    def test_001_navigate_to_cms__system_configuration__config_and_enable_sports_quick_links(self):
        """
        DESCRIPTION: Navigate to CMS > System Configuration > Config and enable Sports Quick Links
        EXPECTED: 
        """
        pass

    def test_002_verify_quick_links_module_in_app_on_event_hub(self):
        """
        DESCRIPTION: Verify Quick Links module in app on Event Hub
        EXPECTED: All active Quick Links displayed on FE
        """
        pass

    def test_003_navigate_to_sport_landing_page_from_preconditions_and_verify_quick_links_module_displaying(self):
        """
        DESCRIPTION: Navigate to Sport Landing page from preconditions and verify Quick Links module displaying
        EXPECTED: All active Quick Links displayed on FE
        """
        pass

    def test_004_back_in_cms___system_configuration__config_disable_sports_quick_links(self):
        """
        DESCRIPTION: Back in CMS  > System Configuration > Config disable Sports Quick Links
        EXPECTED: 
        """
        pass

    def test_005_verify_quick_links_module_in_app_on_event_hub(self):
        """
        DESCRIPTION: Verify Quick Links module in app on Event Hub
        EXPECTED: Quick Links module is not displayed on FE
        """
        pass

    def test_006_navigate_to_sport_landing_page_from_preconditions_and_verify_quick_links_module_displaying(self):
        """
        DESCRIPTION: Navigate to Sport Landing page from preconditions and verify Quick Links module displaying
        EXPECTED: Quick Links module is not displayed on FE
        """
        pass
