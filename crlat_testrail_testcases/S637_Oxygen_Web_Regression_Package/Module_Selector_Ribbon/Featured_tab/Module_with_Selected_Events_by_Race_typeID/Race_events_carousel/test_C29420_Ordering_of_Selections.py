import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29420_Ordering_of_Selections(Common):
    """
    TR_ID: C29420
    NAME: Ordering of Selections
    DESCRIPTION: This test case verifies how selections will be sorted in the <Race> events carousel
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'priceTypeCodes'** on the market level to see which rule for sorting should be applied
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletgo_to_module_selector_ribbon__gt_module_created_by_ltracegt_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -&gt; Module created by &lt;Race&gt; type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by &lt;Race&gt; type ID is shown
        """
        pass

    def test_003_for_desktopscroll_the_page_down_to_featured_section__gt_gt_module_created_by_ltracegt_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section -&gt;-&gt; Module created by &lt;Race&gt; type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by &lt;Race&gt; type ID is shown
        """
        pass

    def test_004_on_ltracegt_events_carousel_find_an_event_with_attribute_pricetypecodessp(self):
        """
        DESCRIPTION: On &lt;Race&gt; events carousel find an event with attribute **'priceTypeCodes'**='SP'
        EXPECTED: Event is shown
        """
        pass

    def test_005_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: 1.  Selections are ordered by** 'runnerNumber'** attribute (if such is available for outcomes)
        EXPECTED: 2.  Selections are sorted alphabetically by **'name'** attribute (if **'runnerNumber' **is absent)
        """
        pass

    def test_006_verify_event_with_attribute_pricetypecodeslp(self):
        """
        DESCRIPTION: Verify event with attribute **'priceTypeCodes'**='LP'
        EXPECTED: The actual price/odd is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        """
        pass

    def test_007_verify_order_of_selection(self):
        """
        DESCRIPTION: Verify order of selection
        EXPECTED: 1.
        EXPECTED: Selections are ordered by odds in ascending order (lowest to highest)
        EXPECTED: 2.
        EXPECTED: If odds of selections are the same -&gt; display alphabetically by horse name (in ascending order)
        EXPECTED: 3.
        EXPECTED: If prices are absent for selections - display alphabetically by horse name (in ascending order)
        """
        pass

    def test_008_verify_event_with_attributes___pricetypecodessp_lp___prices_are_availale_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices ARE availale for outcomes
        EXPECTED: Event is shown
        EXPECTED: One 'LP' button is shown next to each selection
        """
        pass

    def test_009_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered as per LP rule in step #6
        """
        pass

    def test_010_verify_event_with_attributes___pricetypecodessp_lp___prices_are_not_available_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices are NOT available for outcomes
        EXPECTED: Event is shown
        EXPECTED: Only one 'SP' button is shown
        """
        pass

    def test_011_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered alphabetically (in A-Z order) by **'name' **attribute
        """
        pass
