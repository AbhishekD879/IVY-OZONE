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
class Test_C28944_Ordering_of_Selections(Common):
    """
    TR_ID: C28944
    NAME: Ordering of Selections
    DESCRIPTION: This test case verifies how selections will be sorted in the 'Next Races' module.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&responseFormat=json&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: Horse Racing sport id =21
    PRECONDITIONS: X.XX - current supported version of OpenBet release*
    PRECONDITIONS: 2) To get a list of all "Events" for the classes use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'priceTypeCodes'** on the market level to see which rule for sorting should be applied
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_on_next_races_find_an_event_with_attribute_pricetypecodessp(self):
        """
        DESCRIPTION: On 'Next Races' find an event with attribute **'priceTypeCodes'**='SP'
        EXPECTED: Event is shown
        """
        pass

    def test_004_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: 1.  Selections are ordered by** 'runnerNumber'** attribute (if such is available for outcomes)
        EXPECTED: 2.  Selections are sorted alphabetically by **'name'** attribute (if **'runnerNumber' **is absent)
        """
        pass

    def test_005_verify_event_with_attribute_pricetypecodeslp(self):
        """
        DESCRIPTION: Verify event with attribute **'priceTypeCodes'**='LP'
        EXPECTED: The actual price/odd is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        """
        pass

    def test_006_verify_order_of_selection(self):
        """
        DESCRIPTION: Verify order of selection
        EXPECTED: 1.  Selections are ordered by odds in ascending order (lowest to highest)
        EXPECTED: 2.  If odds of selections are the same -> display alphabetically by horse name (in ascending order)
        EXPECTED: 3.  If prices are absent for selections - display alphabetically by horse name (in ascending order)
        """
        pass

    def test_007_verify_event_with_attributes___pricetypecodessp_lp___prices_are_availale_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices ARE availale for outcomes
        EXPECTED: Event is shown
        EXPECTED: One 'LP' button is shown next to each selection
        """
        pass

    def test_008_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered as per LP rule in step #6
        """
        pass

    def test_009_verify_event_with_attributes___pricetypecodessp_lp___prices_are_not_available_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices are NOT available for outcomes
        EXPECTED: * Event is shown
        EXPECTED: * 'SP' price/odds buttons are shown next to each selection
        """
        pass

    def test_010_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered alphabetically (in A-Z order) by **'name' **attribute
        """
        pass

    def test_011_for_mobile_and_tabletgo_to_the_homepage___tap_next_races_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Go to the homepage -> tap 'Next Races' tab from the module selector ribbon
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 'Next Races' module is shown
        """
        pass

    def test_012_repeat_steps__3___10(self):
        """
        DESCRIPTION: Repeat steps # 3 - 10
        EXPECTED: 
        """
        pass

    def test_013_for_desktopgo_to_the_desktop_homepage___check_next_races_section_under_the_in_play_section(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' section under the 'In-Play' section
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' section is shown
        """
        pass

    def test_014_for_desktoprepeat_steps__3___10(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 3 - 10
        EXPECTED: 
        """
        pass
