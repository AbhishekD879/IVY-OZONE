import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


@pytest.mark.crl_tst2  # coral only, ladbrokes uses Datafabric provider instead of Timeform
@pytest.mark.crl_stg2
@pytest.mark.crl_hl
@pytest.mark.crl_prod
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.frequent_blocker
@vtest
class Test_C1158561_Verify_Timeform_Overview(BaseGreyhound):
    """
    TR_ID: C1158561
    VOL_ID: C9698090
    NAME: Verify Timeform Overview
    DESCRIPTION: This test case verifies Timeform Overview on Greyhounds event details page
    PRECONDITIONS: To retrieve data for particular event use the link:
    PRECONDITIONS: https://{endpoint}/api/v1/greyhoundracing/race/{openbetID}/openbet
    PRECONDITIONS: where endpoint can be:
    PRECONDITIONS: * coral-timeform-dev0.symphony-solutions.eu - DEV
    PRECONDITIONS: * coral-timeform-dev1.symphony-solutions.eu  - DEV1(PHOENIX)
    PRECONDITIONS: * coral-timeform-tst2.symphony-solutions.eu - TST2
    PRECONDITIONS: * coral-timeform-stg2.symphony-solutions.eu - STG
    PRECONDITIONS: * coral-timeform.symphony-solutions.eu -PROD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *  **race_distance** - to check race distance correctness
    PRECONDITIONS: *  **race_grade_name** - to check race grade correctness
    PRECONDITIONS: *  **greyHoundFullName** - to check name of dog correctness
    PRECONDITIONS: * **verdict** - to check Timeform summary correctness
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get greyhound event with timeform data
        EXPECTED: Event id is found
        """
        race_info = self.get_initial_data_system_configuration().get('raceInfo', {})
        if not race_info:
            race_info = self.cms_config.get_system_configuration_item('raceInfo')
        if race_info.get('timeFormEnabled') is not True:
            raise CmsClientException('Time Form is disabled in CMS')
        racing_data_hub = self.get_initial_data_system_configuration().get('RacingDataHub', {})
        if not racing_data_hub:
            racing_data_hub = self.cms_config.get_system_configuration_item('RacingDataHub')
        if racing_data_hub.get('isEnabledForGreyhound') is True:
            raise CmsClientException('Datafabric data is enabled in CMS for Greyhounds. '
                                     'Time Form will not be available.')

        params = self.get_event_details(time_form_info=True)
        self.__class__.eventID = params.event_id
        self.__class__.expected_distance = params.distance
        self.__class__.expected_grade = params.grade
        self.__class__.event_name = params.event_name
        self.__class__.expected_verdict = params.verdict

        self._logger.debug(f'**** Outcomes info {params.outcomes_info}')
        timeform_outcomes_info = self.get_positions_prediction(params.outcomes_info)
        self.__class__.expected_prediction = \
            next((list(outcome_info.keys())[0].upper() for outcome_info in timeform_outcomes_info
                  if list(outcome_info.values())[0]['position_prediction'] == 1), None)

    def test_001_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')

    def test_002_verify_timeform_overview(self):
        """
        DESCRIPTION: Verify Timeform overview
        EXPECTED: Timeform overview consists of:
        EXPECTED: * 'Distance' label and race distance value
        EXPECTED: * 'Race Grade' label and race grade value
        EXPECTED: * Timeform logo
        EXPECTED: * 'TFPick' label and name of dog
        EXPECTED: * Timeform summary and 'Show More' option (if available)
        """
        if self.expected_distance:
            self.assertTrue(self.site.greyhound_event_details.tab_content.race_details.has_race_distance(),
                            msg='Distance not found')
            self.__class__.distance = self.site.greyhound_event_details.tab_content.race_details.race_distance
            expected_distance_label = vec.racing.DISTANCE
            self.assertEqual(self.distance.label, expected_distance_label,
                             msg=f'Event distance label "{self.distance.label}" is not "{expected_distance_label}"')
            self.assertTrue(self.distance.value, msg='Distance value is empty')
        else:
            self._logger.warning('*** No distance available, skipping the verification')

        if self.expected_grade:
            self.assertTrue(self.site.greyhound_event_details.tab_content.has_grade(), msg='Grade not found')
            self.__class__.grade = self.site.greyhound_event_details.tab_content.grade
            expected_grade_label = vec.racing.RACE_GRADE
            self.assertEqual(self.grade.label, expected_grade_label,
                             msg=f'Event grade label "{self.grade.label}" is not "{expected_grade_label}"')
            self.assertTrue(self.grade.value, msg='Grade value is empty')

        self.assertTrue(self.site.greyhound_event_details.tab_content.has_timeform_overview(),
                        msg=f'No Timeform overview found for event "{self.event_name}"')
        self.assertTrue(self.site.greyhound_event_details.tab_content.timeform_overview.has_logo_icon(),
                        msg=f'No Timeform logo icon found for event "{self.event_name}"')

        if self.expected_prediction:
            self.assertTrue(self.site.greyhound_event_details.tab_content.timeform_overview.has_prediction(),
                            msg=f'No prediction info found for event "{self.event_name}"')
            self.__class__.prediction = self.site.greyhound_event_details.tab_content.timeform_overview.prediction

            prediction_val = self.site.greyhound_event_details.tab_content.timeform_overview.prediction_value
            self.__class__.prediction_value = self.prediction.value if self.device_type == 'mobile' else prediction_val.text

            if self.device_type == 'mobile':
                expected_prediction_label = f'{vec.racing.TF}{vec.racing.PICK}'
                self.assertEqual(self.prediction.label, expected_prediction_label,
                                 msg=f'Event prediction label "{self.prediction.label}" '
                                     f'is not "{expected_prediction_label}"')
            else:
                expected_prediction_label = f'{vec.racing.TF}{vec.racing.PICK}'.upper()
                self.assertEqual(self.prediction.text, expected_prediction_label,
                                 msg=f'Event prediction label "{self.prediction.text}" '
                                     f'is not "{expected_prediction_label}"')
            self.assertTrue(self.prediction_value, msg='Prediction value is empty')
        if self.expected_verdict:
            self.__class__.summary = self.site.greyhound_event_details.tab_content.timeform_overview.summary_text
            self.assertTrue(self.summary.value, msg='Summary text is not shown')
            self.assertTrue(self.site.greyhound_event_details.tab_content.timeform_overview.has_summary_button,
                            msg='Show More button is not shown')

    def test_003_verify_race_distance_correctness(self):
        """
        DESCRIPTION: Verify race distance correctness
        EXPECTED: * Race distance value corresponds to **race_distance** attribute from Timeform microservice response
        EXPECTED: * Race distance is shown in the next format:
        EXPECTED: race_distance value + 'M' character
        """
        expected_distance = f'{self.expected_distance}M'
        self.assertEqual(self.distance.value, expected_distance,
                         msg=f'Event distance "{self.distance.value}" is not the same '
                             f'as got from Timeform response "{expected_distance}"')

    def test_004_verify_race_grade_correctness(self):
        """
        DESCRIPTION: Verify race grade correctness
        EXPECTED: Race grade value corresponds to **race_grade_name** attribute from Timeform microservice response
        """
        self.assertEqual(self.grade.value, self.expected_grade,
                         msg=f'Event grade "{self.grade.value}" is not the same '
                             f'as got from Timeform response "{self.expected_grade}"')

    def test_005_verify_name_of_dog_correctness_displayed_next_to_tfpick_label(self):
        """
        DESCRIPTION: Verify name of dog correctness displayed next to 'TFPick' label
        EXPECTED: Name of dog corresponds to **position_prediction** attribute from Timeform microservice response
        """
        self.assertEqual(self.prediction_value, self.expected_prediction,
                         msg=f'Prediction dog name "{self.prediction_value}" is not the same '
                             f'as got from Timeform "{self.expected_prediction}"')

    def test_006_verify_show_more_option(self):
        """
        DESCRIPTION: Verify 'Show More' option
        EXPECTED: * 'Show More' option becomes 'Show Less' after tapping it
        EXPECTED: * 3 dogs with Timeform Summary Information are displayed after tapping 'Show More' option
        """
        # Note: 'SHOW MORE' link is applicable only for mobile
        self.__class__.timeform_overview = self.site.greyhound_event_details.tab_content.timeform_overview
        if self.device_type == 'mobile':
            expected_button_name = 'Show Less'
            self.timeform_overview.show_summary_button.click()
            result = wait_for_result(lambda: self.timeform_overview.show_summary_button.name == expected_button_name,
                                     name=f'Button to have name "{expected_button_name}"',
                                     timeout=1)
            self.assertTrue(result, msg=f'Button name "{self.timeform_overview.show_summary_button.name}" '
                                        f'is not the same as expected "{expected_button_name}"')
        self.assertTrue(self.timeform_overview.has_positions(), msg='No positions section found')
        timeform_positions_len = len(self.timeform_overview.positions.items_as_ordered_dict)
        self.assertEqual(timeform_positions_len, 3,
                         msg=f'"{timeform_positions_len}" dogs with '
                             f'Timeform Summary Information are shown while 3 expected')

    def test_007_verify_timeform_summary_correctness(self):
        """
        DESCRIPTION: Verify Timeform summary correctness
        EXPECTED: Timeform summary corresponds to **verdict** attribute from Timeform microservice response
        """
        summary = self.timeform_overview.summary_text
        self.assertEqual(summary.value, self.expected_verdict,
                         msg=f'Prediction dog name "{summary.value}" is not the same '
                             f'as got from Timeform "{self.expected_verdict}"')

    def test_008_verify_show_less_option(self):
        """
        DESCRIPTION: Verify 'Show Less' option
        EXPECTED: * 3 dogs with Timeform Summary Information are collapsed after tapping 'Show Less' option
        EXPECTED: * 'Show Less' option becomes 'Show More' after tapping it
        """
        # Note: 'SHOW LESS' link is applicable only for mobile
        if self.device_type == 'mobile':
            expected_button_name = 'Show More'
            self.timeform_overview.show_summary_button.click()
            result = wait_for_result(lambda: self.timeform_overview.show_summary_button.name == expected_button_name,
                                     name=f'Button to have name "{expected_button_name}"',
                                     timeout=1)
            self.assertTrue(result, msg=f'Button name "{self.timeform_overview.show_summary_button.name}" '
                                        f'is not the same as expected "{expected_button_name}"')
            self.assertFalse(self.timeform_overview.has_positions(expected_result=False),
                             msg='Positions section should not be shown when summary is collapsed')
