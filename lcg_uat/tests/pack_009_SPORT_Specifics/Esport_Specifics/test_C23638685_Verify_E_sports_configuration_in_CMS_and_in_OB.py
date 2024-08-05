import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events in prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C23638685_Verify_E_sports_configuration_in_CMS_and_in_OB(BaseSportTest):
    """
    TR_ID: C23638685
    NAME: Verify  E-sports configuration in CMS and in OB.
    DESCRIPTION: This test case verifies E-sports correct configuration.
    DESCRIPTION: Created to cover this Prod Incident - https://jira.egalacoral.com/browse/BMA-37381
    PRECONDITIONS: To verify correctness of configuration you need to check it in CMS:
    PRECONDITIONS: SPORT PAGES -> SPORT CATEGORIES -> ESPORTS
    PRECONDITIONS: Category ID - 148
    PRECONDITIONS: SS Category Code - ESPORTS
    PRECONDITIONS: Also you need to check configuration in according Back office:
    PRECONDITIONS: Check Market template - |Match Result (2 way)| with Display Sort - HH
    """
    keep_browser_open = True
    event_available = None
    sport_in_cms = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Events for esports and verify ESPORTS configuration in CMS
        """
        category_id = self.ob_config.esports_config.category_id
        sport_categories = self.cms_config.get_sport_categories()
        for sport in sport_categories:
            if 'esports' in sport['targetUri']:
                self.assertEqual(sport['categoryId'], category_id,
                                 msg=f'Actual category id "{sport["categoryId"]}" is not as '
                                     f'Expected "{category_id}".')
                self.assertEqual(sport['ssCategoryCode'], 'ESPORTS',
                                 msg=f'Actual category code "{sport["ssCategoryCode"]}" is not as '
                                     f'Expected "{"ESPORTS"}".')
                self.sport_in_cms = True
                break

        if not self.sport_in_cms:
            raise CmsClientException('ESPORTS sport category is not configured in the CMS')

        self.__class__.event = self.ob_config.add_autotest_esports_event()
        self.__class__.event_name = f'{self.event.team1} v {self.event.team2}'

    def test_001_verify_that_the_newly_created_e_sports_event_is_visible_of_the_fe(self):
        """
        DESCRIPTION: Verify that the newly created E-sports event is visible of the FE.
        EXPECTED: If the configuration is correct, then the user should see the newly created event on the FE.
        """
        self.navigate_to_page('sport/esports')
        self.site.wait_content_state_changed()
        sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in list(sections.items()):
            events = list(section.items_as_ordered_dict.keys())
            if self.event_name in events:
                self._logger.info(f'Event {self.event_name} is available on FE')
                self.event_available = True
                break
            else:
                continue
        self.assertTrue(self.event_available, msg=f'Event "{self.event_name}" is not available on FE')

    def test_002_verify_that_response_is_correct_dev_toolsnetwork_tab(self):
        """
        DESCRIPTION: Verify that response is correct dev tools/network tab.
        EXPECTED: Data should have the following parameters in SS response for the Esports event:
        EXPECTED: categoryCode: "ESPORTS"
        EXPECTED: categoryId: "148"
        EXPECTED: categoryName: "ESports"
        """
        expected_parameters = {'categoryCode': "ESPORTS",
                               'categoryId': "148",
                               'categoryName': "ESports"}

        site_server_req = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event.event_id)
        event_params = site_server_req[0]['event']

        self.assertEqual(expected_parameters['categoryCode'], event_params['categoryCode'],
                         msg=f'Actual parameter: "{event_params["categoryCode"]}" is not as'
                             f'Expected parameter: "{expected_parameters["categoryCode"]}"')
        self.assertEqual(expected_parameters['categoryId'], event_params['categoryId'],
                         msg=f'Actual parameter: "{event_params["categoryId"]}" is not as'
                             f'Expected parameter: "{expected_parameters["categoryId"]}"')
        self.assertEqual(expected_parameters['categoryName'], event_params['categoryName'].replace('|', ''),
                         msg=f'Actual parameter: "{event_params["categoryName"].replace("|", "")}" is not as'
                             f'Expected parameter: "{expected_parameters["categoryName"]}"')
