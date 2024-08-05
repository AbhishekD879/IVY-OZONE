import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.virtual_sports
@vtest
class Test_C869700_Verify_Virtual_Sport_Page_and_List_of_Virtual_Sports_types(Common):
    """
    TR_ID: C869700
    NAME: Verify Virtual Sport Page and List of Virtual Sports types
    DESCRIPTION: This test case verifies the Virtual Sport page, list and order of Virtual Sports types
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/16231,289,288,285,286,287,290,291?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.typeId:notEquals:3048&simpleFilter=event.typeId:notEquals:3049&simpleFilter=event.typeId:notEquals:3123&simpleFilter=event.startTime:lessThanOrEqual:2016-04-18T16:28:45Z&simpleFilter=event.startTime:greaterThan:2016-04-18T09:28:45Z&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_open_virtual_sports_page(self):
        """
        DESCRIPTION: Open Virtual Sports page.
        EXPECTED: 1. The first track from CMS is displayed as default. The display order of the tracks should be as per the CMS.
        EXPECTED: 2. The 'Virtual Sports' page displayed with header contains all icons for the virtual, sorted as configured on CMS.
        """
        pass

    def test_002_verify_the_virtuals_page(self):
        """
        DESCRIPTION: Verify the Virtuals page
        EXPECTED: The page contains the following elements:
        EXPECTED: * Sport carousel
        EXPECTED: * Header with a back button and "Virtual" label
        EXPECTED: * Virtual sports icon
        EXPECTED: * Video stream window
        EXPECTED: * Live and Timer bages icons under Video stream section
        EXPECTED: * Child sports navigation
        EXPECTED: * Event selector ribbon
        EXPECTED: * Markets with price odds buttons
        EXPECTED: Designs: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa
        """
        pass

    def test_003_verify_the_list_of_virtual_sports_in_the_sport_carousel(self):
        """
        DESCRIPTION: Verify the list of Virtual Sports in the Sport carousel
        EXPECTED: The list corresponds to the list in SiteServer response
        """
        pass

    def test_004_change_order_of_parent_sports_on_cms_and_verify_on_fe(self):
        """
        DESCRIPTION: Change order of Parent Sports on CMS and verify on FE
        EXPECTED: The Parent Sports are displayed according to new CMS configuration
        """
        pass

    def test_005_change_order_of_event_sports_on_cms_and_verify_on_fe(self):
        """
        DESCRIPTION: Change order of Event Sports on CMS and verify on FE
        EXPECTED: The Child Sports are displayed according to new CMS configuration
        """
        pass

    def test_006_navigate_to_a_different_event_of_the_same_virtual_sport_using_event_selector_ribbon(self):
        """
        DESCRIPTION: Navigate to a different event of the same virtual sport using event selector ribbon
        EXPECTED: User is able to navigate to a different event of the same virtual sport
        """
        pass

    def test_007_navigate_to_a_different_virtual_sport_using_sport_carousel(self):
        """
        DESCRIPTION: Navigate to a different virtual sport using Sport carousel
        EXPECTED: User is navigated to the event of the selected virtual sport
        """
        pass
