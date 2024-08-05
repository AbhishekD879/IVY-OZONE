import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
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
    keep_browser_open = True

    def test_001__load_application_find_initial_data_response_for_sportcategories_in_devtools(self):
        """
        DESCRIPTION: * Load application
        DESCRIPTION: * Find **initial-data** response for sportCategories in devTools
        EXPECTED: sportCategories tab is present with all existing sport categories in devTools
        """
        pass

    def test_002_expand_any_available_sport_category_gt_sportconfig_gt_config(self):
        """
        DESCRIPTION: Expand any available sport category &gt; sportConfig &gt; config
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
        pass

    def test_003_navigate_to_some_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to some Sport Landing Page
        EXPECTED: * 'sport-config/%categoryID%' request is sent
        EXPECTED: * response of the request does not include information from initial-data response
        EXPECTED: * only tabs data is present (including time filters if available):
        EXPECTED: ![](index.php?/attachments/get/122019625)
        """
        pass
