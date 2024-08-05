import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from crlat_siteserve_client.utils.exceptions import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.race_form
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.reg157_fix
@vtest
class Test_C1056148_Verify_Racing_Post_SilksForm_Information_when_silks_are_available(BaseRacing):
    """
    TR_ID: C1056148
    NAME: Verify Racing Post Silks/Form Information when silks are available
    DESCRIPTION: This test case verifies how racing post info will be displayed for each event
    PRECONDITIONS: 1. Silks should be available for a horse racing event.
    PRECONDITIONS: 2. To retrieve racing post silks, form and odds information follow the next steps:
    PRECONDITIONS: Open Develop Tools -> Network->All->Choose event id and look at Response:
    PRECONDITIONS: Find {racingFormOutcome} response and use attributes on outcome level:
    PRECONDITIONS: - **'name'** to see a horse name
    PRECONDITIONS: - **'runnerNumber'** to see a number
    PRECONDITIONS: - **'draw'** to see markets status
    PRECONDITIONS: - **'jockey'** to see a jockey information
    PRECONDITIONS: - **'trainer'** to see trainer name
    PRECONDITIONS: - **'formGuide'** to see a form attribute
    PRECONDITIONS: - **'courseDistanceWinner'** to see Course or/and Distance winner badge
    PRECONDITIONS: - **'silkName'** to find out a name of file to download needed silk
    PRECONDITIONS: Silk can be downloaded using Image URL's.
    PRECONDITIONS: Image URL's:
    PRECONDITIONS: CI-TST2: http://img-tst2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-STG: http://img-stg2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-PROD: http://img.coral.co.uk/img/racing_post/<silkName>
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event
        """
        self.__class__.event_info = self.get_racing_event_with_form_details(silk_availability=True)
        if not self.event_info:
            raise SiteServeException('Racing events with form details not available')
        self.__class__.event_id = self.event_info[0]
        self.__class__.horses_details = self.event_info[1]

    def test_001_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to event details page
        EXPECTED: * Event details page is opened
        EXPECTED: * 'Win or E/W' tab is opened by default
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.markets = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets found')

    def test_002_verify_silk_icon(self):
        """
        DESCRIPTION: Verify silk icon
        EXPECTED: * Silk icon corresponds to the picture which is got from the Site Server (**'silkName'** attribute)
        EXPECTED: * Generic Silks are displayed for missed mappings
        """
        market = self.markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        market.click()
        self.__class__.outcomes = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.get(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB).items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')
        for horse_name, horse_details in self.horses_details.items():
            if self.horses_details[horse_name].get('silk'):
                expected_silk_id = self.horses_details[horse_name]['silk'].strip('.png')
                if not self.outcomes[horse_name].is_non_runner:
                    actual_silk_ids = self.outcomes[horse_name].silk
                    self.assertIn(expected_silk_id, actual_silk_ids,
                                  msg=f'expected horse {horse_name} silk id {expected_silk_id} is not available in actual {actual_silk_ids}')

    def test_003_verify_horse_name(self):
        """
        DESCRIPTION: Verify horse name
        EXPECTED: Horse name corresponds to the **'name' **attribute
        """
        expected_horses_names = list(self.horses_details.keys())
        actual_horses_names = [outcome_name.upper() for outcome_name, outcome in self.outcomes.items()]
        for horse_name in expected_horses_names:
            self.assertIn(horse_name.upper(), actual_horses_names,
                          msg=f'expected horse {horse_name.upper()} is not available in actual horses list {actual_horses_names}')

    def test_004_verify_runner_number(self):
        """
        DESCRIPTION: Verify runner number
        EXPECTED: Runner number corresponds to the **'runnerNumber'** attribute
        EXPECTED: Runner numbers are NOT displayed and selection (horse) names without **runnerNumber** attribute are aligned with the other horse names
        """
        for horse_name, horse_details in self.horses_details.items():
            expected_runner_number = self.horses_details[horse_name]['saddle']
            if not self.outcomes[horse_name].is_non_runner:
                actual_runner_number = self.outcomes[horse_name].runner_number
                self.assertEqual(expected_runner_number, actual_runner_number,
                                 msg=f"expected {horse_name} horse runner number is {expected_runner_number} but actual is {actual_runner_number}")

    def test_005_verify_draw_number(self):
        """
        DESCRIPTION: Verify draw number
        EXPECTED: Draw Number is contained within brackets and corresponds to the **'draw'** attribute
        """
        for horse_name, horse_details in self.horses_details.items():
            expected_draw_number = self.horses_details[horse_name]['draw']
            if not self.outcomes[horse_name].is_non_runner:
                actual_draw_number = self.outcomes[horse_name].draw_number
                self.assertEqual(expected_draw_number, actual_draw_number,
                                 msg=f"expected {horse_name} horse draw number is {expected_draw_number} but actual is {actual_draw_number}")

    def test_006_verify_jockey_trainer_information(self):
        """
        DESCRIPTION: Verify jockey/trainer information
        EXPECTED: *   Jockey information corresponds to the **'jockey'** attribute
        EXPECTED: *   Trainer information corresponds to the **'trainer' **attribute
        EXPECTED: *   The information is shown in next format: **Jockey/Trainer**
        """
        for horse_name, horse_details in self.horses_details.items():
            expected_jockey_trainer = vec.racing.JOCKEY_TRAINER_TEXT.format(jockey=self.horses_details[horse_name]['jockey'],
                                                                            trainer=self.horses_details[horse_name]['trainer'])
            if not self.outcomes[horse_name].is_non_runner:
                actual_jockey_trainer = self.outcomes[horse_name].jockey_trainer_info
                self.assertEqual(expected_jockey_trainer, actual_jockey_trainer,
                                 msg=f"expected {horse_name} horse jockey trainer name is {expected_jockey_trainer} but actual is {actual_jockey_trainer}")

    def test_007_verify_form(self):
        """
        DESCRIPTION: Verify form
        EXPECTED: Form corresponds to the **'formGuide' **attribute
        """
        for horse_name, horse_details in self.horses_details.items():
            if self.horses_details[horse_name].get('formfigs'):
                expected_form = "Form: "+self.horses_details[horse_name]['formfigs']
            else:
                expected_form = "Form: -"
            if not self.outcomes[horse_name].is_non_runner:
                actual_form = self.outcomes[horse_name].form
                self.assertEqual(expected_form, actual_form,
                                 msg=f"expected {horse_name} horse Form is {expected_form} but actual is {actual_form}")

    def test_008_verify_course_or_and_distance_winner_badgenote_not_available_on_ob_side_yet(self):
        """
        DESCRIPTION: Verify Course or/and Distance winner badge
        DESCRIPTION: [NOTE: Not available on OB side yet]
        EXPECTED: Course or/and Distance winner badge corresponds to **courseDistanceWinner** attribute:
        EXPECTED: - Course (C)
        EXPECTED: - Distance (D)
        EXPECTED: - Course and Distance (CD)
        """
        for horse_name, horse_details in self.horses_details.items():
            if self.horses_details[horse_name].get('courseDistanceWinner'):
                expected_course_distance_badge = self.horses_details[horse_name].get('courseDistanceWinner')
                if not self.outcomes[horse_name].is_non_runner:
                    actual_course_distance_badge = ','.join(self.outcomes[horse_name].course_distance_winner)
                    self.assertEqual(expected_course_distance_badge, actual_course_distance_badge,
                                     msg=f"expected {horse_name} horse CourseDistanceWinner is {expected_course_distance_badge} but actual is {actual_course_distance_badge}")