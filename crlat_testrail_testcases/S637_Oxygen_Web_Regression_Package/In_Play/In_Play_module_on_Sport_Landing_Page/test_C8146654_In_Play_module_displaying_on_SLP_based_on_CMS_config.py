import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C8146654_In_Play_module_displaying_on_SLP_based_on_CMS_config(Common):
    """
    TR_ID: C8146654
    NAME: 'In-Play' module displaying on SLP based on CMS config
    DESCRIPTION: This test case verifies whether 'In-Play' module is displayed on <Sport> Landing page, depending on CMS config
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: - 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: - 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: - 'In-play' module is set to 'Active'
    PRECONDITIONS: - 'Inplay event count' is set to any digit e.g. 10
    PRECONDITIONS: 2) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: 3) To check data regarding In-Play module, open Dev Tools->Network->WS > featured-sports
    PRECONDITIONS: 1. Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: 2. Open 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_in_play_module_availability(self):
        """
        DESCRIPTION: Verify 'In-play' module availability
        EXPECTED: 'In-play' module with live events is displayed on 'Matches' tab
        """
        pass

    def test_002__in_cms_set_in_play_module_to_inactive_cms__sports_pages__sport_categories__specific_sport_eg_footbal_in_application_do_not_refresh_the_page_and_verify_in_play_module_availability(self):
        """
        DESCRIPTION: * In CMS set 'In-Play' module to 'Inactive' (CMS > Sports Pages > Sport Categories > specific sport e.g. Footbal)
        DESCRIPTION: * In application DO NOT refresh the page and verify 'In-Play' module availability
        EXPECTED: * 'In-play' module is NOT displayed on 'Matches' tab
        EXPECTED: * FEATURED_STRUCTURE_CHANGED is received in websocket not containing Inplay module
        """
        pass

    def test_003__in_cms_set_in_play_module_to_active_cms__sports_pages__sport_categories__specific_sport_eg_footbal_in_cms_disable_in_play_module_cms__system_configuration__structure__inplay_module_in_application_refresh_the_page_and_verify_in_play_module_availability(self):
        """
        DESCRIPTION: * In CMS set 'In-Play' module to 'Active' (CMS > Sports Pages > Sport Categories > specific sport e.g. Footbal)
        DESCRIPTION: * In CMS disable 'In-Play' module (CMS > System Configuration > Structure > Inplay Module)
        DESCRIPTION: * In application refresh the page and verify 'In-Play' module availability
        EXPECTED: 'In-play' module is NOT displayed on 'Matches' tab
        """
        pass
