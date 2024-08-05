import pytest
from tests.base_test import vtest
from tests.Common import Common
from json import JSONDecodeError
from voltron.utils.helpers import do_request


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C60075659_Verify_sports_page_configs_receiving_in_initial_data_request(Common):
    """
    TR_ID: C60075659
    NAME: Verify sports page configs receiving in initial data request
    DESCRIPTION: Test case to verify if properties from /sport-config response are moved to /initial-data sports(Categories)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: Note:
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Info about tabs displaying depends on Platforms or Tier Type could be found here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-TabsdisplayingfordifferentPlatformsandTierTypes
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the following <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: - To find **initial-data** response enter **initial** in devTools>'Network' tab
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001__load_application_find_initial_data_response_for_sportcategories_in_devtools(self):
        """
        DESCRIPTION: * Load application
        DESCRIPTION: * Find **initial-data** response for sportCategories in devTools
        EXPECTED: sportCategories tab is present with all existing sport categories in devTools
        """
        self.site.wait_content_state("HomePage")
        cms_az_sports = [sport['imageTitle'].strip() for sport in self.cms_config.get_sport_categories()
                         if all((not sport['disabled'],
                                 sport['imageTitle'],
                                 sport['showInAZ']))]
        self.__class__.sport_categories = self.cms_config.get_initial_data().get('sportCategories', [])
        self.assertTrue(self.sport_categories, msg='No sportCategories tag in initial-data response')
        for sport in self.sport_categories:
            if sport["showInAZ"]:
                self.assertIn(sport['imageTitle'].strip(), cms_az_sports)

    def test_002_expand_any_available_sport_category__sportconfig__config(self):
        """
        DESCRIPTION: Expand any available sport category > sportConfig > config
        EXPECTED: Configurations for selected category are displayed and include following properties (if available in CMS):
        EXPECTED: config: {
        EXPECTED: title: string,
        EXPECTED: name: string,
        EXPECTED: path: string,
        EXPECTED: tier: number,
        EXPECTED: isOutrightSport: boolean,
        EXPECTED: isMultiTemplateSport: string,
        EXPECTED: oddsCardHeaderType: string | any,
        EXPECTED: request: {
        EXPECTED: categoryId: string,
        EXPECTED: siteChannels: string,
        EXPECTED: marketsCount: boolean,
        EXPECTED: dispSortName: string[],
        EXPECTED: dispSortNameIncludeOnly: string[],
        EXPECTED: marketTemplateMarketNameIntersects: string
        EXPECTED: }
        EXPECTED: }
        EXPECTED: ![](index.php?/attachments/get/122010353)
        """
        self.assertTrue(isinstance(next((sport['sportConfig']['config']['title'] for sport in self.sport_categories if
                                         sport['sportConfig']['config']['title'] == "Football"), ''), str))
        self.assertTrue(isinstance(next((sport['sportConfig']['config']['name'] for sport in self.sport_categories if
                                         sport['sportConfig']['config']['title'] == "Football"), ''), str))
        self.assertTrue(isinstance(next((sport['sportConfig']['config']['path'] for sport in self.sport_categories if
                                         sport['sportConfig']['config']['title'] == "Football"), ''), str))
        self.assertTrue(isinstance(next((sport['sportConfig']['config']['tier'] for sport in self.sport_categories if
                                         sport['sportConfig']['config']['title'] == "Football"), ''), int))
        self.assertTrue(
            isinstance(next((sport['sportConfig']['config']['isOutrightSport'] for sport in self.sport_categories if
                             sport['sportConfig']['config']['title'] == "Football"), ''), bool))
        self.assertTrue(isinstance(
            next((sport['sportConfig']['config']['isMultiTemplateSport'] for sport in self.sport_categories if
                  sport['sportConfig']['config']['title'] == "Football"), ''), bool))
        self.assertTrue(
            isinstance(next((sport['sportConfig']['config']['oddsCardHeaderType'] for sport in self.sport_categories if
                             sport['sportConfig']['config']['title'] == "Football"), ''), str))
        self.assertTrue(isinstance(
            next((sport['sportConfig']['config']['request']['categoryId'] for sport in self.sport_categories if
                  sport['sportConfig']['config']['title'] == "Football"), ''), str))
        self.assertTrue(isinstance(
            next((sport['sportConfig']['config']['request']['siteChannels'] for sport in self.sport_categories if
                  sport['sportConfig']['config']['title'] == "Football"), ''), str))
        self.assertTrue(isinstance(
            next((sport['sportConfig']['config']['request']['marketsCount'] for sport in self.sport_categories if
                  sport['sportConfig']['config']['title'] == "Football"), ''), bool))
        self.assertTrue(isinstance(
            next((sport['sportConfig']['config']['request']['dispSortName'] for sport in self.sport_categories if
                  sport['sportConfig']['config']['title'] == "Football"), ''), list))
        self.assertTrue(isinstance(next(
            (sport['sportConfig']['config']['request']['dispSortNameIncludeOnly'] for sport in self.sport_categories if
             sport['sportConfig']['config']['title'] == "Football"), ''), list))
        self.assertTrue(isinstance(
            next((sport['sportConfig']['config']['request']['siteChannels'] for sport in self.sport_categories if
                  sport['sportConfig']['config']['title'] == "Football"), ''), str))

    def test_003_navigate_to_some_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to some Sport Landing Page
        EXPECTED: * 'sport-tab/%categoryID%' request is sent
        EXPECTED: * response of the request does not include information from initial-data response
        EXPECTED: * only tabs data is present (including time filters if available):
        EXPECTED: ![](index.php?/attachments/get/122019625)
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state("football")
        sports_tabs_url = self.get_response_url('sport-tabs/16')
        sport_tabs_response = do_request(method='GET', url=sports_tabs_url)
        self.assertIn('tabs', sport_tabs_response,
                      msg=f'Expected: "tabs" is not present in Actual: "{sport_tabs_response}"')
        self.assertNotIn('sportCategories', sport_tabs_response,
                         msg=f'Expected: "tabs" is not present in Actual: "{sport_tabs_response}"')
