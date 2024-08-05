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
class Test_C62969677_Verify_blank_space_under_the_module_section_If_there_are_no_configurations_for_any_module_for_the_snapshot_requested_date_and_time(Common):
    """
    TR_ID: C62969677
    NAME: Verify blank space under the module section If there are no configurations for any module for the snapshot requested date and time
    DESCRIPTION: This test case verifies blank space when there is no data for selected segment
    PRECONDITIONS: 1) User should have admin access to BI reports
    PRECONDITIONS: 2) CMS config should be done for all modules
    PRECONDITIONS: 3) Segments should be created in Optimove and respective config should added to CMS modules
    """
    keep_browser_open = True

    def test_001_login_to_bi_reports_with_admin_access_andnavigate_to_retro_reports_tbd(self):
        """
        DESCRIPTION: Login to BI reports with admin access and navigate to retro Reports (TBD)
        EXPECTED: Retro Reports page should display
        """
        pass

    def test_002_select_all_mandatory_fields_and_click_on_generate_retro_report_button(self):
        """
        DESCRIPTION: Select all mandatory fields and click on generate retro report button
        EXPECTED: Retro report should generate with data for selected fields
        """
        pass

    def test_003_select_a_date_and_time_where_there_is_no_segments_for_all_modules_and_click_on_generate_report_button(self):
        """
        DESCRIPTION: Select a date and time where there is no segments for all modules and click on generate report button
        EXPECTED: blank space should display under the module section
        """
        pass
