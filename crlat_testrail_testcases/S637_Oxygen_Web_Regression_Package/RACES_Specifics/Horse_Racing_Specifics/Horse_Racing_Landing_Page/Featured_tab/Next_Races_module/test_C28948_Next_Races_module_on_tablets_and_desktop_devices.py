import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28948_Next_Races_module_on_tablets_and_desktop_devices(Common):
    """
    TR_ID: C28948
    NAME: 'Next Races' module on tablets and desktop devices
    DESCRIPTION: This test case verifies  'Next Races' module displaying on tablets and desktop devices.
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-8263 Next races Module on home page - show all selections in the race
    PRECONDITIONS: In order to get a list of **Next Races** events and check **typeflagCode**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_on_tablet_device(self):
        """
        DESCRIPTION: Load Oxygen application on Tablet device
        EXPECTED: Homepage is displayed
        """
        pass

    def test_002_go_to_next_races_module(self):
        """
        DESCRIPTION: Go to  'Next Races' module
        EXPECTED: 'Next Races' module is displayed with next elements:
        EXPECTED: *   Module header
        EXPECTED: *   Races events sections
        """
        pass

    def test_003_verify_width_of_next_races_module(self):
        """
        DESCRIPTION: Verify width of 'Next Races' module
        EXPECTED: Fixed width of 'Next Races' module is equal to 270 pixels in portrait and landscape modes
        """
        pass

    def test_004_verify_data_which_are_displayed_for_each_race(self):
        """
        DESCRIPTION: Verify data which are displayed for each race
        EXPECTED: For each race following data are displayed:
        EXPECTED: *   Race Header in format: **HH:MM EventName**
        EXPECTED: *   ALL available race selections
        EXPECTED: *   Price/Odds button with Previous Odds under it (if exist)
        EXPECTED: *   'Full Race Card' button placed after last race selection
        """
        pass

    def test_005_verify_unnamed_favorite_selections_displaying_for_race_event(self):
        """
        DESCRIPTION: Verify 'Unnamed Favorite' selections displaying for race event
        EXPECTED: 'Unnamed favorite' selections are not displayed for race event
        """
        pass

    def test_006_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * 'Horse Racing' landing page is opened
        EXPECTED: * 'Featured' tab is opened by default
        """
        pass

    def test_007_verify_selections_displaying_in_next_races_module(self):
        """
        DESCRIPTION: Verify selections displaying in 'Next Races' Module
        EXPECTED: Number of selections set in CMS is displayed for each race event
        """
        pass

    def test_008_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Greyhounds' landing page
        EXPECTED: * 'Greyhounds' landing page is opened
        EXPECTED: * 'Today' tab is opened by default
        """
        pass

    def test_009_verify_selections_displaying_in_next_races_module(self):
        """
        DESCRIPTION: Verify selections displaying in 'Next Races' module
        EXPECTED: First 4 selections are displayed for each race event
        """
        pass

    def test_010_load_oxygen_application_on_desktop_device(self):
        """
        DESCRIPTION: Load Oxygen application on desktop device
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_9(self):
        """
        DESCRIPTION: Repeat steps 2-9
        EXPECTED: 
        """
        pass
