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
class Test_C62969691_Verify_Each_report_should_contain_selected_segment_in_the_segment_text_box_and_Requested_time_stamp(Common):
    """
    TR_ID: C62969691
    NAME: Verify Each report should contain selected segment in the segment text box and ‘Requested time stamp’.
    DESCRIPTION: This test case verifies Each report should contain selected segment in the segment text box and ‘Requested time stamp’
    PRECONDITIONS: 1) User should have admin access to BI reports
    PRECONDITIONS: 2) CMS config should be done for all modules
    PRECONDITIONS: 3) Segments should be created in Optimove and respective config should added to CMS modules
    """
    keep_browser_open = True

    def test_001_login_to_bi_reports_with_admin_access_and_navigate_to_retro_reports_tbd(self):
        """
        DESCRIPTION: Login to BI reports with admin access and navigate to retro Reports (TBD)
        EXPECTED: Retro Reports page should display
        """
        pass

    def test_002_select_all_mandatory_fields_and_click_on_generate_retro_report_button(self):
        """
        DESCRIPTION: Select all mandatory fields and click on generate retro report button
        EXPECTED: Retro report should generate with data for selected fields
        """
        pass

    def test_003_verify_after_retro_report_generated(self):
        """
        DESCRIPTION: Verify after retro report generated
        EXPECTED: Selected segment should be display in the segment text box and requested time stamp should be shown
        """
        pass

    def test_004_verify_data_according_to_the_requested_time_stamp(self):
        """
        DESCRIPTION: Verify data according to the requested time stamp
        EXPECTED: Retro report should display relevent data under each module
        """
        pass
