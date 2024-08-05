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
class Test_C1683778_Verify_Results_Module_data_correctness(Common):
    """
    TR_ID: C1683778
    NAME: Verify Results Module data correctness
    DESCRIPTION: This test case verifies Results Module data correctness
    PRECONDITIONS: 1) Competition should be created, set up and enabled in CMS -> Big Competition section - https://{domain}/big-competition
    PRECONDITIONS: where
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - dev env
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - local env
    PRECONDITIONS: 2) Module with type = 'RESULTS' should be created, enabled and set up in CMS (Results must be present for Competition. Please use e.g. Premier League or UEFA Champion League)
    PRECONDITIONS: 3) To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab by ID request
    PRECONDITIONS: 4) To check list of matches correctness for each Season use the link: https://{domain}/api/season/<seasonID>/matches/
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

    def test_003_go_to_group_results_tab_and_verify_that_results_attribute_is_received(self):
        """
        DESCRIPTION: Go to Group Results tab and verify that results attribute is received
        EXPECTED: Result attribute should be present
        EXPECTED: ![](index.php?/attachments/get/21014)
        """
        pass

    def test_004_verify_dates_correctness_expand_results_attribute(self):
        """
        DESCRIPTION: Verify Dates correctness (expand results attribute)
        EXPECTED: All dates from response are present on UI (on Date header)
        EXPECTED: ![](index.php?/attachments/get/21015)
        """
        pass

    def test_005_verify_date_ordering_on_date_header(self):
        """
        DESCRIPTION: Verify date ordering (on Date header)
        EXPECTED: Events should be ordered by Date (Earliest date first and then so on)
        """
        pass

    def test_006_verify_matches_correctness_expand_date_attribute(self):
        """
        DESCRIPTION: Verify matches correctness (expand date attribute)
        EXPECTED: All dates from response are present on UI
        EXPECTED: ![](index.php?/attachments/get/21016)
        """
        pass

    def test_007_verify_teams_correctness_expand_matches_attribute(self):
        """
        DESCRIPTION: Verify teams correctness (expand matches attribute)
        EXPECTED: Teams from response are present on UI
        EXPECTED: ![](index.php?/attachments/get/21017)
        """
        pass

    def test_008_verify_goalscorers_correctness_expand_teama_and_teamb_attributes(self):
        """
        DESCRIPTION: Verify goalScorers correctness (expand teamA and teamB attributes)
        EXPECTED: Goalscorers from response are present on UI
        EXPECTED: ![](index.php?/attachments/get/21019)
        """
        pass

    def test_009_verify_score_correctness_expand_teama_and_teamb_attributes(self):
        """
        DESCRIPTION: Verify score correctness (expand teamA and teamB attributes)
        EXPECTED: Scorers from response are present on UI
        EXPECTED: ![](index.php?/attachments/get/21052)
        """
        pass
