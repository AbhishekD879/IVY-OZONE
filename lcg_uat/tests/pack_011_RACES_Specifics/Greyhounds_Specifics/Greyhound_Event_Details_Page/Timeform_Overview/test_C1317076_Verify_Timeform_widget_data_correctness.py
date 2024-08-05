import pytest
import tests
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # coral only, ladbrokes uses Datafabric instead of Timeform
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.frequent_blocker
@vtest
class Test_C1317076_Verify_Timeform_widget_data_correctness(BaseGreyhound):
    """
    TR_ID: C1317076
    NAME: Verify Timeform widget data correctness
    DESCRIPTION: This test case verifies Timeform widget data correctness on Greyhounds Event Details page
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - TimeForm info will NOT be displayed.
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -----
    PRECONDITIONS: To retrieve data for particular event use the link:
    PRECONDITIONS: https://{endpoint}/api/v1/greyhoundracing/race/{openbetID}/openbet
    PRECONDITIONS: where endpoint can be:
    PRECONDITIONS: * coral-timeform-dev0.symphony-solutions.eu - DEV
    PRECONDITIONS: * coral-timeform-dev1.symphony-solutions.eu  - DEV1(PHOENIX)
    PRECONDITIONS: * coral-timeform-tst2.symphony-solutions.eu - TST2
    PRECONDITIONS: * coral-timeform-stg2.symphony-solutions.eu - STG
    PRECONDITIONS: * coral-timeform.symphony-solutions.eu -PROD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *  **trainerFullName** - to check trainer name correctness
    PRECONDITIONS: *  **starRating** - to check stars rating correctness
    PRECONDITIONS: *  **greyHoundFullName** - to check name of dog correctness
    PRECONDITIONS: *  **positionPrediction** - to check position prediction of dogs
    PRECONDITIONS: *  **verdict** - to check Timeform summary correctness
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        race_info = self.get_initial_data_system_configuration().get('raceInfo', {})
        if not race_info:
            race_info = self.cms_config.get_system_configuration_item('raceInfo')
        if not race_info.get('timeFormEnabled'):
            raise CmsClientException('Time Form is disabled in CMS')

        racing_data_hub = self.get_initial_data_system_configuration().get('RacingDataHub', {})
        if not racing_data_hub:
            racing_data_hub = self.cms_config.get_system_configuration_item('RacingDataHub')
        if racing_data_hub.get('isEnabledForGreyhound'):
            raise CmsClientException('Datafabric data is enabled in CMS for Greyhounds. '
                                     'Time Form will not be available.')

        params = self.get_event_details(time_form_info=True)
        self.__class__.eventID = params.event_id
        self.__class__.event_name = params.event_name
        self.__class__.expected_verdict = params.verdict
        self.__class__.expected_prediction = self.get_positions_prediction(params.outcomes_info)
        self._logger.debug(f'**** Outcomes info {params.outcomes_info}')

    def test_001_load_oxygen_app_in_desktop_mode_with_resolution_of_970px(self):
        """
        DESCRIPTION: Load Oxygen app in Desktop mode with resolution of 970px
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('Homepage', timeout=40)
        self.device.set_viewport_size(width=970, height=970)

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing', timeout=20)

    def test_003_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: * Event details page is opened
        EXPECTED: * Timeform widget is located under selections list
        EXPECTED: * Timeform is expanded by default
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
        self.site.wait_content_state('GreyHoundEventDetails', timeout=20)
        self.__class__.timeform_overview = self.site.greyhound_event_details.tab_content.timeform_overview
        self.assertTrue(self.timeform_overview, msg='TimeForm widget is not displayed')
        self.assertTrue(self.timeform_overview.is_expanded(), msg='Timeform is not expanded by default')

    def test_004_verify_name_of_dog_correctness_displayed_next_to_tfpick_label(self):
        """
        DESCRIPTION: Verify name of dog correctness displayed next to 'TFPick' label
        EXPECTED: Name of dog corresponds to **greyHoundFullName** attribute from Timeform microservice response
        """
        if self.expected_prediction:
            self.assertTrue(self.site.greyhound_event_details.tab_content.timeform_overview.has_prediction(),
                            msg=f'No prediction info found for event "{self.event_name}"')
            self.__class__.prediction = self.site.greyhound_event_details.tab_content.timeform_overview.prediction

            prediction_val = self.site.greyhound_event_details.tab_content.timeform_overview.prediction_value
            self.__class__.prediction_value = prediction_val.text
        expected_prediction_label = f'{vec.racing.TF}{vec.racing.PICK}'.upper()
        self.assertEqual(self.prediction.text, expected_prediction_label,
                         msg=f'Event prediction label "{self.prediction.text}" '
                             f'is not "{expected_prediction_label}"')

        self.assertTrue(self.prediction_value, msg='Prediction value is empty')

    def test_005_verify_timeform_summary_correctness(self):
        """
        DESCRIPTION: Verify Timeform summary correctness
        EXPECTED: Timeform summary corresponds to **verdict** attribute from Timeform microservice response
        """
        summary = self.timeform_overview.summary_text
        self.assertEqual(summary.value, self.expected_verdict,
                         msg=f'Prediction dog name "{summary.value}" is not the same '
                             f'as got from Timeform "{self.expected_verdict}"')

    def test_006_verify_3_dogs_ordering(self):
        """
        DESCRIPTION: Verify 3 dogs ordering
        EXPECTED: 3 dogs are ordered according to **positionPrediction** and **starRating** attributes from Timeform microservice response (from the highest to the lowest)
        """
        self.assertTrue(self.timeform_overview.has_positions(), msg='No positions section found')
        self.__class__.positions = self.timeform_overview.positions.items_as_ordered_dict
        timeform_positions_len = len(self.positions)
        self.assertEqual(timeform_positions_len, 3,
                         msg=f'"{timeform_positions_len}" dogs with Timeform Summary Information '
                             f'are shown while 3 expected')
        for index, (name, position) in enumerate(self.positions.items()):
            self.assertEqual(name, list(self.expected_prediction[index].keys())[0])
            self.assertEqual(position.trainer_name, list(self.expected_prediction[index].values())[0]['trainer_name'])
            self.assertEqual(position.stars_count, list(self.expected_prediction[index].values())[0]['star_rating'])
            self.assertNotEqual(list(self.expected_prediction[index].values())[0]['status'], 'Non-Runner')

    def test_007_verify_name_of_dog_correctness(self):
        """
        DESCRIPTION: Verify name of dog correctness
        EXPECTED: Name of dog corresponds to **positionPrediction** attribute from Timeform microservice response
        """
        sections = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertIn(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB, markets,
                      msg=f'"{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}" market is not in "{markets}" markets')
        w_or_ew_section = markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.__class__.outcomes = w_or_ew_section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')

        for outcome_name, outcome in self.outcomes.items():
            if 'Unnamed Favourite' in outcome_name:
                del self.outcomes[outcome_name]

        for outcome_name, outcome in self.outcomes.items():
            if not outcome.bet_button.is_enabled():
                del self.outcomes[outcome_name]

        ui_dogs_names = list(self.outcomes.keys())
        dogs_names = [list(node.keys())[0] for node in self.expected_prediction]
        self.assertListEqual(sorted(ui_dogs_names), sorted(dogs_names),
                             msg=f'Dogs names in timeform response \n"{sorted(dogs_names)}" '
                                 f'are not the same as on UI \n"{sorted(ui_dogs_names)}"')

    def test_008_verify_name_of_trainer_correctness(self):
        """
        DESCRIPTION: Verify name of trainer correctness
        EXPECTED: Name of trainer corresponds to **trainerFullName** attribute Timeform microservice response
        EXPECTED: **NOTE** meeting name returned in **trainerFullName** attribute is NOT displayed on FE
        """
        trainer_names_ui = [outcome.trainer_name.value for outcome in self.outcomes.values()]
        trainer_names = []
        for node in self.expected_prediction:
            name = list(node.keys())[0]
            trainer_names.append(node[name]['trainer_name'])
        self.assertListEqual(sorted(trainer_names_ui), sorted(trainer_names),
                             msg=f'Trainer names in timeform response "{sorted(trainer_names)}" '
                                 f'are not the same as on UI "{sorted(trainer_names_ui)}"')

    def test_009_verify_stars_rating_correctness(self):
        """
        DESCRIPTION: Verify stars rating correctness
        EXPECTED: Stars rating  corresponds to **starRating** attribute Timeform microservice response
        """
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        w_or_ew_section = markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.__class__.outcomes = w_or_ew_section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')
        for outcome_name, outcome in self.outcomes.items():
            if outcome_name != 'Unnamed Favourite':
                outcome.click()
                sleep(3)
                self.site.contents.scroll_to()
                star_rating = outcome.expanded_summary.stars_count
                for node in self.expected_prediction:
                    name = list(node.keys())[0]
                    if name == outcome_name:
                        self.assertEqual(int(star_rating), node[name]['star_rating'],
                                         msg=f'Star rating "{star_rating}" is not the same as in '
                                             f'timeform response "{node[name]["star_rating"]}" '
                                             f'for outcome "{outcome_name}"')
            break

    def test_010_verify_non_runner_selection_within_timeform_summary_information(self):
        """
        DESCRIPTION: Verify Non-runner selection within Timeform Summary Information
        EXPECTED: Non-runner selection is NOT included in Timeform Summary Information
        """
        for position_name in self.positions.keys():
            self.assertNotIn('Unnamed Favourite', position_name,
                             msg=f'"Unnamed Favourite" is displayed in Timeform Summary for "{position_name}"')
        self.device.set_viewport_size(width=1025, height=1025)

    def test_011_change_resolution_from_970px_to_1025px_and_repeat_steps_4_10(self):
        """
        DESCRIPTION: Change resolution from 970px to 1025px and repeat steps #4-10
        EXPECTED:
        """
        self.test_004_verify_name_of_dog_correctness_displayed_next_to_tfpick_label()
        self.test_005_verify_timeform_summary_correctness()
        self.test_006_verify_3_dogs_ordering()
        self.test_007_verify_name_of_dog_correctness()
        self.test_008_verify_name_of_trainer_correctness()
        self.test_010_verify_non_runner_selection_within_timeform_summary_information()

    def test_012_change_resolution_from_1025px_to_1280px_and_repeat_steps_4_10(self):
        """
        DESCRIPTION: Change resolution from 1025px to 1280px and repeat steps #4-10
        EXPECTED:
        """
        self.device.set_viewport_size(width=1280, height=1280)
        self.test_011_change_resolution_from_970px_to_1025px_and_repeat_steps_4_10()

    def test_013_change_resolution_from_1280px_to_1600px_and_repeat_steps_4_10(self):
        """
        DESCRIPTION: Change resolution from 1280px to 1600px and repeat steps #4-10
        EXPECTED:
        """
        sleep(2)
        self.device.set_viewport_size(width=1600, height=1600)
        self.test_011_change_resolution_from_970px_to_1025px_and_repeat_steps_4_10()
