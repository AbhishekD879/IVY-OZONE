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
class Test_C1743732_Tracking_of_click_on_Exit_builder_Close_button(Common):
    """
    TR_ID: C1743732
    NAME: Tracking of click on 'Exit builder/Close' button
    DESCRIPTION: This test case verifies GA tracking of clicks on 'Exit Builder/Close' button ('Build Your Own Racecard' section)
    PRECONDITIONS: * Test case should be run on Desktop.
    PRECONDITIONS: * Browser console should be opened.
    PRECONDITIONS: * Horse Racing landing page is opened containing 'Build Your Own Racecard' section with text block and 'Build a Racecard' button
    """
    keep_browser_open = True

    def test_001_click_on_build_a_racecard_button_at_the_build_your_own_racecard_section(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button at the 'Build Your Own Racecard' section
        EXPECTED: 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        """
        pass

    def test_002_click_on_exit_builder_button(self):
        """
        DESCRIPTION: Click on "Exit builder" button
        EXPECTED: 'Exit Builder' is replaced by 'Build a Racecard' button
        """
        pass

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'build race card',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        """
        pass

    def test_004_repeat_steps_1(self):
        """
        DESCRIPTION: Repeat steps 1
        EXPECTED: 
        """
        pass

    def test_005_click_on_close_icon_next_to_exit_builder(self):
        """
        DESCRIPTION: Click on 'Close' icon next to 'Exit Builder'
        EXPECTED: 'Exit Builder' is replaced by 'Build a Racecard' button
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'build race card',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        """
        pass
