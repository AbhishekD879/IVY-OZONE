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
class Test_C62969693_Verify_the_format_of_the_report_should_be_excel(Common):
    """
    TR_ID: C62969693
    NAME: Verify the format of the report -should be excel
    DESCRIPTION: This test case verifies the format of the report should be excel
    PRECONDITIONS: 1) User should have admin access to BI reports
    PRECONDITIONS: 2) CMS config should be done for all modules
    PRECONDITIONS: 3) Segments should be created in Optimove and respective config should added to CMS modules
    """
    keep_browser_open = True

    def test_001_login_to_bi_reports_with_admin_accessnavigate_to_retro_reports_tbd(self):
        """
        DESCRIPTION: Login to BI reports with admin access
        DESCRIPTION: navigate to retro Reports (TBD)
        EXPECTED: Retro Reports page should display
        """
        pass

    def test_002_select_all_mandatory_fields_and_click_on_generate_retro_report_button(self):
        """
        DESCRIPTION: Select all mandatory fields and click on generate retro report button
        EXPECTED: Retro report should generate with data for selected fields
        """
        pass

    def test_003_click_on_download_report_button(self):
        """
        DESCRIPTION: Click on "Download Report" button
        EXPECTED: "Download Report" button should be clickable.Should allow to download data
        """
        pass

    def test_004_verify_format_of_the_report(self):
        """
        DESCRIPTION: Verify format of the report
        EXPECTED: Dowloaded report should be in Excel format
        """
        pass

    def test_005_verify_the_content_in_report(self):
        """
        DESCRIPTION: Verify the content in Report
        EXPECTED: Retro report should display relevent data
        """
        pass
