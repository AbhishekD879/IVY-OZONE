import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C14890127_Verify_selection_information_popup(Common):
    """
    TR_ID: C14890127
    NAME: Verify selection information popup
    DESCRIPTION: This test case verifies that selection information popup is shown after tapping on selection name area in Betslip and user can navigate to appropriate EDP
    PRECONDITIONS: See designs:
    PRECONDITIONS: LADBROKES Design: https://app.zeplin.io/project/5c01259e7c06af027fe0065a?seid=5c094ae515fa11b80692dd35
    PRECONDITIONS: CORAL Design (iOS pt): https://app.zeplin.io/project/5b801d678d472e7c23e481fa?seid=5bb3885ed9bbe973da64a727
    PRECONDITIONS: CORAL Design (Web px): https://app.zeplin.io/project/5cc18478560e4a2d671900df/dashboard?seid=5cc189843cbfe30ff95478b9
    PRECONDITIONS: 1. Load app
    PRECONDITIONS: 2. Add any selection to Betslip
    PRECONDITIONS: 3. Navigate to Betslip
    PRECONDITIONS: 4. Open Dev Tools -> Network tab -> XHR filter -> find 'EventToOutcomeForOutcome' request
    PRECONDITIONS: Data for selection information popup is retrieved from the next request:
    PRECONDITIONS: https://{domain}/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForOutcome/{outcomeID}?simpleFilter=event.suspendAtTime:greaterThan:2020-01-23T14:31:00.000Z&racingForm=outcome&translationLang=en&responseFormat=json&includeRestricted=true&prune=event&prune=market
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - the last version of OB
    PRECONDITIONS: outcomeID - outcome id added to Betslip
    PRECONDITIONS: domain - valid domain URL
    """
    keep_browser_open = True

    def test_001_tap_on_selection_name_area(self):
        """
        DESCRIPTION: Tap on selection name area
        EXPECTED: * 'EventToOutcomeForOutcome' request to SS is sent to retrieve selection info
        EXPECTED: * Selection information popup is shown
        """
        pass

    def test_002_verify_that_selection_information_popup_content(self):
        """
        DESCRIPTION: Verify that selection information popup content
        EXPECTED: Selection information popup is shown with appropriate elements:
        EXPECTED: - selection name (popup header - name wraps if too long)
        EXPECTED: - event name (user can click to go to event)
        EXPECTED: - promo icons (if available: e.g. Cashout, Money back, smart boost, extra place)
        EXPECTED: - event start time
        EXPECTED: - selection name
        EXPECTED: - market name
        EXPECTED: - selection price (this is the price at the time of opening popup - no push update required in popup)
        EXPECTED: ![](index.php?/attachments/get/31106)
        EXPECTED: ![](index.php?/attachments/get/31107)
        """
        pass

    def test_003_tap_on_event_nameverify_that_edp_for_appropriate_event_is_opened(self):
        """
        DESCRIPTION: Tap on event name
        DESCRIPTION: Verify that EDP for appropriate event is opened
        EXPECTED: - Selection information popup is closed
        EXPECTED: - Event details page for the appropriate event is opened
        """
        pass

    def test_004_add_racing_selection_with_lpand_sp_price_available_to_betslip_lp_is_selectednavigate_to_betslip_and_tap_on_selection_nameverify_that_selection_information_popup_is_shown(self):
        """
        DESCRIPTION: Add racing selection with LPand SP price available to Betslip (LP is selected)
        DESCRIPTION: Navigate to Betslip and tap on selection name
        DESCRIPTION: Verify that selection information popup is shown
        EXPECTED: Selection information popup is shown with appropriate elements:
        EXPECTED: - selection name (popup header - name wraps if too long)
        EXPECTED: - time of event and event name (user can click to go to event)
        EXPECTED: - promo icons (if available: e.g. Cashout, Money back, smart boost, extra place)
        EXPECTED: - event start time
        EXPECTED: - selection name
        EXPECTED: - market name
        EXPECTED: - selection price (LP) (this is the price at the time of opening popup - no push update required in popup)
        EXPECTED: ![](index.php?/attachments/get/31289)
        """
        pass

    def test_005_change_price_for_selection_from_lp_to_sptap_on_selection_nameverify_that_sp_price_is_shown_on_selection_information_popup(self):
        """
        DESCRIPTION: Change price for selection from LP to SP
        DESCRIPTION: Tap on selection name
        DESCRIPTION: Verify that SP price is shown on selection information popup
        EXPECTED: 'Odds: SP' is shown on popup
        """
        pass

    def test_006_add_forecasttricastreverse_forecastcombinations_selections_to_betslipnavigate_to_betslip_and_tap_on_selection_nameverify_that_selection_information_popup_is_shown(self):
        """
        DESCRIPTION: Add forecast/tricast/reverse forecast/combinations selections to Betslip
        DESCRIPTION: Navigate to Betslip and tap on selection name
        DESCRIPTION: Verify that selection information popup is shown
        EXPECTED: Selection information popup is shown with appropriate elements:
        EXPECTED: - selection name (popup header - name wraps if too long)
        EXPECTED: - time of event and event name (user can click to go to event)
        EXPECTED: - promo icons (if available: e.g. Cashout, Money back, smart boost, extra place)
        EXPECTED: - event start time
        EXPECTED: - selection name
        EXPECTED: - market name
        EXPECTED: - selection price is NOT shown
        EXPECTED: ![](index.php?/attachments/get/31293)
        """
        pass
