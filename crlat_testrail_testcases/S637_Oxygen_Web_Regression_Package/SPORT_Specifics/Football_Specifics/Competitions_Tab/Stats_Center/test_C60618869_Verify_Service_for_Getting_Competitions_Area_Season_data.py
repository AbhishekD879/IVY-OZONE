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
class Test_C60618869_Verify_Service_for_Getting_Competitions_Area_Season_data(Common):
    """
    TR_ID: C60618869
    NAME: Verify Service for Getting Competitions/Area/Season data
    DESCRIPTION: Thsi test case verifies service for getting data about different areas, sports, competitions, etc.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: SFD-528
    PRECONDITIONS: Note, this test case verifies functionality when XMLs are sent manually
    PRECONDITIONS: Currently there are 3 {domains}:
    PRECONDITIONS: *   Current tst environment (domain) - https://spark-br-tst.symphony-solutions.eu
    PRECONDITIONS: *   Current stage environment (domain) - https://spark-br-stg2.symphony-solutions.eu
    PRECONDITIONS: *   Current prod environment (domain) - https://spark-br.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_web_browser(self):
        """
        DESCRIPTION: Load web browser
        EXPECTED: Web browser page is loaded
        """
        pass

    def test_002_check_the_following_api_calldomainapitournaments(self):
        """
        DESCRIPTION: Check the following API call:
        DESCRIPTION: {domain}/api/tournaments
        EXPECTED: The endpoint returns a list of all competitions
        """
        pass

    def test_003_enter_the_following_addressdomainapisports(self):
        """
        DESCRIPTION: Enter the following address:
        DESCRIPTION: {domain}/api/sports
        EXPECTED: The endpoint returns all sports which are currently supported by Sport Radar
        """
        pass

    def test_004_check_the_endpointdomainapiareassportid___param_sportid___id_of_sport_which_is_taken_from_the_step_2(self):
        """
        DESCRIPTION: Check the endpoint:
        DESCRIPTION: {domain}/api/areas/:sportId,
        DESCRIPTION: *   param :**sportId** - id of sport which is taken from the step #2
        EXPECTED: The endpoint returns areas (countries) which currently available on Sport Radar for particular sport
        """
        pass

    def test_005_check_the_following_end_point_in_the_web_browserdomainapicompetitionssportidareaid___param_sportid___id_of_sport_taken_from_step_3___param_areaid___id_of_area_which_is_taken_from_step_4(self):
        """
        DESCRIPTION: Check the following end point in the web browser:
        DESCRIPTION: {domain}/api/competitions/:sportId/:areaId
        DESCRIPTION: *   param :**sportId** - id of sport taken from step #3
        DESCRIPTION: *   param :**areaId** - id of area which is taken from step #4
        EXPECTED: The endpoint returns list of competitions for particulat sport and area (if competition is a league)
        """
        pass

    def test_006_check_the_following_endpoint_in_web_browserdomainapiseasonssportidareaidcompetitionid___param_sportid___id_of_sport_returned_is_step_3___param_areaid___id_of_area_returned_in_step_4___param_competitionid___id_of_competition_returned_in_step_5(self):
        """
        DESCRIPTION: Check the following endpoint in web browser:
        DESCRIPTION: {domain}/api/seasons/:sportId/:areaId/:competitionId,
        DESCRIPTION: *   param:** sportId **- id of sport returned is step #3
        DESCRIPTION: *   param: **areaId **- id of area, returned in step #4
        DESCRIPTION: *   param:** competitionId** - id of competition, returned in step #5
        EXPECTED: The endpoint returns list of seasons available for particular competition from the selected sport and area
        """
        pass

    def test_007_check_the_folloiwng_endpoint_in_web_browserdomainapiseasonseasonidupcomingmatches___param_seasonid__the_id_of_season_received_in_step_6(self):
        """
        DESCRIPTION: Check the folloiwng endpoint in web browser:
        DESCRIPTION: {domain}/api/season/:seasonId/upcomingmatches
        DESCRIPTION: *   param : **seasonId - **the id of season received in step #6
        EXPECTED: The endpoint returns season upcoming matches
        """
        pass

    def test_008_check_the_following_endpoint_in_web_browserdomainapiseasonseasonidtopplayersparam_seasonid___id_of_season_which_is_taken_from_the_step_6(self):
        """
        DESCRIPTION: Check the following endpoint in web browser:
        DESCRIPTION: {domain}/api/season/:seasonId/topplayers
        DESCRIPTION: param :seasonId - id of season which is taken from the step #6
        EXPECTED: A list of top player from the selected season is shown
        """
        pass

    def test_009_check_the_following_endpoint_in_web_browserdomainapiareaareaidupcomingmatches___param_areaid___the_id_of_area_country_received_in_step_4(self):
        """
        DESCRIPTION: Check the following endpoint in web browser:
        DESCRIPTION: {domain}/api/area/:areaid/upcomingmatches
        DESCRIPTION: *   param: **areaId **- the id of area (country) received in step #4
        EXPECTED: The endpoit returns area upcoming matches
        """
        pass
