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
class Test_C60618892_Verify_existing_betradar_services_to_include_OB_event_type_display_order(Common):
    """
    TR_ID: C60618892
    NAME: Verify existing betradar services to include OB event type display order
    DESCRIPTION: Jira tickets:
    DESCRIPTION: SFD-816
    PRECONDITIONS: Currently there are 3 {domains}:
    PRECONDITIONS: *   Current tst environment (domain) - https://spark-br-tst.symphony-solutions.eu
    PRECONDITIONS: *   Current stage environment (domain) - https://spark-br-stg2.symphony-solutions.eu
    PRECONDITIONS: *   Current prod environment (domain) - https://spark-br.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_web_browser(self):
        """
        DESCRIPTION: Load web browser
        EXPECTED: Web browser is opened
        """
        pass

    def test_002_load_servicedomainapiseasonseasonidmatchesbydatequery_params____startdate___start_date___enddate___end_daterequest_with_date_paramshttpsspark_br_tstsymphony_solutionseuapimatchesbydatestartdate2016_08_23enddate2016_10_31(self):
        """
        DESCRIPTION: Load service:
        DESCRIPTION: {domain}/api/season/:seasonId/matches/bydate/,
        DESCRIPTION: Query params :
        DESCRIPTION: *   :startdate - start date
        DESCRIPTION: *   :enddate - end date
        DESCRIPTION: Request with date params:
        DESCRIPTION: https://spark-br-tst.symphony-solutions.eu/api/matches/bydate/?startdate=2016-08-23&enddate=2016-10-31
        EXPECTED: Matches details by season and start date and date are returted
        EXPECTED: Request without date param returns all matches from todays date
        """
        pass

    def test_003_open_mapping_document(self):
        """
        DESCRIPTION: Open mapping document
        EXPECTED: Mapping document is opened
        """
        pass

    def test_004_find_the_competition_which_has_valid_mapping_in_the_document_and_which_match_is_returned_in_the_service_from_the_step_2(self):
        """
        DESCRIPTION: Find the competition which has valid mapping in the document and which match is returned in the service from the step #2
        EXPECTED: Competition is found
        EXPECTED: Bet Radar competition has its mapped OB type id
        """
        pass

    def test_005_open_site_server_query_and_fing_the_type_id(self):
        """
        DESCRIPTION: Open SIte Server query and fing the type id
        EXPECTED: Type is is shown
        """
        pass

    def test_006_find_the_displayorder_for_this_type(self):
        """
        DESCRIPTION: Find the 'displayOrder' for this type
        EXPECTED: 'displayOrder' is shown
        """
        pass

    def test_007_open_teh_service_from_teh_step_2_and_fin_the_relevat_match(self):
        """
        DESCRIPTION: Open teh service from teh step 2 and fin the relevat match
        EXPECTED: Match is shown
        """
        pass

    def test_008_find_the_displayorder_attribute(self):
        """
        DESCRIPTION: Find the 'displayOrder' attribute
        EXPECTED: 'displayOrder0 is shown'
        """
        pass

    def test_009_check_displayorder_value(self):
        """
        DESCRIPTION: Check 'displayOrder' value
        EXPECTED: The display order will be pulled from SiteServer using the mappings between the betradar competitions and the betradar competitions in the existing config file
        """
        pass

    def test_010_in_teh_service_find_teh_competition_which_doesnt_have_mapping_to_the_ob_competition(self):
        """
        DESCRIPTION: In teh service find teh competition which doesn't have mapping to the OB competition
        EXPECTED: Competition is found
        """
        pass

    def test_011_check_displayorder_value_for_it(self):
        """
        DESCRIPTION: Check 'displayOrder' value for it
        EXPECTED: displayOrder= 10000 is set by default
        """
        pass

    def test_012_repeat_steps__3__11_for_competitions_which_are_retyrned_from_teh_querydomainapiseasonseasonidmatchesbydatequery_params____startdate___start_date___enddate___end_date(self):
        """
        DESCRIPTION: Repeat steps # 3 -11 for competitions which are retyrned from teh query:
        DESCRIPTION: {domain}/api/season/:seasonId/matches/bydate/
        DESCRIPTION: Query params :
        DESCRIPTION: *   :startdate - start date
        DESCRIPTION: *   :enddate - end date
        EXPECTED: Matches details by season and start date and date are shown
        """
        pass
