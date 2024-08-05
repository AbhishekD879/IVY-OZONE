from datetime import datetime
import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException

@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_beta2
@pytest.mark.high
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.reg157_fix
@vtest
class Test_C10436244_Ladbrokes_Verify_info_about_race_on_the_Race_Card_EDP(BaseRacing):
    """
    TR_ID: C10436244
    NAME: [Ladbrokes] Verify info about race on the Race Card (EDP)
    DESCRIPTION: This test case verifies information from Racing Post about the race on the Racing Card (EDP)
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event with race form present
        DESCRIPTION: Navigate to EDP page
        """
        self.__class__.event_info = self.get_racing_event_with_form_details(distance=True, going=True)
        if not self.event_info:
            raise SiteServeException('Racing events with distance and going details are not available')
        self.__class__.event_id = list(self.event_info.keys())[0]
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_001_verify_the_information_about_the_race_on_the_racing_card(self):
        """
        DESCRIPTION: Verify the information about the race on the Racing Card
        DESCRIPTION: [Design Mobile](https://app.zeplin.io/project/5ba39ed8bae1840f5adf5467/screen/5bb5fb254f797f1a1be2c8a7)
        DESCRIPTION: [Design Desktop](https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5c6d6283959ef19a213306d1)
        EXPECTED: Further information from Racing Post is displayed:
        EXPECTED: - Race Title
        EXPECTED: - Race Type
        EXPECTED: - Going (Soft / Heavy /Good / Standard etc)
        EXPECTED: - Distance
        """
        self.__class__.race_details = self.site.racing_event_details.tab_content.race_details
        self.assertTrue(self.race_details.has_race_title(), msg='Race Title is not displayed')
        # ========> commented because Race Type not available in FE in both beta and prod environments
        # self.assertTrue(self.race_details.has_race_type(), msg='Race Type is not displayed')
        self.assertTrue(self.race_details.has_race_distance(), msg='Race Distance is not displayed')
        if self.event_info[self.event_id].get('going'):
            self.assertTrue(self.race_details.has_race_going(), msg='Race Going is not displayed')

    def test_002_verify_race_title(self):
        """
        DESCRIPTION: Verify Race Title
        EXPECTED: - Race Title  is displayed below event time & name (e.g., 'Watch Irish Racing on Racing TV')
        EXPECTED: - Race Title = 'raceName' attribute from Racing Post response
        """
        race_title = self.race_details.race_title.name.upper()
        actual_race_title = race_title.replace('\n', '')
        time = datetime.strptime(self.event_info[self.event_id].get('time'), "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
        course_name = self.event_info[self.event_id].get('courseName').upper()
        split_course_name = course_name.split(' ')
        result_course_name = ' '.join(split_course_name[:1])
        expected_race_title = f'{time}{result_course_name}'
        self.assertEqual(actual_race_title, expected_race_title,
                         msg=f'Expected Race Title is "{expected_race_title}" but actual is "{actual_race_title}"')

    def test_003_verify_race_type(self):
        """
        DESCRIPTION: Verify Race Type
        EXPECTED: - Race Type is displayed below Race Title (e.g., 'Chase Turf')
        EXPECTED: - Race Type = 'RaceType' attribute from Racing Post response. Description is displayed (not code)
        """
        # ========> commented because Race Type not available in FE in both beta and prod environments
        # actual_race_type = self.race_details.race_type.name
        # type_code = self.datafabric_data['raceType']
        # expected_race_type = vec.racing.RACE_TYPE._asdict().get(type_code)
        # self.assertEqual(actual_race_type, expected_race_type, msg=f'Actual: "{actual_race_type}" race type does not '
        #                                                            f'match with expected: "{expected_race_type}"')

    def test_004_verify_going(self):
        """
        DESCRIPTION: Verify Going (Soft / Heavy /Good / Standard etc)
        EXPECTED: - Going is displayed below Race Title, after Race Type (e.g., 'Good to Soft')
        EXPECTED: - Going = 'goingCode' attribute from Racing Post response  (e.g.,"GS")
        """
        actual_race_going = self.race_details.race_going.value.upper()
        expected_race_going = self.event_info[self.event_id]['going'].upper()
        self.assertEqual(actual_race_going, expected_race_going,
                         msg=f'Actual: "{actual_race_going}" race going does not '
                             f'match with expected: "{expected_race_going}"')

    def test_005_verify_distance(self):
        """
        DESCRIPTION: Verify Distance
        EXPECTED: - Distance is displayed below Race Title, after 'Going' (e.g., 2m 4f)
        EXPECTED: - Distance = 'distance' attribute from Racing Post response
        """
        actual_race_distance = self.race_details.race_distance.value
        expected_race_distance = self.event_info[self.event_id]['distance']
        self.assertEqual(actual_race_distance.strip(), expected_race_distance.strip(),
                         msg=f'Expected Race Distance is "{expected_race_distance}" but actual is "{actual_race_distance}"')