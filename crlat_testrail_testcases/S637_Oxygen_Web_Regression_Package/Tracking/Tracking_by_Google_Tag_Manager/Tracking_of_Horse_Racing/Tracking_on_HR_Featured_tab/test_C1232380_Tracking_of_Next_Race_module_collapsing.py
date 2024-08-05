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
class Test_C1232380_Tracking_of_Next_Race_module_collapsing(Common):
    """
    TR_ID: C1232380
    NAME: Tracking of Next Race module collapsing
    DESCRIPTION: This test case verifies GA tracking of "Next Race" module collapsing
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_scroll_till_next_races_module_and_collapse_ittype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Scroll till Next Races module and collapse it.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'next 4 races',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_002_expand_and_collapse_the_next_race_module_againtype_in_browser_console_datalayer_and_press_enter_verify_that_the_new_event_hasnt_been_created_in_the_data_layer(self):
        """
        DESCRIPTION: Expand and collapse the Next Race module again.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter". Verify that the new event hasn't been created in the data layer
        EXPECTED: The new events haven't been added to dataLayer
        """
        pass

    def test_003_navigate_to_the_different_page_and_come_back_to_horse_racing_landing_pagecollapse_the_next_race_module_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Navigate to the different page and come back to Horse Racing landing page.
        DESCRIPTION: Collapse the Next Race module, Type in browser console "dataLayer" and press "Enter".
        EXPECTED: One more event with the following details has been created in the data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'next 4 races',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass
