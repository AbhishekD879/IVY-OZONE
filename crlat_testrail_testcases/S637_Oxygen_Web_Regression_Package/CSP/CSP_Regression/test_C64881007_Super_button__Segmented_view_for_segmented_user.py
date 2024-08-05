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
class Test_C64881007_Super_button__Segmented_view_for_segmented_user(Common):
    """
    TR_ID: C64881007
    NAME: Super button - Segmented view for segmented user
    DESCRIPTION: This test case verifies segmented view for segmented user
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button >Create superbutton
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    """
    keep_browser_open = True

    def test_001_launch_the_application_in_mobilewebapp(self):
        """
        DESCRIPTION: Launch the application in mobile(Web/App)
        EXPECTED: Application should launch successfully.
        """
        pass

    def test_002_(self):
        """
        DESCRIPTION: 
        EXPECTED: Home page should be opened.
        """
        pass

    def test_003_login_with_specific_segmented_user__as_per_pre_conditions(self):
        """
        DESCRIPTION: Login with specific segmented user ( as per Pre-conditions)
        EXPECTED: User should login successfully
        """
        pass

    def test_004_verify_segmented_record(self):
        """
        DESCRIPTION: Verify segmented record
        EXPECTED: User should able to see segmented record(The first valid Super button)for specific segmented user as per CMS configuration
        """
        pass
