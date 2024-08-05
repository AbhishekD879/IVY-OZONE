import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C9315129_Verify_Featured_tab_behavior_with_slow_network_connection(Common):
    """
    TR_ID: C9315129
    NAME: Verify Featured tab behavior with slow network connection
    DESCRIPTION: This Test Case verifies Featured tab behavior with slow network connection.
    PRECONDITIONS: * Application is launched
    PRECONDITIONS: * There are featured modules with data configured in CMS
    PRECONDITIONS: * Slow network connection (Edge/Slow 3G) is turn on in device preference
    """
    keep_browser_open = True

    def test_001_navigate_to_the_featured_tab(self):
        """
        DESCRIPTION: Navigate to the Featured tab
        EXPECTED: * Featured tab is loaded
        EXPECTED: * Featured modules are loaded
        """
        pass

    def test_002_trigger_liveserve_update_suspension_price_change_etc(self):
        """
        DESCRIPTION: Trigger LiveServe update (suspension, price change etc.)
        EXPECTED: All updates triggered during slow network connection are received in WS connection and are displayed on FE
        """
        pass

    def test_003_trigger_completionexpiration_of_the_event(self):
        """
        DESCRIPTION: Trigger completion/expiration of the event
        EXPECTED: Completed/expired event is removed from the front-end automatically
        """
        pass

    def test_004_trigger_expiration_of_the_featured_module(self):
        """
        DESCRIPTION: Trigger expiration of the Featured module
        EXPECTED: Expired Featured module is removed from the front-end automatically
        """
        pass

    def test_005_add_new_featured_module_that_is_not_present_on_current_page(self):
        """
        DESCRIPTION: Add new Featured module that is not present on current page
        EXPECTED: Featured module appears on Featured tab
        """
        pass

    def test_006_repeat_steps_2_5_for_featured_module_created_by_type_id_race_type_id_selection_id_race_grid___deprecated_enhanced_multiples(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Featured module created by:
        DESCRIPTION: * Type ID
        DESCRIPTION: * Race Type ID
        DESCRIPTION: * Selection ID
        DESCRIPTION: * Race Grid - deprecated
        DESCRIPTION: * Enhanced Multiples
        EXPECTED: 
        """
        pass
