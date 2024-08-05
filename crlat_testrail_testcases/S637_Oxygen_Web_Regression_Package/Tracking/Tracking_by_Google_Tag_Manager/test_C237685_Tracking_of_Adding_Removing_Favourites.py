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
class Test_C237685_Tracking_of_Adding_Removing_Favourites(Common):
    """
    TR_ID: C237685
    NAME: Tracking of Adding/Removing Favourites
    DESCRIPTION: This Test Case verified tracking in the Google Analytic's data Layer when events are added/removed to the (from) Favourites section, on Oxygen.
    DESCRIPTION: Jira ticket: BMA-19134 Google Analytics (Blast) – Add Favourites
    DESCRIPTION: Jira ticket: BMA-19136 Google Analytics (Blast) - Remove Favourites
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        pass

    def test_003_navigate_to_the_football_landing_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: * Football Landing page
        EXPECTED: * 'Today' tab is opened by default
        """
        pass

    def test_004_add_event_to_favourites_tap_on_star_icon_near_team_names(self):
        """
        DESCRIPTION: Add Event to Favourites (tap on 'star' icon near Team Names)
        EXPECTED: * 'Star' icon is becomes bold
        EXPECTED: * The event is added to the 'Favourite Matches'
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'favourites',
        EXPECTED: 'eventAction' : 'add',
        EXPECTED: 'eventLabel' : 'favourite icon'
        EXPECTED: 'location': 'football matches'
        EXPECTED: });
        """
        pass

    def test_006_remove_event_from_the_favourites_one_more_time_tap_on_bold_star_icon_near_team_names(self):
        """
        DESCRIPTION: Remove Event from the Favourites (one more time tap on bold 'star' icon near Team Names)
        EXPECTED: * 'Star' icon becomes not filled (not selected)
        EXPECTED: * The event is removed from the 'Favourite Matches'
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'favourites',
        EXPECTED: 'eventAction' : 'remove',
        EXPECTED: 'eventLabel' : 'favourite icon'
        EXPECTED: 'location': 'betslip receipt'
        EXPECTED: });
        """
        pass

    def test_008_repeat_steps_4_7_in_the_following_pages(self):
        """
        DESCRIPTION: Repeat steps 4-7 in the following pages:
        EXPECTED: * Event Details page
        EXPECTED: * Bet Receipt
        EXPECTED: * Home
        EXPECTED: * In-play
        EXPECTED: * Football matches
        EXPECTED: * Football coupons
        EXPECTED: * Football competitions
        EXPECTED: * Football in-play
        EXPECTED: * Big Competition (e.g. World Cup)
        """
        pass

    def test_009_the_location_reply_must_be_one_of_the_following_options(self):
        """
        DESCRIPTION: The ‘location’ reply must be one of the following options:
        EXPECTED: * event page
        EXPECTED: * betslip receipt
        EXPECTED: * home
        EXPECTED: * in play
        EXPECTED: * football matches
        EXPECTED: * football coupons
        EXPECTED: * football competitions
        EXPECTED: * football in play
        EXPECTED: * world cup (configured name of big competition)
        """
        pass
