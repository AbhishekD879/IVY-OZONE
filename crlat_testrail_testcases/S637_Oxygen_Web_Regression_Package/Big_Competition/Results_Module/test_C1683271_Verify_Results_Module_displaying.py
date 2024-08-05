import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1683271_Verify_Results_Module_displaying(Common):
    """
    TR_ID: C1683271
    NAME: Verify Results Module displaying
    DESCRIPTION: This test case verifies Results Module displaying
    PRECONDITIONS: 1) Competition should be created, set up and enabled in CMS -> Big Competition section - https://{domain}/big-competition
    PRECONDITIONS: where
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - dev env
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - local env
    PRECONDITIONS: 2) Module with type = 'RESULTS' should be created, enabled and set up in CMS (Results must be present for Competition. Please use e.g. Premier League or UEFA Champion League)
    PRECONDITIONS: 3) To check list of matches correctness for each Season use the link: https://{domain}/api/season/<seasonID>/matches/
    PRECONDITIONS: where
    PRECONDITIONS: domain spark-br.symphony-solutions.eu - PROD
    PRECONDITIONS: spark-br-tst.symphony-solutions.eu - TST2
    PRECONDITIONS: spark-br-stg2.symphony-solutions.eu - Stage
    PRECONDITIONS: seasonId - Stats Center Season ID
    """
    keep_browser_open = True

    def test_001_load_oxygen_page(self):
        """
        DESCRIPTION: Load Oxygen page
        EXPECTED: Oxygen page is loaded
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: Competition page is opened
        EXPECTED: Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_group_results_tab(self):
        """
        DESCRIPTION: Go to Group Results tab
        EXPECTED: Results tab/module is present
        """
        pass

    def test_004_verify_results_page(self):
        """
        DESCRIPTION: Verify Results page
        EXPECTED: Resulted Events should be shown in Date Order ( Earliest date first and then so on)
        EXPECTED: Date is present on accordions on Date header. Date format:
        EXPECTED: ![](index.php?/attachments/get/21013)
        EXPECTED: All Date accordions should be expanded by default
        EXPECTED: Number of events should be shown due to CMS configuration (7 by default)
        EXPECTED: 'Show more' button is present (if more then 7 (by default) are present)
        """
        pass

    def test_005_verify_results_page_sorting_correctness_case_when_there_are_more_than_1_event_per_day(self):
        """
        DESCRIPTION: Verify Results page sorting correctness (case when there are more than 1 event per day)
        EXPECTED: - Sorting should be by time (hh.mm.ss) - earliest first and then so on
        EXPECTED: - If time is similar then alphabetically (by TeamA -> name field).
        """
        pass

    def test_006_press_show_more_button(self):
        """
        DESCRIPTION: Press 'Show more' button
        EXPECTED: Next events should be shown (due to CMS configuration, 7 by default)
        """
        pass

    def test_007_go_to_cms___big_competition___results_tab___results_module_and_change_max_display_value_eg_10_save_changes(self):
        """
        DESCRIPTION: Go to CMS -> Big Competition -> Results tab -> Results Module and change Max Display value (e.g. 10), save changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_008_go_to_oxygen_app_and_navigate_to_competition___results_tab(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Competition -> Results tab
        EXPECTED: Number of events should be shown due to CMS configuration (e.g. 10)
        """
        pass

    def test_009_press_show_more_button(self):
        """
        DESCRIPTION: Press 'Show more' button
        EXPECTED: Next events should be shown (due to CMS configuration)
        """
        pass

    def test_010_go_to_cms___big_competition___results_tab___results_module_and_select_available_season_that_doesnt_have_results_events_eg_premier_league_1617_save_changes(self):
        """
        DESCRIPTION: Go to CMS -> Big Competition -> Results tab -> Results Module and select Available Season that doesn't have results events (e.g. Premier League 16/17), save changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_011_go_to_oxygen_app_and_navigate_to_competition___results_tab(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Competition -> Results tab
        EXPECTED: 'No events found' message should be shown
        """
        pass
