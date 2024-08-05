import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C1108265_Verify_date_and_time_format_on_Football_Competitions_Results_tab(Common):
    """
    TR_ID: C1108265
    NAME: Verify date and time format on Football > Competitions > Results tab
    DESCRIPTION: This test case verifies date and time format on Football > Competitions > Results tab
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_football__competitions_tab_select_some_competition_and_click_it(self):
        """
        DESCRIPTION: Navigate to Football > Competitions tab, select some competition and click it
        EXPECTED: Competition page opens.
        """
        pass

    def test_003_select_results_tab(self):
        """
        DESCRIPTION: Select Results tab
        EXPECTED: Results page opens. Matches results divided by sections (ordered by date):
        EXPECTED: - Today
        EXPECTED: - Tomorrow
        EXPECTED: - future date, eg: 1 Jan 2018
        EXPECTED: etc
        """
        pass

    def test_004_verify_date_format_on_sections_with_date(self):
        """
        DESCRIPTION: Verify date format on sections with date
        EXPECTED: Date is in format %Day Month Year%
        """
        pass
