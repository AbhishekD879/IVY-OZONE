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
class Test_C1743734_Tracking_of_clicks_on_day_switchers_when_Build_a_Racecard_is_activated_should_be_updated_in_accordance_with_changes__BMA_34002(Common):
    """
    TR_ID: C1743734
    NAME: Tracking of clicks on day switchers when 'Build a Racecard' is activated  (should be updated in accordance with changes - BMA-34002)
    DESCRIPTION: This test case verifies GA tracking of clicks on day switchers when 'Build a Racecard' is activated
    PRECONDITIONS: * Test case should be run on Desktop.
    PRECONDITIONS: * Browser console should be opened.
    PRECONDITIONS: * Horse Racing landing page is opened containing 'Build Your Own Racecard' section with text block and 'Build a Racecard' button
    PRECONDITIONS: * Day switchers on the racing grids should be available
    """
    keep_browser_open = True

    def test_001_click_on_build_a_race_card_button(self):
        """
        DESCRIPTION: Click on "Build a Race card" button
        EXPECTED: Checkboxes appear before 'Event off time' tabs
        """
        pass

    def test_002_click_on_several_day_switchers_one_after_another_on_uk__ire_race_grid(self):
        """
        DESCRIPTION: Click on several day switchers one after another on 'UK & IRE' race grid
        EXPECTED: 
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
        EXPECTED: 'eventLabel' : 'select day - << SELECTED DAY >>' //e.g. select day - saturday
        EXPECTED: })
        """
        pass

    def test_004_repeat_steps_2_3_on_international_race_grid(self):
        """
        DESCRIPTION: Repeat steps 2-3 on 'International' race grid
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_2_3_on_virtual_race_grid(self):
        """
        DESCRIPTION: Repeat steps 2-3 on 'Virtual' race grid
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'Virtual',
        EXPECTED: 'eventLabel' : 'select day - << DAY TAB >>'
        EXPECTED: })
        """
        pass
