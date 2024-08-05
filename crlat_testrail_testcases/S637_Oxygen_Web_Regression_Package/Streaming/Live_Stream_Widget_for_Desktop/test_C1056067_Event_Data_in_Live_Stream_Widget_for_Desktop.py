import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C1056067_Event_Data_in_Live_Stream_Widget_for_Desktop(Common):
    """
    TR_ID: C1056067
    NAME: Event Data in 'Live Stream' Widget for Desktop
    DESCRIPTION: This test case verifies event data in 'Live Stream' widget for Desktop
    PRECONDITIONS: 1) User is logged in
    PRECONDITIONS: 2) Live Stream is mapped
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1) To get information about event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/xxxx?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * x.xx latest supported SiteServer version
    PRECONDITIONS: * xxxx event id
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: **startTime** attribute - to see start time of event
    PRECONDITIONS: 2) For each **Class **retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?translationLang=LL
    PRECONDITIONS: *   XXX -  comma separated list of **Class **ID's
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: *   **'name'** to define event name
    PRECONDITIONS: *   **'drilldownTagNames'** to determine WHICH stream provider has been mapped to the event
    PRECONDITIONS: **'drilldownTagNames'**** ***Streaming flags are:*
    PRECONDITIONS: 1.  *EVFLAG_IVM -  IMG Video Mapped for this event*
    PRECONDITIONS: 2.  *EVFLAG_PVM - Perform Video Mapped for this event*
    PRECONDITIONS: 3.  *EVFLAG_AVA - At The Races stream available*
    PRECONDITIONS: 4.  *EVFLAG_RVA - RacingUK stream available*
    PRECONDITIONS: 5.  *EVFLAG_RPM - RPGTV Greyhound streaming Mapped*
    PRECONDITIONS: 6.  *EVFLAG_GVM - IGameMedia streaming Mapped*
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sport_landing_page_where_live_streaming_is_mapped(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page where live streaming is mapped
        EXPECTED: * <Sport> Landing page is opened
        EXPECTED: * 'Matches' tab is opened by default
        EXPECTED: * Live Stream widget is present in the Main view column 2
        EXPECTED: * Live Stream widget is expanded
        EXPECTED: * First available event from current <Sport>, that has live streaming mapped, is displayed(see **startTime** attribute)
        EXPECTED: * Events with identical start time are sorted in the following way:
        EXPECTED: 1) competition 'displayOrder' in ascending
        EXPECTED: 2) Alphabetical order
        """
        pass

    def test_003_verify_correct_event_is_displayed_in_live_stream_widget(self):
        """
        DESCRIPTION: Verify correct event is displayed in Live Stream widget
        EXPECTED: Event which satisfy the following conditions should be present on widget:
        EXPECTED: * **drilldownTagNames** should include the following attributes: {EVFLAG_BL and EVFLAG_IVM} OR {EVFLAG_BL, EVFLAG_PVM} OR {EVFLAG_BL, EVFLAG_GVM} (on the Event level)
        EXPECTED: * AND **isMarketBetInRun**="true"(on the any Market level)
        EXPECTED: * event **startTime** is today
        EXPECTED: * AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        """
        pass

    def test_004_verify_that_event_with_several_streaming_providers_mapped_is_shown_in_the_live_stream_widget(self):
        """
        DESCRIPTION: Verify that event with several streaming providers mapped is shown in the Live Stream widget
        EXPECTED: * Event with several streaming providers mapped is show
        EXPECTED: * List of mapped providers are available in /api/video/igame/<eventID> response
        EXPECTED: * response contains <priorityProviderName> attribute
        """
        pass

    def test_005_verify_event_classtype(self):
        """
        DESCRIPTION: Verify event class/type
        EXPECTED: * Class/type that event belongs to is truncated in case it doesn't fit
        EXPECTED: * Class/type is in the following format and correspond to the following attributes:
        EXPECTED: * **Type Name** if on Pre-Match pages section is named in the format 'Category Name + Type Name'
        EXPECTED: * **Class Name - Type Name** if on Pre-Match pages section is named in the format 'Class Name (Sports name should not be displayed) + Type Name'
        """
        pass

    def test_006_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: * Event name corresponds to 'name' attribute
        EXPECTED: * Event name is shown in format 'Team1/player1 v Team2/player2' in 1 line
        EXPECTED: * Event name is truncated in case it doesn't fit
        """
        pass

    def test_007_verify_scores(self):
        """
        DESCRIPTION: Verify Scores
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' team/player respectively
        EXPECTED: * Scores are placed in the same line with event name
        """
        pass

    def test_008_verify_fixture_header(self):
        """
        DESCRIPTION: Verify Fixture header
        EXPECTED: * Fixture header is shown with 'Home'/'Draw'/'Away' options for 3-way Primary Market
        EXPECTED: * Fixture header is shown with '1'/'2' options for 2-way Primary Market
        EXPECTED: * Fixture header's color changes to green when appropriate 'Price/Odds' button is selected
        """
        pass

    def test_009_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify Price/Odds buttons
        EXPECTED: * 'Price/Odds' corresponds to the 'priceNum/priceDen' if eventStatusCode="A" in fraction format
        EXPECTED: * 'Price/Odds' corresponds to the 'priceDec' if eventStatusCode="A" in decimal format
        EXPECTED: * Disabled 'Price/Odds' button is displayed with 'priceNum/priceDen' (for fractional format) or 'priceDec' (for Decimal format if eventStatusCode="S"
        EXPECTED: * 'Price/Odds' buttons are ordered by the rule for 2-Way Market bellow respective option from Fixture header:
        EXPECTED: outcomeMeaningMinorCode="H" is a Home
        EXPECTED: outcomeMeaningMinorCode="A" is an Away
        EXPECTED: * 'Price/Odds' buttons are ordered by the rule for 3-Way Market bellow respective option from Fixture header:
        EXPECTED: outcomeMeaningMinorCode="H" is a Home
        EXPECTED: outcomeMeaningMinorCode="D" is a Draw
        EXPECTED: outcomeMeaningMinorCode="A" is an Away
        EXPECTED: * 'Price/Odds' button's color changes to green when selected; selection is added to the bet slip
        """
        pass
