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
class Test_C64881008_Super_button__for_Segmented_viewReorder_the_recordsUniversal_record_is_in_first_place_in_CMS_Verify_in_FE(Common):
    """
    TR_ID: C64881008
    NAME: Super button - for Segmented view,Reorder the records(Universal record is in first place)  in CMS ,Verify in FE
    DESCRIPTION: Â This test case verifies for Segmented view records reordering.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button >Create superbutton
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    PRECONDITIONS: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
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

    def test_003_select_any_segment_form_the_segment_dropdown(self):
        """
        DESCRIPTION: Select any segment form the Segment dropdown
        EXPECTED: Exisiting records for specific segment should display along with universal records
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
        """
        pass

    def test_005_reorder_the_records__valid_universal_record_as_first_position(self):
        """
        DESCRIPTION: Reorder the records , valid universal record as first position
        EXPECTED: User should able to reorder the records
        """
        pass

    def test_006_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_007_login_in_fe_with_segment_useras_per_preconditions(self):
        """
        DESCRIPTION: Login in FE with segment user(as per preconditions)
        EXPECTED: User should able to view first valid record as per CMS configuration
        """
        pass
