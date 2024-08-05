import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # coral only, ladbrokes uses Datafabric instead of Timeform
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.prod_incident
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.races
@pytest.mark.frequent_blocker
@vtest
class Test_C1165690_C1165695_Verify_Timeform_Selection_And_Summary_Overview(BaseGreyhound):
    """
    TR_ID: C1165690  # TODO: to split test scripts (VOL-2996)
    TR_ID: C1165695
    VOL_ID: C9697590
    NAME: Verify Timeform Selection Overview and Summary Information
    DESCRIPTION: This test case verifies Timeform Selection Overview on Greyhounds event details page
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
    PRECONDITIONS: *  **form** - to check form value correctness
    """
    keep_browser_open = True
    win_or_each_way_tab = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB

    def test_001_get_greyhound_event_with_timeform_data(self):
        """
        DESCRIPTION: Get greyhound event with timeform data
        EXPECTED: Event id is found
        """
        race_info = self.get_initial_data_system_configuration().get('raceInfo')
        if not race_info:
            race_info = self.cms_config.get_system_configuration_item('raceInfo')
        if not race_info.get('timeFormEnabled'):
            raise CmsClientException('Time Form is disabled in CMS')

        racing_data_hub = self.get_initial_data_system_configuration().get('RacingDataHub')
        if not racing_data_hub:
            racing_data_hub = self.cms_config.get_system_configuration_item('RacingDataHub')
        if racing_data_hub and racing_data_hub.get('isEnabledForGreyhound') is True:
            raise CmsClientException('Datafabric data is enabled in CMS for Greyhounds. '
                                     'Time Form will not be available.')

        params = self.get_event_details(time_form_info=True)
        self.__class__.eventID, self.__class__.event_name = params.event_id, params.event_name
        self.__class__.outcomes_info = self.get_positions_prediction(params.outcomes_info)

    def test_002_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: * Event details page is opened
        EXPECTED: * Timeform overview is displayed above markets
        EXPECTED: * 'Show more' link is available
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
        self.__class__.timeform_overview = self.site.greyhound_event_details.tab_content.timeform_overview

    def test_003_go_to_selection_area(self):
        """
        DESCRIPTION: Go to selection area
        EXPECTED: Selection area consists of:
        EXPECTED: * Runner number
        EXPECTED: * Dogs name
        EXPECTED: * 'Trainer' label and trainer name corresponds to **trainer_full_name** attribute from Timeform microservice response
        # EXPECTED: * 'Form' label and Form value corresponds to **form** attribute from Timeform microservice response #TODO not implemented due to https://jira.egalacoral.com/browse/BMA-29238
        EXPECTED: * Expandable/collapsible arrow with 'expand' default state
        EXPECTED: * Timeform Selection Summary Information is expanded on expand and collapsed on collapse
        EXPECTED: Stars rating corresponds to **star_rating** attribute Timeform microservice response for particular dog
        EXPECTED: On expanded Timeform Summary, text corresponds to onelinecomment attribute from Timeform microservice response for particular dog
        # cannot test 3 following items as we never got Timeform Selection Summary Information with more than 100 symbols
        # EXPECTED: 'Show More' option is displayed when Timeform Selection Summary Information is more than 100 characters
        # EXPECTED: 'Show More' option becomes 'Show Less' after tapping it
        # EXPECTED: All Timeform Selection Summary is displayed after tapping 'Show More' option
        """
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        market_name = self.win_or_each_way_tab if self.win_or_each_way_tab in markets else vec.racing.RACING_EDP_WIN_OR_EACH_WAY_FULL_NAME
        w_or_ew_section = markets.get(market_name)
        self.assertTrue(w_or_ew_section, msg='"%s" is not found in markets "%s"'
                                             % (market_name, ', '.join(markets.keys())))
        selections = w_or_ew_section.items_as_ordered_dict
        self.assertTrue(selections, msg=f'No selections found in "{market_name}" section')
        for selection_name, selection in selections.items():
            if selection_name == 'Unnamed Favourite' or 'N/R' in selection_name:
                self._logger.warning('*** Skipping verification for Unnamed Favourite or N/R selection')
                continue
            self.assertTrue(selection.has_silks, msg=f'No runner number found for "{selection_name}"')
            timeform_outcome_info = next((list(outcome_info.values())[0] for outcome_info in self.outcomes_info
                                          if list(outcome_info.keys())[0] in selection_name), None)

            self.assertTrue(timeform_outcome_info, msg=f'Outcome info not found for "{selection_name}"')
            trainer_name = timeform_outcome_info.get('trainer_name', '')
            self.assertEqual(selection.trainer_name.value, trainer_name,
                             msg=f'Trainer name "{selection.trainer_name.value}" '
                                 f'is not the same as expected "{trainer_name}"')
            self.assertEqual(selection.trainer_name.label, vec.racing.TRAINER,
                             msg=f'Label "{selection.trainer_name.label}" '
                                 f'is not the same as expected "{vec.racing.TRAINER}"')
            self.assertTrue(selection.has_show_summary_toggle(),
                            msg=f'No summary toggle found for selection "{selection_name}"')
            self.assertFalse(selection.has_expanded_summary(expected_result=False),
                             msg=f'Summary is not collapsed by default for selection "{selection_name}"')
            selection.show_summary_toggle.click()
            self.assertTrue(selection.has_expanded_summary(),
                            msg=f'Summary is not shown after expanding selection "{selection_name}"')
            stars_count = selection.expanded_summary.stars_count
            expected_stars_count = timeform_outcome_info.get('star_rating')
            self.assertEqual(stars_count, expected_stars_count,
                             msg=f'Stars rating count "{stars_count}" is not the same as the one got from Timeform '
                                 f'"{expected_stars_count}" for "{selection_name}"')
            outcome_overview = selection.expanded_summary.outcome_overview
            expected_outcome_overview = timeform_outcome_info.get('one_line_comment')
            self.assertEqual(outcome_overview, expected_outcome_overview,
                             msg=f'Outcome overview "{outcome_overview}" is not the same as '
                                 f'the one got from Timeform "{expected_outcome_overview}"')
            selection.show_summary_toggle.click()
            result = wait_for_result(lambda: selection.has_expanded_summary(expected_result=False),
                                     expected_result=False,
                                     name='Expanded summary to hide',
                                     timeout=1)
            self.assertFalse(result,
                             msg=f'Summary is still shown after collapsing for selection "{selection_name}"')
