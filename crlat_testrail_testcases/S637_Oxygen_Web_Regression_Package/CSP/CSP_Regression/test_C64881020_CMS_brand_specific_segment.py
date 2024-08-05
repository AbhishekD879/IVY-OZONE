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
class Test_C64881020_CMS_brand_specific_segment(Common):
    """
    TR_ID: C64881020
    NAME: CMS brand specific segment
    DESCRIPTION: This test case verifies specific segment for Brand in CMS
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2.User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>CMS > sports pages > super button.( all modules )
    PRECONDITIONS: a)Create a record with CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL  in One brand(ex:lads)
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_create_a_record_in_superbutton_for_segment_from_precondition_in_lads(self):
        """
        DESCRIPTION: Create a record in superbutton for segment from precondition in lads
        EXPECTED: User should able to create superbutton successfully ,and Segment name should reflect in all other modules in lads
        """
        pass

    def test_004_navigate_to_coral_from_header_menu_in_cms_search_for_segment_which_is_created_in_lads(self):
        """
        DESCRIPTION: Navigate to Coral from header menu in CMS ,Search for Segment which is created in lads
        EXPECTED: Segment name should not display in Coral ,as this is brand specific
        """
        pass
