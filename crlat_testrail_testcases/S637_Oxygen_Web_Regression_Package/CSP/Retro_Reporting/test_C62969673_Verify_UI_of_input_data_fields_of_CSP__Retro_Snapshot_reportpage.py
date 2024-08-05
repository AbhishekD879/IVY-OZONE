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
class Test_C62969673_Verify_UI_of_input_data_fields_of_CSP__Retro_Snapshot_reportpage(Common):
    """
    TR_ID: C62969673
    NAME: Verify UI of input data fields of CSP - Retro Snapshot report*page
    DESCRIPTION: This test case verifies UI of input fields of CSP - Retro Snapshot report* page
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

    def test_002_verify_retro_reports_ui(self):
        """
        DESCRIPTION: Verify retro reports UI
        EXPECTED: Retro report should have following input fields
        EXPECTED: Title: CSP - Retro Snapshot report*
        EXPECTED: Report from date : Date picker (DD/MM/YYYY)
        EXPECTED: Report from time : HH:MM:SS (24 hrs format)
        EXPECTED: Selected Segment(s): (Multi-selection allowed) dropdown
        EXPECTED: Selected Module(s): (Multi-selection allowed) dropdown
        EXPECTED: CTA : Generate retro report
        """
        pass

    def test_003_select_date_and_time_within_last_6_monthscheck_date_and_time_for_last_6_months(self):
        """
        DESCRIPTION: Select date and time within last 6 months(check date and time for last 6 months)
        EXPECTED: Selected date and time should visible in report from date and time fields
        """
        pass

    def test_004_select_single_or_multiple_segments_from_drop_down_and_verify(self):
        """
        DESCRIPTION: Select single or multiple segments from drop down and verify
        EXPECTED: Selected segments should display in Selected Segment(s) field(TBD)
        EXPECTED: if we click on segment drop down selected segments should display as checked
        """
        pass

    def test_005_select_all_segments_from_drop_down_and_verify(self):
        """
        DESCRIPTION: Select all segments from drop down and verify
        EXPECTED: All segments should display in Selected Segment(s) field (TBD)
        EXPECTED: if we click on segment drop down all segments should display as checked
        """
        pass

    def test_006_select_single_or_multiple_modules_from_drop_down_and_verify(self):
        """
        DESCRIPTION: Select single or multiple modules from drop down and verify
        EXPECTED: Selected modules should display in Selected Module(s) field(TBD)
        EXPECTED: if we click on module drop down selected modules should display as checked
        """
        pass

    def test_007_select_all_modules_from_drop_down_and_verify(self):
        """
        DESCRIPTION: Select all modules from drop down and verify
        EXPECTED: All modules should display in Selected Module(s) field(TBD)
        EXPECTED: if we click on module drop down selected modules should display as checked
        """
        pass

    def test_008_verify_generate_retro_report_button_is_enabled_when_only_selecting_all_mandatory_fields(self):
        """
        DESCRIPTION: Verify generate retro report button is enabled when only selecting all mandatory fields
        EXPECTED: If we unselect any mandatory fields, generate retro button should be disabled
        """
        pass
