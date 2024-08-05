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
class Test_C9607583_Tracking_of_click_on_More_link_on_Next_Races_tab_on_Horse_Racing_EDP(Common):
    """
    TR_ID: C9607583
    NAME: Tracking of click on 'More' link on 'Next Races' tab on Horse Racing EDP
    DESCRIPTION: This test case verifies tracking in Google Analytic's data Layer of click on 'More' link on 'Next Races' tab on Horse Racing EDP
    PRECONDITIONS: 1. Enable 'Next Races' tab on Horse Racing EDP in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Horse Racing page and select "Next Races" tab
    """
    keep_browser_open = True

    def test_001_click_on_more_link_at_the_event_card_header(self):
        """
        DESCRIPTION: Click on 'More' link at the Event card Header
        EXPECTED: User is redirected to the event details page
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'navigation',     'eventAction' : 'next races',     'eventLabel' : Meeting Type /Time ' }
        EXPECTED: )
        """
        pass

    def test_003_navigate_back_to_horse_racing_page__next_races_tab(self):
        """
        DESCRIPTION: Navigate back to Horse Racing page > 'Next Races' tab
        EXPECTED: 
        """
        pass

    def test_004_click_on_more_link_for_another_event_card_header_again(self):
        """
        DESCRIPTION: Click on 'More' link for another Event card Header again
        EXPECTED: User is redirected to the event details page
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'navigation',     'eventAction' : 'next races',     'eventLabel' : Meeting Type /Time ' }
        EXPECTED: )
        """
        pass
