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
class Test_C62969685_Verify_to_generate_retro_report_for_all_segments_and_all_modules(Common):
    """
    TR_ID: C62969685
    NAME: Verify to generate retro report for all segments and all modules
    DESCRIPTION: This test case verifies generate retro report for all segments and all modules
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

    def test_003_select_all_segments_from_selected_segments_and_all_modules_from_selected_modules_drop_down_and_verify_and_click_on_generate_retro_report_button(self):
        """
        DESCRIPTION: Select all segments from Selected Segment(s) and all modules from Selected Module(s) drop down and verify and click on Generate Retro Report button
        EXPECTED: Retro report should be generate with data for all segments and all modules.
        """
        pass
