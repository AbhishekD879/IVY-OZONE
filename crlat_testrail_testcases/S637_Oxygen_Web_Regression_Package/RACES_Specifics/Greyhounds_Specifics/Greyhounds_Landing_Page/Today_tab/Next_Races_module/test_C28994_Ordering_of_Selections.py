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
class Test_C28994_Ordering_of_Selections(Common):
    """
    TR_ID: C28994
    NAME: Ordering of Selections
    DESCRIPTION: This test case verifies how selections will be ordered on the 'Next Races' module
    DESCRIPTION: Jira ticket: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:19&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Greyhound category id =19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of all 'Events' for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: *YYYY is a comma separated list of Class ID's e.g. 97 or 97, 98*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) To retrieve information about event outcomes and silks info etc use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?racingForm=outcome&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *ZZZZ is an **'event id'** which is taken from the link in step 2*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'priceTypeCodes'** on the market level to see which rule for sorting should be applied
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: 'Greyhounds' landing page is opened
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
        EXPECTED: 1.  Selections are ordered by** 'runnerNumber'** attribute (if such is available for outcomes)
        EXPECTED: 2.  Selections are sorted alphabetically by 'name' attribute (if **'runnerNumber' **is absent)
        """
        pass

    def test_005_verify_event_with_attribute_pricetypecodeslp(self):
        """
        DESCRIPTION: Verify event with attribute **'priceTypeCodes'**='LP'
        EXPECTED: Event is shown
        """
        pass

    def test_006_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: 1.
        EXPECTED: Selections are ordered by odds in ascending order (lowest to highest)
        EXPECTED: 2.
        EXPECTED: If odds of selections are the same -> display alphabetically by horse name (in ascending order)
        EXPECTED: 3.
        EXPECTED: If prices are absent for selections - > display alphabetically by horse name (in ascending order)
        """
        pass

    def test_007_verify_event_with_attributes___pricetypecodessp_lp___prices_are_availale_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices ARE availale for outcomes
        EXPECTED: Event is shown
        """
        pass

    def test_008_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: 1.  Only 'LP' buttons are displayed
        EXPECTED: 2.  Selections are ordered as per LP rule (see step #6)
        """
        pass

    def test_009_verify_event_with_attributes___pricetypecodessp_lp___prices_are_not_available_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices are NOT available for outcomes
        EXPECTED: Event is shown
        EXPECTED: Only one 'SP' button is shown
        """
        pass

    def test_010_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered alphabetically (A-Z order) by** 'name' **attribute
        """
        pass
