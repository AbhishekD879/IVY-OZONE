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
class Test_C1952688_Verify_Build_Your_Bet_configurations_on_Module_Ribbon_Tabs_and_Desktop_Widgets(Common):
    """
    TR_ID: C1952688
    NAME: Verify Build Your Bet configurations on Module Ribbon Tabs and Desktop Widgets
    DESCRIPTION: This test case verifies configuration of Build Your Bet Option on Module Ribbon Tab.
    PRECONDITIONS: 1)'Build Your Bet' is available in 'Module Ribbon Tabs' tab in CMS
    PRECONDITIONS: 2)'Build Your Bet' is available in 'Widgets' tab in CMS
    PRECONDITIONS: Widgets API:
    PRECONDITIONS: https://coral-cms-api-dev1.symphony-solutions.eu/cms/api/module-ribbon-tabs
    PRECONDITIONS: Module ribbon tabs API:
    PRECONDITIONS: https://coral-cms-api-dev1.symphony-solutions.eu/cms/api/bma/widgets
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened.
        """
        pass

    def test_002_check_module_ribbon_tabs(self):
        """
        DESCRIPTION: Check Module Ribbon Tabs
        EXPECTED: Build Your Bet option should be present on Module Ribbon Tab.
        """
        pass

    def test_003_verify_order_of_tabs_on_module_ribbon_tabs(self):
        """
        DESCRIPTION: Verify order of tabs on Module Ribbon Tabs
        EXPECTED: Order of tabs corresponds to the order in CMS ('Module Ribbon Tabs' tab)
        """
        pass

    def test_004_verify_order_of_tabs_when_changing_and_adding_new_items_on_module_ribbon_tabs_in_cms(self):
        """
        DESCRIPTION: Verify order of tabs when changing and adding new items on Module Ribbon Tabs in CMS
        EXPECTED: Order of tabs on app corresponds to the order in CMS ('Module Ribbon Tabs' tab)
        """
        pass

    def test_005_verify_correctness_settings_through_api_from_preconditions(self):
        """
        DESCRIPTION: Verify correctness settings through API from preconditions
        EXPECTED: Settings in CMS is the same as it is returned from Widgets/Module ribbon tabs APIs
        """
        pass
