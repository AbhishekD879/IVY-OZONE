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
class Test_C58011963_TO_BE_ARCHIVED_after_BMA_55205_release_Verify_sport_config_request_on_different_pages_across_the_app(Common):
    """
    TR_ID: C58011963
    NAME: [TO BE ARCHIVED after BMA-55205 release] Verify 'sport-config' request on different pages across the app
    DESCRIPTION: This test case verifies 'sport-config' request on different pages across the app
    DESCRIPTION: !!! TO BE ARCHIVED after BMA-55205 release
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Open dev tools > Network > XHR > find request <domain>/cms/api/ladbrokes/sport-config/<sport_category_id> e.g.
    PRECONDITIONS: https://cms-dev2.coralsports.dev.cloud.ladbrokescoral.com/cms/api/ladbrokes/sport-config/16
    PRECONDITIONS: ![](index.php?/attachments/get/99322850)
    PRECONDITIONS: **Home page config:**
    PRECONDITIONS: №1: no modules should be configured in CMS
    PRECONDITIONS: №2: 'In-play' module should be configured in CMS
    PRECONDITIONS: №3: Several featured modules, containing data from different sports should be configured; expanded by default should be set to true
    PRECONDITIONS: №4: 'In-play' module and several featured modules should be configured
    """
    keep_browser_open = True

    def test_001__navigate_to_home_page_with_config_1_from_pre_conditions_verify_sport_config_request(self):
        """
        DESCRIPTION: * Navigate to Home page with config №1 from pre-conditions
        DESCRIPTION: * Verify 'sport-config' request
        EXPECTED: Event though no modules are created, 'sport-config' request for categoryId=16 is sent (it's needed for betslip)
        """
        pass

    def test_002__navigate_to_in_play_pagetab_and_switch_between_sportsexpand_sport_accordions(self):
        """
        DESCRIPTION: * Navigate to 'In-play' page/tab and switch between sports/expand sport accordions
        EXPECTED: * 'sport-config' request for each sport category is sent on click on sports in ribbon/expanding sport accordion
        """
        pass

    def test_003_for_mobiletablet_navigate_to_home_page_with_config_2_from_pre_conditions_verify_sport_config_request(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Navigate to Home page with config №2 from pre-conditions
        DESCRIPTION: * Verify 'sport-config' request
        EXPECTED: * 'sport-config' request for categoryId=16 is sent
        EXPECTED: * 'sport-config' request with multiple category IDs is sent (i.e. only those sport category IDs that are displayed within 'In-play' module)
        EXPECTED: ![](index.php?/attachments/get/99442011)
        """
        pass

    def test_004__navigate_to_home_page_with_config_3_from_pre_conditions_verify_sport_config_request(self):
        """
        DESCRIPTION: * Navigate to Home page with config №3 from pre-conditions
        DESCRIPTION: * Verify 'sport-config' request
        EXPECTED: * 'sport-config' request for categoryId=16 is sent
        EXPECTED: * separate 'sport-config' requests are sent for each sport category in Featured modules
        """
        pass

    def test_005_for_mobiletablet_navigate_to_home_page_with_config_4_from_pre_conditions_verify_sport_config_request(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Navigate to Home page with config №4 from pre-conditions
        DESCRIPTION: * Verify 'sport-config' request
        EXPECTED: * 'sport-config' request for categoryId=16 is sent
        EXPECTED: * 'sport-config' request with multiple category IDs is sent (i.e. only those sport category IDs that are displayed in 'In-play' module)
        EXPECTED: * separate 'sport-config' requests are sent for each unique sport category in Featured modules
        """
        pass

    def test_006__navigate_to_any_sport_landing_page_verify_sport_config_request(self):
        """
        DESCRIPTION: * Navigate to any sport landing page
        DESCRIPTION: * Verify 'sport-config' request
        EXPECTED: * 'sport-config' request for respective sport category is sent
        """
        pass
