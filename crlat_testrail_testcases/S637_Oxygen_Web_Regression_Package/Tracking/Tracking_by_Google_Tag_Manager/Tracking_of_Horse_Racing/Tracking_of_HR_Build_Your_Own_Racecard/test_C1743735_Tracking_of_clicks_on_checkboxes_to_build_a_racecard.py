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
class Test_C1743735_Tracking_of_clicks_on_checkboxes_to_build_a_racecard(Common):
    """
    TR_ID: C1743735
    NAME: Tracking of clicks on checkboxes to build a racecard
    DESCRIPTION: This test case verifies GA tracking of clicks on checkboxes to build a racecard
    PRECONDITIONS: * Test case should be run on Desktop.
    PRECONDITIONS: * Browser console should be opened.
    PRECONDITIONS: * Horse Racing landing page is opened containing 'Build Your Own Racecard' section with text block and 'Build a Racecard' button
    """
    keep_browser_open = True

    def test_001_click_on_build_a_race_card_button(self):
        """
        DESCRIPTION: Click on "Build a Race card" button
        EXPECTED: Checkboxes appear before 'Event off time' tabs
        """
        pass

    def test_002_tick_several_checkboxes(self):
        """
        DESCRIPTION: Tick several checkboxes
        EXPECTED: Selected checkboxes are checked
        """
        pass

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'build race card',
        EXPECTED: 'eventLabel' : 'select race'
        EXPECTED: })
        """
        pass

    def test_004_deselect_checkboxes(self):
        """
        DESCRIPTION: Deselect checkboxes
        EXPECTED: 
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: No events for deselecting checkboxes are created in dataLayer
        """
        pass
