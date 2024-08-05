import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C59549184_Verify_5_A_Side_BYB_tabs_handling_when_user_is_on_EDP_and_event_goes_Live(Common):
    """
    TR_ID: C59549184
    NAME: Verify 5-A-Side/BYB tabs handling when user is on EDP and event goes Live
    DESCRIPTION: This TC verifies that 5-A-Side/BYB tabs disappear and user is redirected to All Markets tab when event goes live
    PRECONDITIONS: 5-A-Side/BYB event
    """
    keep_browser_open = True

    def test_001_navigate_to_any_tab_except_5_a_sidebyb_edp_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to any tab (except 5-A-Side/BYB) EDP of event from preconditions
        EXPECTED: User is on EDP
        """
        pass

    def test_002_trigger_push_update_from_ti_event_should_become_live(self):
        """
        DESCRIPTION: Trigger Push update from TI (Event should become Live)
        EXPECTED: - Live Push update is received on UI
        EXPECTED: - 5-A-Side/BYB tabs disappeared from EDP
        """
        pass

    def test_003___update_event_in_ti_make_it_pre_match_again__reload_page_and_navigate_to_5_a_sidebyb_tab(self):
        """
        DESCRIPTION: - Update event in TI (make it pre-match again)
        DESCRIPTION: - Reload page and navigate to 5-A-Side/BYB tab
        EXPECTED: User is on 5-A-Side/BYB tab
        """
        pass

    def test_004_trigger_push_update_from_ti_event_should_become_live(self):
        """
        DESCRIPTION: Trigger Push update from TI (Event should become Live)
        EXPECTED: - Live Push update is received on UI
        EXPECTED: - User is redirected to All Markets tab
        EXPECTED: - 5-A-Side/BYB tabs disappeared(not shown on EDP)
        """
        pass

    def test_005___update_event_in_ti_make_it_pre_match_again__reload_page_and_navigate_to_5_a_sidebyb_tab__add_some_selection_to_byb_dashboard_or_5_a_side_pitch_view(self):
        """
        DESCRIPTION: - Update event in TI (make it pre-match again)
        DESCRIPTION: - Reload page and navigate to 5-A-Side/BYB tab
        DESCRIPTION: - Add some selection to BYB dashboard or 5-A-Side pitch view
        EXPECTED: - User is on 5-A-Side/BYB tab
        EXPECTED: - Selections are added to BYB dashboard/ 5-A-Side pitch view
        """
        pass

    def test_006_trigger_push_update_from_ti_event_should_become_live(self):
        """
        DESCRIPTION: Trigger Push update from TI (Event should become Live)
        EXPECTED: - Live Push update is received on UI
        EXPECTED: - User is redirected to All Markets tab
        EXPECTED: - 5-A-Side/BYB tabs disappeared(not shown on EDP)
        """
        pass
