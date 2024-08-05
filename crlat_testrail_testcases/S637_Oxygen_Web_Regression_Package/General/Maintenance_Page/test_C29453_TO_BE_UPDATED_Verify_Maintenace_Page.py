import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C29453_TO_BE_UPDATED_Verify_Maintenace_Page(Common):
    """
    TR_ID: C29453
    NAME: (TO BE UPDATED) Verify Maintenace Page
    DESCRIPTION: 
    PRECONDITIONS: Either Siteserver should be down in order to observe Maintenace Page.
    PRECONDITIONS: Use https://ladbrokescoral.testrail.com//index.php?/tests/view/182809 test case for configuring Maintenance page.
    PRECONDITIONS: CMS > System configuration > Config > maintenancePage > enabled = 'true'
    PRECONDITIONS: CMS > System configuration > Config > maintenancePage > Target Uri = '/in-play'
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load 'Oxygen' application
        EXPECTED: 
        """
        pass

    def test_002_verify_maintenance_page(self):
        """
        DESCRIPTION: Verify Maintenance Page
        EXPECTED: The Maintenance Page is displayed on Mobile/Tablet/Desktop (depends on settings in CMS)
        """
        pass

    def test_003_in_cms_upload_new_image_for_the_existing_active_maintenance_page(self):
        """
        DESCRIPTION: In CMS, upload new image for the existing active maintenance page
        EXPECTED: Maintenance page settings are updated
        """
        pass

    def test_004_click_on_the_maintenance_page_in_oxygen_app(self):
        """
        DESCRIPTION: Click on the Maintenance Page in 'Oxygen' app
        EXPECTED: User is not redirected to the page that was set in CMS
        EXPECTED: Maintenance page splash screen is updated
        """
        pass

    def test_005_in_cms_set_validity_period_end_date_to_a_datetime_that_will_be_reached_within_5_mins_from_current_datetime(self):
        """
        DESCRIPTION: In CMS, set 'Validity Period End' date to a date/time that will be reached within 5 mins from current date/time
        EXPECTED: Maintenance page settings are updated
        """
        pass

    def test_006_go_back_to_oxygen_app_and_make_sure_that_maintenance_page_is_still_displayedrefresh_the_page(self):
        """
        DESCRIPTION: Go back to 'Oxygen' app and make sure that Maintenance Page is still displayed.
        DESCRIPTION: Refresh the page.
        EXPECTED: * Maintenance Page is still displayed in case if 'Validity Period End' set in CMS is not reached.
        EXPECTED: * Maintenance page disappears and user redirects to the Homepage in case if 'Validity Period End' set in CMS is reached.
        """
        pass
