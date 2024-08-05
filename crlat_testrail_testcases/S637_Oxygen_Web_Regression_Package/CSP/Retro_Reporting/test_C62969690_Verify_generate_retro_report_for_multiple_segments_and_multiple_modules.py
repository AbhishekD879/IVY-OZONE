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
class Test_C62969690_Verify_generate_retro_report_for_multiple_segments_and_multiple_modules(Common):
    """
    TR_ID: C62969690
    NAME: Verify generate retro report for multiple segments and multiple modules
    DESCRIPTION: This test case verifies generate retro report for multiple segments and multiple modules
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

    def test_002_select_multiple_segments_from_selected_segments_and_multiple_modules_from_selected_modules_drop_down_and_verify_and_click_on_generate_retro_report_button(self):
        """
        DESCRIPTION: Select multiple segments from Selected Segment(s) and multiple modules from Selected Module(s) drop down and verify and click on Generate Retro Report button
        EXPECTED: Retro report should be generate with data for multiple segments and multiple modules.
        """
        pass

    def test_003_click_on_download_report_button(self):
        """
        DESCRIPTION: Click on "Download Report" button
        EXPECTED: "Download Report" button should be clickable.Should allow to download data
        """
        pass

    def test_004_verify_the_content_in_report(self):
        """
        DESCRIPTION: Verify the content in Report
        EXPECTED: Retro report should display relevent data
        """
        pass

    def test_005_repeat_above_steps_for_multiple_segments_with_other_multiple_modules(self):
        """
        DESCRIPTION: Repeat above steps for multiple segments with other multiple modules
        EXPECTED: Report should be display accordingly
        """
        pass
