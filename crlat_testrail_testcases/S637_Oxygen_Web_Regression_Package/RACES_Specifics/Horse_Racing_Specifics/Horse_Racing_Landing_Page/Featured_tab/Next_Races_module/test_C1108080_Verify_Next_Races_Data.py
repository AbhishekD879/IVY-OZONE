import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1108080_Verify_Next_Races_Data(Common):
    """
    TR_ID: C1108080
    NAME: Verify 'Next Races' Data
    DESCRIPTION: This test case is checking data which is displayed in 'Next Races' module.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) In order to control Events displaying in the Next Races Widget on the Horse Racing page
    PRECONDITIONS: Go to CMS -> System-configuration -> Structure -> NextRaces
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure, where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 2) In order to get a list of **Next Races **events check following Network response:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * <Horse Racing> landing page is opened
        EXPECTED: * 'Featured' tab is opened by default
        EXPECTED: * 'Next Races' module is displayed
        """
        pass

    def test_002_verify_next_races_module(self):
        """
        DESCRIPTION: Verify 'Next Races' module
        EXPECTED: 'Next Races' module is shown
        """
        pass

    def test_003_verify_data_in_next_races_module(self):
        """
        DESCRIPTION: Verify data in 'Next Races' module
        EXPECTED: * The next available races in terms of OpenBet event off time are shown
        EXPECTED: * Data corresponds to the Racing Post or Site Server response. See attribute **'raceName'** or **'name'** / **'title'**
        EXPECTED: * Events are sorted in the following order: the first event to start is shown first
        """
        pass

    def test_004_verify_events_which_are_displayed_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify events which are displayed in the 'Next Races' module
        EXPECTED: Events with appropriate **'typeFlagCodes'="UK, IE, INT" **are present in Next Races widget** **(*It is a CMS controlled value)*
        """
        pass

    def test_005_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: * 3 selection in the event are shown by default (*It is a CMS controlled value)*
        EXPECTED: * Only active selections are shown (**'outcomeStatusCode'**='A')
        """
        pass

    def test_006_verify_the_race_countdown_timer_module_for_the_shown_events(self):
        """
        DESCRIPTION: Verify the race countdown timer module for the shown events
        EXPECTED: The race countdown timer is displayed for race events with start time less than 45 minutes
        """
        pass

    def test_007_verify_selections_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify selections in the 'Next Races' module
        EXPECTED: Selections ONLY from 'Win or Each Way' market are displayed in the 'Next Races' module
        """
        pass

    def test_008_for_mobile_and_tabletgo_to_the_homepage___tap_next_races_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Go to the homepage -> tap 'Next Races' tab from the module selector ribbon
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 'Next Races' module is shown
        EXPECTED: Note: this is for Coral only, on Ladbrokes there is 'Next Races' tab
        """
        pass

    def test_009_for_mobile_and_tabletrepeat_steps__4___8(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Repeat steps # 4 - 8
        EXPECTED: --
        """
        pass

    def test_010_for_desktopgo_to_the_desktop_homepage___check_next_races_carousel_under_the_in_play_section(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' carousel under the 'In-Play' section
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' section is shown
        """
        pass

    def test_011_for_desktoprepeat_steps__4___8(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 4 - 8
        EXPECTED: --
        """
        pass
