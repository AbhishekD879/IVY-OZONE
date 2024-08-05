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
class Test_C62969678_Verify_If_a_segment_has_entries_for_some_modules_but_not_all(Common):
    """
    TR_ID: C62969678
    NAME: Verify If a segment has entries for some modules but not all
    DESCRIPTION: This test case verifies If a segment has entries for some modules but not all
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

    def test_003_select_date_and_time_where_segment_has_entries_for_some_modules_but_not_all_and_click_on_generate_report_button(self):
        """
        DESCRIPTION: Select date and time where segment has entries for some modules but not all and click on generate report button
        EXPECTED: Retro report should display whatever module has the data and remaining modules should shown blank space.
        """
        pass
