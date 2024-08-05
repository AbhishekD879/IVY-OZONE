import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1232399_Tracking_of_race_grids_collapsing_should_be_updated_in_accordance_with_changes__BMA_34002(Common):
    """
    TR_ID: C1232399
    NAME: Tracking of race grids collapsing (should be updated in accordance with changes - BMA-34002)
    DESCRIPTION: This test case verifies GA tracking of UK & IRE, International, Virtuals race grids collapsing
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_collapse_uk__ire_grid_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Collapse "UK & IRE" grid. Type in browser console "dataLayer" and press "Enter"
        EXPECTED: An event with the following details has been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'UK & IRE',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_002_collapse_international_grid_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Collapse "International" grid. Type in browser console "dataLayer" and press "Enter"
        EXPECTED: An event with the following details has been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'International',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_003_collapse_virtual_grid_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Collapse "Virtual" grid. Type in browser console "dataLayer" and press "Enter"
        EXPECTED: An event with the following details has been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'Virtual',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_004_expand_and_collapse_all_3_grids_once_more_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Expand and collapse all 3 grids once more. Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The new events hadn't been created in dataLayer
        """
        pass

    def test_005_navigate_to_the_different_page_and_come_back_to_horse_race_pagerepeat_steps_1_3(self):
        """
        DESCRIPTION: Navigate to the different page and come back to Horse Race page.
        DESCRIPTION: Repeat steps 1-3
        EXPECTED: A relevant event is created after collapsing each grid
        """
        pass
