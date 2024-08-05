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
class Test_C62969675_Verify_user_is_able_to_fetch_data_between_past_6_months_to_todayVerify_version_creation_date(Common):
    """
    TR_ID: C62969675
    NAME: Verify user is able to fetch data between past 6 months to today(Verify version creation date)
    DESCRIPTION: This test case verifies retro report can give data not more than last 6 months
    DESCRIPTION: This testcases also verifies report date and time should not be more than version create date
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

    def test_002_select_date_and_time_for_more_than_last_6_months(self):
        """
        DESCRIPTION: Select date and time for more than last 6 months
        EXPECTED: Valid error message should display (TBD) or date picker should not allow to select date not more than last 6 months
        """
        pass

    def test_003_select_date_and_time_exactly_last_6_monthscheck_date_and_time_for_last_6_months(self):
        """
        DESCRIPTION: Select date and time exactly last 6 months(check date and time for last 6 months)
        EXPECTED: Selected date and time should visible in report from date and time fields
        """
        pass

    def test_004_select_date_and_time_within_last_6_monthscheck_date_and_time_for_last_6_months(self):
        """
        DESCRIPTION: Select date and time within last 6 months(check date and time for last 6 months)
        EXPECTED: Selected date and time should visible in report from date and time fields
        """
        pass

    def test_005_verify_selecting_date_and_time__more_than_6_months(self):
        """
        DESCRIPTION: Verify selecting date and time  more than 6 months
        EXPECTED: User should not allowed to select more than last 6 month
        """
        pass

    def test_006_verify_version_creation_date_in_report(self):
        """
        DESCRIPTION: Verify version creation date in report
        EXPECTED: Data displayed in all modules should match with selected date
        EXPECTED: Version creation date for all module should be less than selected date in report date
        """
        pass
