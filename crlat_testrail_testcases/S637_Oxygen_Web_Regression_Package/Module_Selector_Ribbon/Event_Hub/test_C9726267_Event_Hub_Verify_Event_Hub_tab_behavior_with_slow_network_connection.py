import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726267_Event_Hub_Verify_Event_Hub_tab_behavior_with_slow_network_connection(Common):
    """
    TR_ID: C9726267
    NAME: Event Hub: Verify Event Hub tab behavior with slow network connection
    DESCRIPTION: This Test Case verifies Event Hub tab behavior with slow network connection.
    PRECONDITIONS: * Application is launched
    PRECONDITIONS: * There is Event Hub with modules with data configured in CMS
    PRECONDITIONS: * Slow network connection (Edge/Slow 3G) is turn on in device preference
    """
    keep_browser_open = True

    def test_001_navigate_to_the_event_hub_tab(self):
        """
        DESCRIPTION: Navigate to the Event Hub tab
        EXPECTED: * Event Hub tab is loaded
        EXPECTED: * Modules are loaded
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

    def test_004_trigger_expiration_of_the_module(self):
        """
        DESCRIPTION: Trigger expiration of the Module
        EXPECTED: Expired Module is removed from the front-end automatically
        """
        pass

    def test_005_add_new_module_that_is_not_present_on_current_page(self):
        """
        DESCRIPTION: Add new Module that is not present on current page
        EXPECTED: Module appears on Event Hub tab
        """
        pass

    def test_006_repeat_steps_2_5_for_module_created_by_type_id_race_type_id_selection_id_race_grid_enhanced_multiples_quick_links_highlights_carousel_surface_bets(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Module created by:
        DESCRIPTION: * Type ID
        DESCRIPTION: * Race Type ID
        DESCRIPTION: * Selection ID
        DESCRIPTION: * Race Grid
        DESCRIPTION: * Enhanced Multiples
        DESCRIPTION: * Quick links
        DESCRIPTION: * Highlights carousel
        DESCRIPTION: * Surface bets
        EXPECTED: 
        """
        pass
