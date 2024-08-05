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
class Test_C62969680_Verify_table_columns_of_super_button_module_in_report(Common):
    """
    TR_ID: C62969680
    NAME: Verify table columns of super button module in report
    DESCRIPTION: This test case verifies table columns of super button module in report
    PRECONDITIONS: 1) User should have admin access to BI reports
    PRECONDITIONS: 2) CMS config should be done for super button module
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

    def test_003_verify_table_columns_of_super_button_module_in_report(self):
        """
        DESCRIPTION: Verify table columns of super button module in report
        EXPECTED: Si.No, Title,segment(s), Short Description, Destination URL, Validity Period Start, Validity Period End, Enabled, version creation date Columns should be displayed.
        """
        pass

    def test_004_select_date_and_time_where_segment_has_entries_for_super_button_and_click_on_generate_report_button(self):
        """
        DESCRIPTION: Select date and time where segment has entries for super button and click on generate report button
        EXPECTED: Retro report should display relevent super button data under each coloumn
        """
        pass
