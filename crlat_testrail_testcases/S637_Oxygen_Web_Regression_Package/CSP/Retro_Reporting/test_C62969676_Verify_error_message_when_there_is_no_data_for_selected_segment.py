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
class Test_C62969676_Verify_error_message_when_there_is_no_data_for_selected_segment(Common):
    """
    TR_ID: C62969676
    NAME: Verify error message when there is no data for selected segment
    DESCRIPTION: This test case verifies error message when there is no data for selected segment
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

    def test_003_select_a_date_where_there_is_no_segments_for_all_modules_and_click_on_generate_report_button(self):
        """
        DESCRIPTION: Select a date where there is no segments for all modules and click on generate report button
        EXPECTED: Error message "There are no entries for this segment' should display
        """
        pass

    def test_004_select_a_segment_for_which_there_are_no_entriesitem_in_module_eg_no_surfacebets_and_hit_generate_retro_report_button(self):
        """
        DESCRIPTION: Select a segment for which there are no entries(item in module, eg no surfacebets) and hit generate retro report button
        EXPECTED: Error message "There are no entries for this segment' should display
        """
        pass

    def test_005_disable_any_all_valid_entries_of_segment_in_all_modules_in_cms_and_select__the_same_segment_from_drop_down_and_click_on_generate_retro_report_button(self):
        """
        DESCRIPTION: Disable any all valid entries of segment in all modules in CMS and select  the same segment from drop down and click on generate retro report button
        EXPECTED: Error message "There are no entries for this segment' should display
        """
        pass

    def test_006_select_a_module_for_which_there_are_no_entries_and_click_on_generate_retro_report_button(self):
        """
        DESCRIPTION: Select a module for which there are no entries and click on generate retro report button
        EXPECTED: Error message "There are no entries for this segment' should display
        """
        pass

    def test_007_select_report_date_and_time_just_for_1_sec_and_verify_report(self):
        """
        DESCRIPTION: Select report date and time just for 1 sec and verify report
        EXPECTED: Error message "There are no entries for this segment' should display. If there is no entries for select date
        """
        pass
