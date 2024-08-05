import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C120302_Verify_Maintenance_page_displaying_on_front_end_according_to_CMS_configuration(Common):
    """
    TR_ID: C120302
    NAME: Verify Maintenance page displaying on front-end according to CMS configuration
    DESCRIPTION: This test case verifies displaying of Maintenance page configured via CMS on front-end.
    PRECONDITIONS: Create Maintenance page in the CMS.
    PRECONDITIONS: CMS > System configuration > Config > maintenancePage > enabled = true
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_verify_maintenance_page(self):
        """
        DESCRIPTION: Verify Maintenance page
        EXPECTED: Maintenance page consists of next elements:
        EXPECTED: * Basic blue background behind the Splash Banner
        EXPECTED: * Maintenance Splash Banner:
        EXPECTED: - Coral logo
        EXPECTED: - Inscription about time when application will be available
        EXPECTED: - 'Bet Now' button
        """
        pass

    def test_003_verify_redirection_functionality_after_clicking_on_maintenance_splash_banner(self):
        """
        DESCRIPTION: Verify redirection functionality after clicking on Maintenance Splash Banner
        EXPECTED: * If Validity period is NOT finished, user is redirected to configured maintenance URL
        EXPECTED: * If Validity period is finished then User is redirected to the relevant landing pages
        """
        pass

    def test_004_verify_case_if_maintenance_page_schedule_has_ended(self):
        """
        DESCRIPTION: Verify case if Maintenance page schedule has ended
        EXPECTED: *  Application is refreshed automatically and Maintenance page disappears
        EXPECTED: * User is redirected to the relevant page
        """
        pass
