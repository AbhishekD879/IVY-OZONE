import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound


# @pytest.mark.tst2 # Racing Post Info is not available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.racing
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.event_details
@vtest
class Test_C64749888_Verify_Greyhounds_EDP_page_Overview(BaseGreyhound):
    """
    TR_ID: C64749888
    NAME: Verify Greyhounds EDP page Overview
    DESCRIPTION: This test case verifies the CMS configurations for surface bet.
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Oxygen applicationC1317076
        EXPECTED: Homepage is loaded
        """
        racing_datahub_status = self.get_initial_data_system_configuration().get('RacingDataHub')[
            "isEnabledForGreyhound"]
        if not racing_datahub_status:
            self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                                  field_name='isEnabledForGreyhound',
                                                                  field_value=True)
        self.__class__.event = self.get_event_details(racing_post_pick=True)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen applicationC1317076
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('Homepage', timeout=10)

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing', timeout=20)

    def test_003_select_event_with_racingpost_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with RacingPost available and go to its details page
        EXPECTED: Event details page is opened
        EXPECTED: ** Mobile** and **Desktop**
        """
        self.navigate_to_edp(event_id=self.event.event_id, sport_name='greyhound-racing', timeout=10)
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

    def test_004_verify_event_details_page_overview(self):
        """
        DESCRIPTION: Verify event details page overview
        EXPECTED: overview consists of:
        EXPECTED: *  time of the race
        EXPECTED: *  event name
        EXPECTED: *  distance of the race
        EXPECTED: *  race grade
        EXPECTED: *  racingPost logo
        EXPECTED: *  markets
        """
        race_distance = self.site.greyhound_event_details.tab_content.race_details.has_race_distance()
        self.assertTrue(race_distance, msg='Distance not found')
        race_grade = self.site.greyhound_event_details.tab_content.has_grade
        self.assertTrue(race_grade, msg="Race grade is not appeared")
        racing_post_logo = self.site.greyhound_event_details.tab_content.post_info
        self.assertTrue(racing_post_logo, msg='Racing Post pick values are not displayed')
        markets = self.site.greyhound_event_details.tab_content.event_markets_list
        self.assertTrue(markets, msg="Markets are not found")

    def test_005_verify_race_distance_correctness(self):
        """
        DESCRIPTION: Verify race distance correctness
        EXPECTED: Race distance value corresponds to **distance** attribute from RacingPost microservice response
        """
        distance = self.site.greyhound_event_details.tab_content.race_details.race_distance
        expected_distance = f'{self.event.distance}m'
        self.assertEqual(distance.value, expected_distance,
                         msg=f'Event distance "{distance.value}" is not the same '
                             f'as got from Timeform response "{expected_distance}"')

    def test_006_verify_race_grade_correctness(self):
        """
        DESCRIPTION: Verify race grade correctness
        EXPECTED: grade value corresponds to **raceType or greade??** attribute from RacingPost microservice response
        """
        grade = self.site.greyhound_event_details.tab_content.grade
        self.assertTrue(grade, msg='Grade is not displayed as expected')
