import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60098321_Verify_Future_tab_displaying_based_on_availability_of_Future_Events(Common):
    """
    TR_ID: C60098321
    NAME: Verify 'Future' tab displaying based on availability of Future Events
    DESCRIPTION: this test case verifies 'Future' tab is shown if there are events that starts in more than 48h
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tier 1/2 Sport Landing page where 'Matches' tab is enabled in CMS (for Tier 1 'checkEvents: false' set by default and can not be edited,'checkEvents: true' is set by default for Tier 2 and can not be edited)
    PRECONDITIONS: 3. No sport modules should be created (i.e. Inplay module, Quick Links, Highlight Carousel, etc) for that sport
    PRECONDITIONS: 4. Events for the next 24h, 48h and 48h+ are created
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 3) Info about tabs displaying depends on Platforms or Tier Type could be found here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-TabsdisplayingfordifferentPlatformsandTierTypes
    PRECONDITIONS: 4) To verify Matches availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForClass/XXXXX?&simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2019-03-20T22:00:00.000Z&existsFilter=event:simpleFilter:market.dispSortName:intersects:MR&simpleFilter=event.suspendAtTime:greaterThan:2019-03-21T13:32:30.000Z&translationLang=en&count=event:market
    PRECONDITIONS: X.XX - the latest version of SS
    PRECONDITIONS: XX - Category Id
    PRECONDITIONS: XXXXX - Class Id
    """
    keep_browser_open = True

    def test_001_sport_landing_page_is_loadedmatches_tab_is_openedverify_availability_of_todaytomorrowfuture_tabs(self):
        """
        DESCRIPTION: Sport Landing Page is Loaded.
        DESCRIPTION: Matches tab is opened.
        DESCRIPTION: Verify availability of Today/Tomorrow/Future tabs
        EXPECTED: Today/Tomorrow/Future tabs are displayed. Events are present in each tab
        """
        pass

    def test_002_undisplay_all_events_that_starts_earlier_than_48h_from_now(self):
        """
        DESCRIPTION: Undisplay all events that starts earlier than 48h from now
        EXPECTED: Future tab is displayed.
        EXPECTED: Today/Tomorrow tabs are not displayed.
        """
        pass

    def test_003_display_events_that_starts_earlier_than_48h_from_now(self):
        """
        DESCRIPTION: Display events that starts earlier than 48h from now
        EXPECTED: Today/Tomorrow/Future tabs are displayed. Events are present in each tab
        """
        pass

    def test_004_undisplay_all_events_that_starts_in_more_than_48h_from_now(self):
        """
        DESCRIPTION: Undisplay all events that starts in more than 48h from now
        EXPECTED: Future tab is not displayed.
        EXPECTED: Today/Tomorrow tabs are displayed.
        """
        pass

    def test_005_display_all_events__that_starts_in_more_than_48h_from_now(self):
        """
        DESCRIPTION: Display all events  that starts in more than 48h from now
        EXPECTED: Today/Tomorrow/Future tabs are displayed. Events are present in each tab
        """
        pass
