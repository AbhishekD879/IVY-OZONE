import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # coral only, ladbrokes uses Datafabric instead of Timeform
@pytest.mark.crl_stg2
@pytest.mark.crl_hl
@pytest.mark.crl_prod
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.races
@pytest.mark.medium
@pytest.mark.frequent_blocker
@vtest
class Test_C1159079_Verify_Timeform_Summary_Information(BaseGreyhound):
    """
    TR_ID: C1159079
    VOL_ID: C9698348
    NAME: Verify Timeform Summary Information
    DESCRIPTION: This test case verifies Timeform Summary Information on Greyhounds event details page
    PRECONDITIONS: To retrieve data for particular event use the link:
    PRECONDITIONS: https://{endpoint}/api/v1/greyhoundracing/race/{openbetID}/openbet
    PRECONDITIONS: where endpoint can be:
    PRECONDITIONS: * coral-timeform-dev0.symphony-solutions.eu - DEV
    PRECONDITIONS: * coral-timeform-dev1.symphony-solutions.eu  - DEV1(PHOENIX)
    PRECONDITIONS: * coral-timeform-tst2.symphony-solutions.eu - TST2
    PRECONDITIONS: * coral-timeform-stg2.symphony-solutions.eu - STG
    PRECONDITIONS: * coral-timeform.symphony-solutions.eu -PROD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *  **trainer_full_name** - to check trainer name correctness
    PRECONDITIONS: *  **star_rating** - to check stars rating correctness
    PRECONDITIONS: *  **greyHoundFullName** - to check name of dog correctness
    """
    keep_browser_open = True

    def test_001_get_greyhound_event_with_timeform_data(self):
        """
        DESCRIPTION: Get greyhound event with timeform data
        EXPECTED: Event id is found
        """
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
        self.__class__.expected_prediction = self.get_positions_prediction(params.outcomes_info)

    def test_002_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: * Event details page is opened
        EXPECTED: * Timeform overview is displayed above markets
        EXPECTED: * 'Show more' link is available
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
        self.__class__.timeform_overview = self.site.greyhound_event_details.tab_content.timeform_overview

    def test_003_tap_show_more_link(self):
        """
        DESCRIPTION: Tap 'Show more' link
        EXPECTED: Timeform Summary Information is displayed for 3 dogs and consists of the next data for each dog:
        EXPECTED: * Dog image
        EXPECTED: * Name of dog
        EXPECTED: * 'Trainer' label and name of trainer
        EXPECTED: * 'Rating' label and Stars rating
        """
        # Note: 'SHOW MORE' link is applicable only for mobile
        if self.device_type == 'mobile':
            expected_button_name = 'Show Less'
            self.timeform_overview.show_summary_button.click()
            result = wait_for_result(lambda: self.timeform_overview.show_summary_button.name == expected_button_name,
                                     name=f'Button to have name "{expected_button_name}"',
                                     timeout=1)
            self.assertTrue(result, msg=f'Button name "{self.timeform_overview.show_summary_button.name}" '
                                        f'is not the same as expected "{expected_button_name}"')
        self.assertTrue(self.timeform_overview.has_positions(), msg='No positions section found')
        self.__class__.positions = self.timeform_overview.positions.items_as_ordered_dict
        timeform_positions_len = len(self.positions)
        self.assertEqual(timeform_positions_len, 3,
                         msg=f'"{timeform_positions_len}" dogs with Timeform Summary Information '
                             f'are shown while 3 expected')

        for position_name, position in self.positions.items():
            self.assertTrue(position.has_logo(), msg=f'Greyhound "{position_name}" does not have logo')
            self.assertTrue(position.trainer_name, msg=f'Greyhound "{position_name}" does not have trainer name')
            self.assertTrue(position.trainer_label, msg=f'Greyhound "{position_name}" does not have logo')
            self.assertTrue(position.has_rating(), msg=f'Greyhound "{position_name}" does not have rating')
            self.assertTrue(position.stars_count, msg=f'Greyhound "{position_name}" does not have stars in rating')

    def test_004_verify_dogs_information_and_ordering(self):
        """
        DESCRIPTION: Verify: 3 dogs ordering, name of dog correctness, name of trainer correctness and Non runner selection within Timeform Summary
        EXPECTED: 3 dogs are ordered according to **position_prediction** and **star_rating** attributes from Timeform microservice response (from the highest to the lowest)
        EXPECTED: Name of dog corresponds to **position_prediction** attribute from Timeform microservice response
        EXPECTED: **NOTE** meeting name returned in **trainer_full_name** attribute is NOT displayed on FE
        EXPECTED: Name of trainer corresponds to **trainer_full_name** attribute Timeform microservice response
        EXPECTED: Non-runner selection is NOT included in Timeform Summary
        """
        for index, (name, position) in enumerate(self.positions.items()):
            self.assertEqual(name, list(self.expected_prediction[index].keys())[0])
            self.assertEqual(position.trainer_name, list(self.expected_prediction[index].values())[0]['trainer_name'])
            self.assertEqual(position.stars_count, list(self.expected_prediction[index].values())[0]['star_rating'])
            self.assertNotEqual(list(self.expected_prediction[index].values())[0]['status'], 'Non-Runner')

    def test_005_verify_name_of_dog_correctness(self):
        """
        DESCRIPTION: Verify name of dog correctness
        EXPECTED: Name of dog corresponds to position_prediction attribute from Timeform microservice response
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

    def test_006_verify_name_of_trainer_correctness(self):
        """
        DESCRIPTION: Verify name of trainer correctness
        EXPECTED: Name of trainer corresponds to trainerfullname attribute Timeform microservice response
        """
        trainer_names_ui = [outcome.trainer_name.value for outcome in self.outcomes.values()]

        trainer_names = []
        for node in self.expected_prediction:
            name = list(node.keys())[0]
            trainer_names.append(node[name]['trainer_name'])

        self.assertListEqual(sorted(trainer_names_ui), sorted(trainer_names),
                             msg=f'Trainer names in timeform response "{sorted(trainer_names)}" '
                             f'are not the same as on UI "{sorted(trainer_names_ui)}"')

    def test_007_verify_stars_rating_correctness(self):
        """
        DESCRIPTION: Verify stars rating correctness
        EXPECTED: Stars rating corresponds to star_rating attribute Timeform microservice response
        """
        for outcome_name, outcome in self.outcomes.items():
            outcome.click()
            star_rating = outcome.expanded_summary.stars_count
            for node in self.expected_prediction:
                name = list(node.keys())[0]
                if name == outcome_name:
                    self.assertEqual(int(star_rating), node[name]['star_rating'],
                                     msg=f'Star rating "{star_rating}" is not the same as in '
                                         f'timeform response "{node[name]["star_rating"]}" '
                                         f'for outcome "{outcome_name}"')

    def test_008_verify_non_runner_selection_within_timeform_summary(self):
        """
        DESCRIPTION: Verify Non runner selection within Timeform Summary
        EXPECTED: Non-runner selection is NOT included in Timeform Summary
        """
        for position_name in self.positions.keys():
            self.assertNotIn('Unnamed Favourite', position_name,
                             msg=f'"Unnamed Favourite" is displayed in Timeform Summary for "{position_name}"')
