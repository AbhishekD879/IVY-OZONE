import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28489_Verify_Outright_Event_Details_Page(Common):
    """
    TR_ID: C28489
    NAME: Verify Outright Event Details Page
    DESCRIPTION: This test case verifies <Sport> Event Details Page for 'Outrights' events
    DESCRIPTION: AUTOTEST [C2536567]
    PRECONDITIONS: *   'Outright' events are present
    PRECONDITIONS: *   http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: *   See attributes:
    PRECONDITIONS: - **'name'** on event level to see event name
    PRECONDITIONS: - '**startTime' **to check event start time and event start date
    PRECONDITIONS: - **'name****' **on outcome level to check selection name
    PRECONDITIONS: - **'priceNum',** **'priceDen'**,** 'priceDec'** on outcome level to check Price/Odds buttons correctness
    PRECONDITIONS: **Note:**
    PRECONDITIONS: *   LivePrice updates are NOT applicable for Outrights
    PRECONDITIONS: *   Scores are NOT applicable for Outrights
    PRECONDITIONS: *   Please check in Sport Specifics test cases whether Outrights are displayed in 'In-Play' and 'Outrights' tabs only or in all tabs (<Sports> where all events are Outrights)
    """
    keep_browser_open = True

    def test_001_open_sport_outright_details_page(self):
        """
        DESCRIPTION: Open <Sport> Outright Details Page
        EXPECTED: Outright Details Page is opened
        """
        pass

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: *   Event name corresponds to '**name**' attribute
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the 'Back' button
        EXPECTED: **For desktop view:**
        EXPECTED: * It is displayed in the same line as 'Back' button, next to it
        EXPECTED: * Long names are truncated
        """
        pass

    def test_003_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify Event start date/time
        EXPECTED: *   Event start date corresponds to **startTime** attribute
        EXPECTED: *   Event start time is shown in following format:
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the event name
        EXPECTED: Event start time is shown in: "HH:mm, DD-MMM" - 24h format (e.g. 14:00, 28 Feb)
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed below  the market name, on the right side
        EXPECTED: Event start time is shown in: "<name of the day>, DD-MMM-YY, HH:mm AM/PM" - 12h format (e.g. Tuesday, 24-Sep-19, 11:33 AM)
        """
        pass

    def test_004_verify_live_label(self):
        """
        DESCRIPTION: Verify 'LIVE' label
        EXPECTED: 'LIVE' label is displayed if event is live now:
        EXPECTED: 1.  rawIsOffCode="Y"
        EXPECTED: 2.  rawIsOffCode="-" AND isStarted="true"
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed before the Event Start Time
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed before Event Start Time
        """
        pass

    def test_005_verify_market_sections(self):
        """
        DESCRIPTION: Verify market sections
        EXPECTED: - Market sections is displayed under event start time
        EXPECTED: - Market name should be displayed within accordion
        EXPECTED: - Accordion should be collapsible/expandable
        EXPECTED: - Chevron should be before the Name of the market
        EXPECTED: - Markets are shown based on **'dispayOrder' **attribute in ascending if more than one are available
        EXPECTED: - The first two sections are expanded by default
        EXPECTED: - Market section header corresponds to  **'name'** attribute from SS response on market level
        EXPECTED: - Market collection is NOT shown
        """
        pass

    def test_006_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is shown next to market name if cashoutAvail="Y" on market level
        """
        pass

    def test_007_verify_the_list_of_selections(self):
        """
        DESCRIPTION: Verify the list of selections
        EXPECTED: The list of selections corresponds to **'name'** attribute for each outcome for verified event
        """
        pass

    def test_008_verify_priceodds_button(self):
        """
        DESCRIPTION: Verify Price/Odds button
        EXPECTED: *   Price/Odds corresponds to the **'priceNum/priceDen' **in fraction format
        EXPECTED: *   Price/Odds corresponds to the **'priceDec'** in decimal format
        """
        pass

    def test_009_verify_ordering_of_selection(self):
        """
        DESCRIPTION: Verify ordering of selection
        EXPECTED: Selections are ordered by:
        EXPECTED: *.  **displayOrder** for each selection
        EXPECTED: *   **Price / Odds** in ascending order
        EXPECTED: *   **Alphabetically** by selection name - if prices are the same
        """
        pass
