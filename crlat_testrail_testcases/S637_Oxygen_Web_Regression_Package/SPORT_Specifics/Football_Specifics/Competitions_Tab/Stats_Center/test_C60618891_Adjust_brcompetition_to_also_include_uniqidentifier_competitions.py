import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C60618891_Adjust_brcompetition_to_also_include_uniqidentifier_competitions(Common):
    """
    TR_ID: C60618891
    NAME: Adjust brcompetition to also include uniqidentifier competitions
    DESCRIPTION: This test case verified adjusting brcompetitions to include uniqidentifier competitions
    DESCRIPTION: **Jirs tickets:**
    DESCRIPTION: SFD-815
    PRECONDITIONS: Make sure that area contains several competitions with the same uniqidentifier
    PRECONDITIONS: Currently there are 3 {domains}:
    PRECONDITIONS: *   Current tst environment (domain) - https://spark-br-tst.symphony-solutions.eu
    PRECONDITIONS: *   Current stage environment (domain) - https://spark-br-stg2.symphony-solutions.eu
    PRECONDITIONS: *   Current prod environment (domain) - https://spark-br.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_web_browser(self):
        """
        DESCRIPTION: Load web browser
        EXPECTED: Web browser is loaded
        """
        pass

    def test_002_in_the_list_of_requests_find_the_requestdomainapibrcompetitionseasonobsportidobclassidobtypeidwhere___param_obsportid___open_bet_sport_id___param_obclassid___open_bet_class_id___param_obtypeid___open_bet_type_id(self):
        """
        DESCRIPTION: In the list of requests find the request:
        DESCRIPTION: {domain}/api/brcompetitionseason/:obSportId/:obClassId/:obTypeId,
        DESCRIPTION: where:
        DESCRIPTION: *   param :obSportId - open bet sport id
        DESCRIPTION: *   param :obClassId - open bet class id
        DESCRIPTION: *   param :obTypeId - open bet type id
        EXPECTED: Competitions and season for some OB event
        """
        pass

    def test_003_in_services_check_competitions_with_the_same_uniqidentifier(self):
        """
        DESCRIPTION: In services check competitions with the same uniqidentifier
        EXPECTED: All compatitions are dispaleyd
        """
        pass

    def test_004_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: App is opened
        """
        pass

    def test_005_go_to_the_football_sport___competition_tab(self):
        """
        DESCRIPTION: Go to the Football  sport -> Competition tab
        EXPECTED: Tab is opened
        """
        pass

    def test_006_open_dev_console___network_tab(self):
        """
        DESCRIPTION: Open dev console -> Network tab
        EXPECTED: Tab is opened
        """
        pass

    def test_007_find_the_competitions_from_the_step_5(self):
        """
        DESCRIPTION: Find the competitions from the step #5
        EXPECTED: Competitions are shown
        """
        pass

    def test_008_check_the_changes_on_the_front_end(self):
        """
        DESCRIPTION: Check the changes on the front end
        EXPECTED: All competitions are displayed correctly
        """
        pass

    def test_009_check_the_service_with_the_several_cometitionseg_england_championship_uefa_champions_league(self):
        """
        DESCRIPTION: Check the service with the several cometitions:
        DESCRIPTION: e.g. England Championship, UEFA Champions League
        EXPECTED: All competitions are displayed correctly
        """
        pass
