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
class Test_C28863_Verify_Order_of_Suspended_LPSP_Selections(Common):
    """
    TR_ID: C28863
    NAME: Verify Order of Suspended 'LP,SP' Selections
    DESCRIPTION: This test case verifies order of suspended 'LP, SP' selections.
    PRECONDITIONS: To retrieve an information from Site Server use steps:
    PRECONDITIONS: 1) To retrieve data about particular event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL?racingForm=outcome
    PRECONDITIONS: Where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *ZZZZ - an event id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: -  **'priceTypeCodes'** to specify a type of price / odds buttons
    PRECONDITIONS: - **'outcomeStatusCode'** to see whether outcome is active or suspended
    PRECONDITIONS: - **'marketStatusCode' **to see a status of event markets
    PRECONDITIONS: -** 'eventStatusCode' **to see a status of event
    PRECONDITIONS: Suspension rules:
    PRECONDITIONS: if **'eventStatusCode'='S' -> **all price / odds from all markets are suspended
    PRECONDITIONS: if** ' marketStatusCode'='S' -> **all price / odds buttons within this market are suspended
    PRECONDITIONS: if **'outcomeStatusCode' = 'S'** -> one price/odds button becomes suspended
    PRECONDITIONS: if **'isStarted' = true **on event level -> all price / odds buttons become suspended (because event is started)
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: 
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is shown
        """
        pass

    def test_004_verify_events_with_attributes___marketstatuscodes____pricetypecodesp_lp____outcomestatuscode_a___prices_are_availabe_for_outcomes(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   **'marketStatusCode'='S' **
        DESCRIPTION: *   'priceTypeCode'='SP, LP, '
        DESCRIPTION: *   'outcomeStatusCode' = 'A'
        DESCRIPTION: *   Prices ARE availabe for outcomes
        EXPECTED: One button is displayed as greyed out for all selection within this market
        EXPECTED: Selections are ordered by rule:
        EXPECTED: *   Price in ascending order => lowest to highest
        EXPECTED: *   If prices of selections are the same -> use alphabetical order (by Horse name)
        EXPECTED: Sorting doesn't influence 'Unnamed' selections
        """
        pass

    def test_005_verify_events_with_attributes___marketstatuscodes___pricetypecodesp_lp____outcomestatuscode_a___prices_are_not_availabe_for_outcomes(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   **'marketStatusCode'='S'**
        DESCRIPTION: *   'priceTypeCode'='SP, LP, '
        DESCRIPTION: *   'outcomeStatusCode' = 'A'
        DESCRIPTION: *   Prices are NOT availabe for outcomes
        EXPECTED: Greyed out buttons are shown for all selections within this market
        EXPECTED: Selections are ordered Alphabetically in 'A-Z' order  (if runner number is not specified), in other cased they should be sorted according to the runner number
        EXPECTED: Ordering doesn't influence 'Unnamed' selections
        """
        pass

    def test_006_verify_events_with_attributes___marketstatuscode_a___pricetypecodesp_lp____outcomestatuscodes(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   'marketStatusCode' = 'A'
        DESCRIPTION: *   'priceTypeCode'='SP, LP,  '
        DESCRIPTION: *   **'outcomeStatusCode'='S'**
        EXPECTED: For suspended outcome user sees One greyed out button
        EXPECTED: Selections are ordered as per rules is steps # 4 - 5 (depending on prices availability)
        """
        pass

    def test_007_verify_event_with_attributes___eventstatuscodes____marketstatuscodea___outcomestatuscodea___pricetypecodessp_lp(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'eventStatusCode'=S' **
        DESCRIPTION: *   'marketStatusCode'=A'
        DESCRIPTION: *   'outcomeStatusCode'='A'
        DESCRIPTION: *   'priceTypeCodes'='SP, LP'
        EXPECTED: One greyed out button is shown for each selection
        EXPECTED: Selections are ordered as per rules in steps # 4 - 5 (depending on prices availability)
        """
        pass
