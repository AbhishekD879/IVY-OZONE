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
class Test_C360236_Verify_Market_Selector_Tracking(Common):
    """
    TR_ID: C360236
    NAME: Verify Market Selector Tracking
    DESCRIPTION: This test case verifies Market Selector Tracking
    PRECONDITIONS: Dev Tools -> Console should be opened
    PRECONDITIONS: *Note:*
    PRECONDITIONS: MARKET NAME - This is what market the customer sees and selects on site
    PRECONDITIONS: OPENBET CATEGORY ID - This is the Sport on which the market selector was used. Will always be football for now.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_football_landing_page(self):
        """
        DESCRIPTION: Go to Football Landing page
        EXPECTED: - Football Landing page is opened
        EXPECTED: - Default market is displayed in Market Selector
        """
        pass

    def test_003_choose_any_other_item_from_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Choose any other item from Market Selector dropdown list
        EXPECTED: The events for selected market are shown on the page
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'market selector',
        EXPECTED: 'eventAction' : 'change market',
        EXPECTED: 'eventLabel' : '<< MARKET NAME >>',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>'
        EXPECTED: });
        """
        pass

    def test_005_repeat_step_3_for_each_item_from_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Repeat step 3 for each item from Market Selector dropdown list
        EXPECTED: The events for selected market are shown on the page
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter_after_each_item_selection(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter' after each item selection
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'market selector',
        EXPECTED: 'eventAction' : 'change market',
        EXPECTED: 'eventLabel' : '<< MARKET NAME >>',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>'
        EXPECTED: });
        """
        pass

    def test_007_choose_in_play_tab_on_football_landing_page(self):
        """
        DESCRIPTION: Choose In-Play tab on Football Landing page
        EXPECTED: * In-Play page is opened
        EXPECTED: * Live Now filter is selected by default
        EXPECTED: * Default market is displayed in Market Selector
        """
        pass

    def test_008_repeat_step_3_for_each_item_from_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Repeat step 3 for each item from Market Selector dropdown list
        EXPECTED: The events for selected market are shown on the page
        """
        pass

    def test_009_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'market selector',
        EXPECTED: 'eventAction' : 'change market',
        EXPECTED: 'eventLabel' : '<< MARKET NAME >>',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>'
        EXPECTED: });
        """
        pass

    def test_010_choose_competitions_tab_on_football_landing_page(self):
        """
        DESCRIPTION: Choose Competitions tab on Football Landing page
        EXPECTED: List of sub-categories (Class ID's) is loaded
        """
        pass

    def test_011_clicktap_on_sub_category_class_id_with_type_ids(self):
        """
        DESCRIPTION: Click/Tap on sub-category (Class ID) with Type ID's
        EXPECTED: List of Competitions (Type ID) is displayed
        """
        pass

    def test_012_choose_competition_type_id(self):
        """
        DESCRIPTION: Choose Competition (Type ID)
        EXPECTED: * List of Events is displayed
        EXPECTED: * The ‘Market Selector’ displayed within opened by default Matches section below the First level accordion
        EXPECTED: * 'Default market is displayed in Market Selector
        """
        pass

    def test_013_repeat_step_3_for_each_item_from_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Repeat step 3 for each item from Market Selector dropdown list
        EXPECTED: The events for selected market are shown on the page
        """
        pass

    def test_014_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'market selector',
        EXPECTED: 'eventAction' : 'change market',
        EXPECTED: 'eventLabel' : '<< MARKET NAME >>',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>'
        EXPECTED: });
        """
        pass

    def test_015_tap_in_play_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * 'All Sports' tab is opened by default and underlined by red line
        EXPECTED: * 'Live Now' filter is selected by default
        """
        pass

    def test_016_tap_on_football_icon_on_ribbon(self):
        """
        DESCRIPTION: Tap on 'Football' icon on Ribbon
        EXPECTED: * 'Football' Page is opened
        EXPECTED: * 'Football' tab is selected and underlined by red line
        EXPECTED: * 'Live Now' filter is selected by default
        EXPECTED: * The 'Market Selector' displayed below the 'Live Now'/'Upcoming' switcher and above the First accordion on the page
        EXPECTED: * Default market is displayed in Market Selector
        """
        pass

    def test_017_repeat_step_3_for_each_item_from_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Repeat step 3 for each item from Market Selector dropdown list
        EXPECTED: The events for selected market are shown on the page
        """
        pass

    def test_018_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'market selector',
        EXPECTED: 'eventAction' : 'change market',
        EXPECTED: 'eventLabel' : '<< MARKET NAME >>',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>'
        EXPECTED: });
        """
        pass
