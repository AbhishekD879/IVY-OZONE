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
class Test_C1232396_Tracking_of_click_on_the_day_tab_inside_the_race_grids(Common):
    """
    TR_ID: C1232396
    NAME: Tracking of click on the day tab inside the race grids
    DESCRIPTION: This test case verifies GA tracking of day tabs click on the UK & IRE, International, Virtuals race grids
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Day tabs on the racing grids should be available. If there is only one tab, create additional tabs in TI:
    PRECONDITIONS: 1. Navigate to categoty Horse Racing (id =21) > class Horse Racing - Live
    PRECONDITIONS: 2. The type should have one of the following check boxes selected: UK, IRE, Is International or Virtual Racing in order to appear in  UK&IRE, International, Virtual grids
    PRECONDITIONS: 3. Open the event under the type and set a start time date matching the day of the week to display on a day tab
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_scroll_till_the_uk__ire_race_grid_click_on_the_several_day_tabs_one_after_anothertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Scroll till the UK & IRE race grid. Click on the several day tabs one after another.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'UK & IRE',
        EXPECTED: 'eventLabel' : 'select day - << DAY TAB >>'
        EXPECTED: })
        """
        pass

    def test_002_scroll_till_the_international_race_grideg_france_south_africa_other_international_etc_click_on_the_several_day_tabs_one_after_anothertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Scroll till the International race grid(e.g. France, South Africa, Other International etc). Click on the several day tabs one after another.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : <Module name>(e.g. France, South Africa etc),
        EXPECTED: 'eventLabel' : 'select day - << DAY TAB >>'
        EXPECTED: })
        """
        pass

    def test_003_scroll_till_the_virtual_race_grid_click_on_the_several_day_tabs_one_after_anothertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Scroll till the Virtual race grid. Click on the several day tabs one after another.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'Virtual',
        EXPECTED: 'eventLabel' : 'select day - << DAY TAB >>'
        EXPECTED: })
        """
        pass
