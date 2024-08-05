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
class Test_C58011962_TO_BE_ARCHIVED_after_BMA_55205_release_Verify_sport_config_JSON_response(Common):
    """
    TR_ID: C58011962
    NAME: [TO BE ARCHIVED after BMA-55205 release] Verify 'sport-config' JSON response
    DESCRIPTION: This test case verifies:
    DESCRIPTION: - 'sport-config' JSON response when navigating to any Sport Landing page
    DESCRIPTION: - there's no 'sport-config' JSON for Untied sport category
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to any sport landing page e.g. Football
    PRECONDITIONS: 3. Open dev tools > Network > XHR > find request <domain>/cms/api/ladbrokes/sport-config/<sport_category_id> e.g.
    PRECONDITIONS: https://cms-dev2.coralsports.dev.cloud.ladbrokescoral.com/cms/api/ladbrokes/sport-config/16
    PRECONDITIONS: ![](index.php?/attachments/get/99322850)
    PRECONDITIONS: **NOTE!**
    PRECONDITIONS: - Values in 'sport-config' JSON response should correspond to CMS > Sports Pages > Sport Categories > select specific sport category e.g. Football
    PRECONDITIONS: - To have sports configured correctly, the following things should be set:
    PRECONDITIONS: - **isOutrightSport** - true should be set for the following **Outright sports**: {CYCLING, FORMULA_1, GOLF, MOTOR_BIKES, MOTOR_SPORTS, MOVIES, POLITICS, MOTOR_SPEEDWAY, TV_SPECIALS}"
    PRECONDITIONS: - **isMultiTemplateSport** - true should be set for: {CRICKET, DARTS, HOCKEY, RUGBY_UNION}
    """
    keep_browser_open = True

    def test_001_verify_structure_of_sport_config_json_response(self):
        """
        DESCRIPTION: Verify structure of 'sport-config' JSON response
        EXPECTED: 'sport-config' JSON response consists of 'config' and 'tabs' arrays
        """
        pass

    def test_002_verify_config_array(self):
        """
        DESCRIPTION: Verify 'config' array
        EXPECTED: 'config' array consists of 'request' and 'tabs' sub-arrays and the following properties:
        EXPECTED: * 'title'- value from 'Title' field in CMS
        EXPECTED: * 'name'- last segment from Target URI without specific symbols e.g. "beachvolleyball"
        EXPECTED: * 'path'- last Target URI segment e.g. "beach-volleyball"
        EXPECTED: * 'tier'- numeric value (e.x. 1, 2)
        EXPECTED: * 'categoryType' - always "gaming" for sports (value NOT from CMS)
        EXPECTED: * 'isOutrightSport' - true/false
        EXPECTED: * 'isMultiTemplateSport' - true/false
        EXPECTED: * 'oddsCardHeaderType' - value from respective field in CMS
        """
        pass

    def test_003_verify_configrequest_array(self):
        """
        DESCRIPTION: Verify 'config.request' array
        EXPECTED: 'config.request' array consists of the following properties:
        EXPECTED: * 'categoryID' - value from respective field in CMS
        EXPECTED: * 'siteChannels' - value NOT from CMS
        EXPECTED: * 'marketsCount'- true/false ("boolean: == !isOutrightSport")
        EXPECTED: * 'isActive'- true/false ("boolean: == isOutrightSport")
        EXPECTED: * 'dispSortName' - value from 'Disp sort name' in CMS
        EXPECTED: * 'dispSortNameIncludeOnly' - value from 'Disp sort name' in CMS
        EXPECTED: * 'typeIds'- value from respective field in CMS
        EXPECTED: * 'marketTemplateMarketNameIntersects'- value from 'Primary markets' field in CMS
        """
        pass

    def test_004_verify_configtabs_array(self):
        """
        DESCRIPTION: Verify 'config.tabs' array
        EXPECTED: 'config.tabs' array consists of the following properties:
        EXPECTED: * 'live'{}
        EXPECTED: * 'coupons':
        EXPECTED: { "date": "today",
        EXPECTED: "isActive": true}
        EXPECTED: * 'today':
        EXPECTED: { "isNotStarted": true,
        EXPECTED: "templateMarketNameOnlyIntersects": true if football / else - null"},
        EXPECTED: * 'tomorrow':
        EXPECTED: {"templateMarketNameOnlyIntersects": true if football / else - null}
        EXPECTED: * 'future':
        EXPECTED: {"templateMarketNameOnlyIntersects": true if football / else - null"}
        EXPECTED: * 'outrights':
        EXPECTED: {"isActive": true,
        EXPECTED: "marketsCount": false}
        EXPECTED: * 'upcoming:
        EXPECTED: { "_comment": "only for football",
        EXPECTED: "isNotStarted": true}
        EXPECTED: * 'specials':
        EXPECTED: {"_comment": "only for football",
        EXPECTED: "marketsCount": false,
        EXPECTED: "marketDrilldownTagNamesContains": "MKTFLAG_SP"}
        EXPECTED: * 'jackpot': only for football
        EXPECTED: * 'results': only for football
        """
        pass

    def test_005_verify_tabs_array(self):
        """
        DESCRIPTION: Verify 'tabs' array
        EXPECTED: 'tabs' array consists of the list of tabs with the following properties:
        EXPECTED: * 'id' e.g. "tab-matches"
        EXPECTED: * 'name' - value from 'Tab Name' field in CMS
        EXPECTED: * 'label' - value from 'Tab Display Name' field in CMS
        EXPECTED: * 'url' - e.g. "/sport/football/matches"
        EXPECTED: * 'hidden' - true/false
        EXPECTED: * 'sortOrder' - numeric value (e.x. 0, 1, 2)
        """
        pass

    def test_006__navigate_to_any_untied_sport_category_verify_presence_of_sport_config_request(self):
        """
        DESCRIPTION: * Navigate to any Untied sport category
        DESCRIPTION: * Verify presence of 'sport-config' request
        EXPECTED: 'sport-config' request is not sent
        """
        pass
