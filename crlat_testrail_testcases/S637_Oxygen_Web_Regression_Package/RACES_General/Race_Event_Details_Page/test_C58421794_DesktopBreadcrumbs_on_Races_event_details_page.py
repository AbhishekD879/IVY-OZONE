import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C58421794_DesktopBreadcrumbs_on_Races_event_details_page(Common):
    """
    TR_ID: C58421794
    NAME: [Desktop]Breadcrumbs on <Races> event details page
    DESCRIPTION: This test case verifies breadcrumbs on Horse Racing event details page.
    PRECONDITIONS: 1. Race with '-' in the name should be created
    PRECONDITIONS: 2. App is loaded
    """
    keep_browser_open = True

    def test_001___open_horse_racing_landing_page_and_click_on_any_event__verify_breadcrumbs(self):
        """
        DESCRIPTION: - Open Horse Racing landing page and click on any event.
        DESCRIPTION: - Verify breadcrumbs
        EXPECTED: - Breadcrumbs are located below the page header
        EXPECTED: - Type and Race name should be the same as set in TI. No characters should be missed.
        EXPECTED: ![](index.php?/attachments/get/101706628)
        """
        pass

    def test_002_repeat_previous_step_for__next_races_tab__next_races_module__future_tab__greyhound_tabs(self):
        """
        DESCRIPTION: Repeat previous step for:
        DESCRIPTION: - 'Next Races' tab
        DESCRIPTION: - 'Next Races' module
        DESCRIPTION: - 'Future' tab
        DESCRIPTION: - 'Greyhound' tabs.
        EXPECTED: 
        """
        pass
