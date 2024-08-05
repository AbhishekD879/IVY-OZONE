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
class Test_C28861_Verify_Order_of_Suspended_SP_Selections(Common):
    """
    TR_ID: C28861
    NAME: Verify Order of Suspended 'SP' Selections
    DESCRIPTION: This test case verifies order of suspended 'SP' selections.
    DESCRIPTION: NOTE, **User Story BMA-2977**
    DESCRIPTION: For checking steps where 'runnerNumber' is NOT available for outcomes you need to create an event without enter 'runnerNumber' in TI ('Outcome' level) ![](index.php?/attachments/get/37710503)
    DESCRIPTION: NOTE: 'runnerNumber' can't be deleted for created and set outcomes
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
    PRECONDITIONS: -** 'eventStatusCode' **to see a status of event
    PRECONDITIONS: Suspension rules:
    PRECONDITIONS: if **'eventStatusCode'='S' -> **all price / odds from all markets are suspended
    PRECONDITIONS: if** ' marketStatusCode'='S' -> **all price / odds buttons within this market are suspended
    PRECONDITIONS: if **'outcomeStatusCode' = 'S'** -> one price/odds button becomes suspended
    PRECONDITIONS: if **'isStarted' = true **on event level -> all price / odds buttons become suspended (because event is started)
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

    def test_004_verify_events_with_attributes___marketstatuscodes___pricetypecodesp____outcomestatuscode__a___runnernumber_attribute_is_available_for_outcomes(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   **'marketStatusCode'='S' **
        DESCRIPTION: *   **'**priceTypeCode'='SP, '
        DESCRIPTION: *   'outcomeStatusCode' = 'A'
        DESCRIPTION: *   'runnerNumber' attribute IS available for outcomes
        EXPECTED: * All selections are greyed out within this market
        EXPECTED: * Selections are ordered by **'runnerNumber'** attribute
        EXPECTED: * Only one is greyed out button is shown next to each selection
        """
        pass

    def test_005_verify_events_with_attributes___marketstatuscodes___pricetypecodesp____outcomestatuscode_a___runnernumberis_not_available_for_outcomes(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   **'marketStatusCode'='S'**
        DESCRIPTION: *   'priceTypeCode'='SP, '
        DESCRIPTION: *   'outcomeStatusCode' = 'A'
        DESCRIPTION: *   'runnerNumber' is NOT available for outcomes
        EXPECTED: * All selections are greyed out within this market
        EXPECTED: * Selections are ordered in alphabetical in 'A-Z' order
        EXPECTED: * Only one is greyed out button is shown next to each selection
        """
        pass

    def test_006_verify_events_with_attributes___marketstatuscodes___pricetypecodesp____outcomestatuscode_a___runnernumber_is_available_for_some_outcomes_within_market_section(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   **'marketStatusCode'='S'**
        DESCRIPTION: *   priceTypeCode'='SP, '
        DESCRIPTION: *   'outcomeStatusCode' = 'A'
        DESCRIPTION: *   'runnerNumber' is available for some outcomes within market section
        EXPECTED: * All selections are greyed out within this market
        EXPECTED: * Selections are ordered in alphabetical in 'A-Z' order
        EXPECTED: * Only one is greyed out button is shown next to each selection
        """
        pass

    def test_007_verify_events_with_attributes___marketstatuscode_a___pricetypecodesp____outcomestatuscodes___runnernumber_attribute_is_available_for_outcomes(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   'marketStatusCode' = 'A'
        DESCRIPTION: *   'priceTypeCode'='SP, '
        DESCRIPTION: *   **'outcomeStatusCode'='S'**
        DESCRIPTION: *   'runnerNumber' attribute IS available for outcomes
        EXPECTED: * For suspended outcome user sees greyed out button
        EXPECTED: * Selections are ordered as in step # 4
        """
        pass

    def test_008_verify_events_with_attributes___marketstatuscode_a___pricetypecodesp____outcomestatuscodes___runnernumberattribute_is_not_available_for_outcomes(self):
        """
        DESCRIPTION: Verify events with attributes:
        DESCRIPTION: *   'marketStatusCode' = 'A'
        DESCRIPTION: *   'priceTypeCode'='SP, '
        DESCRIPTION: *   **'outcomeStatusCode'='S'**
        DESCRIPTION: *   'runnerNumber' attribute is NOT available for outcomes
        EXPECTED: * For suspended outcome user sees greyed out button
        EXPECTED: * Selections are ordered as in step # 5
        """
        pass

    def test_009_verify_eventw_with_attributes___eventstatuscodes___marketstatuscodea___outcomestatuscodea____pricetypecodessp___runnernumberattribute_is_available_for_outcomes(self):
        """
        DESCRIPTION: Verify eventw with attributes:
        DESCRIPTION: *   **'eventStatusCode'=S'**
        DESCRIPTION: *   'marketStatusCode'=A'
        DESCRIPTION: *   'outcomeStatusCode'='A' &
        DESCRIPTION: *   'priceTypeCodes'='SP'
        DESCRIPTION: *   'runnerNumber' attribute IS available for outcomes
        EXPECTED: * All selections are greyed out
        EXPECTED: * Selections are ordered as in step #4
        EXPECTED: * Only one greyed out button is shown next to each selection
        """
        pass

    def test_010_verify_eventw_with_attributes___eventstatuscodes___marketstatuscodea___outcomestatuscodea____pricetypecodessp___runnernumberattribute_is_not_available_for_outcomes(self):
        """
        DESCRIPTION: Verify eventw with attributes:
        DESCRIPTION: *   **'eventStatusCode'=S'**
        DESCRIPTION: *   'marketStatusCode'=A'
        DESCRIPTION: *   'outcomeStatusCode'='A' &
        DESCRIPTION: *   'priceTypeCodes'='SP'
        DESCRIPTION: *   'runnerNumber' attribute is NOT available for outcomes
        EXPECTED: * All selections are greyed out
        EXPECTED: * Selections are ordered as in step #5
        EXPECTED: * Only one greyed out button is shown next to each selection
        """
        pass
