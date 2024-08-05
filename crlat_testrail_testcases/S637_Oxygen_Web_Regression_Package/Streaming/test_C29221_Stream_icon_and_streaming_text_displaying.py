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
class Test_C29221_Stream_icon_and_streaming_text_displaying(Common):
    """
    TR_ID: C29221
    NAME: 'Stream' icon and streaming text displaying
    DESCRIPTION: AUTOTEST: [C9771270]
    DESCRIPTION: This test case verifies Stream icon and streaming text displaying on <Sport>/<Race> Landing pages.
    PRECONDITIONS: *1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XX - Sport Category ID.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: *2. For each **Class **retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?translationLang=LL
    PRECONDITIONS: *   XXX -  comma separated list of **Class **ID's
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: *   **'name'** to define event name
    PRECONDITIONS: *   **'drilldownTagNames'** to determine WHICH stream provider has been mapped to the event
    PRECONDITIONS: **'drilldownTagNames'**** ***Streaming flags are:*
    PRECONDITIONS: 1.  *EVFLAG_IVM - IMG Video streaming Mapped*
    PRECONDITIONS: 2.  *EVFLAG_PVM - Perform Video streaming Mapped*
    PRECONDITIONS: 3.  *EVFLAG_AVA - At The Races streaming Mapped*
    PRECONDITIONS: 4.  *EVFLAG_RVA - RacingUK streaming Mapped*
    PRECONDITIONS: 5.  *EVFLAG_RPM - RPGTV Greyhound streaming Mapped*
    PRECONDITIONS: 6.  *EVFLAG_GVM - iGameMedia streaming Mapped*
    PRECONDITIONS: *3. Oxygen App is opened
    """
    keep_browser_open = True

    def test_001_go_to_sport_landing_page(self):
        """
        DESCRIPTION: Go to <Sport> Landing page
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_002_verify_sport_event_which_has_a_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Sport> event which has a 'Stream' icon displayed
        EXPECTED: 'Stream' icon ![](index.php?/attachments/get/2668501)(Coral) / ![](index.php?/attachments/get/2668538) (Ladbrokes) is displayed on Sport Landing Page
        EXPECTED: *   **'drilldownTagNames'** in SiteServe response for the event contains one or more flags from the list in Preconditions.
        EXPECTED: ![](index.php?/attachments/get/2668494)
        """
        pass

    def test_003_verify_sport_event_which_doesnt_have_a_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Sport> event which doesn't have a 'Stream' icon displayed
        EXPECTED: 'Stream' icon is NOT displayed on Sport Landing Page and 'Watch Live' tab is NOT displayed on Event Details pages when:
        EXPECTED: *   **'drilldownTagNames'** in SiteServe response for the event doesn't contain any of the mentioned flags from the list in Preconditions.
        """
        pass

    def test_004_go_to_race_landing_page(self):
        """
        DESCRIPTION: Go to <Race> Landing page
        EXPECTED: <Race> Landing page is opened
        """
        pass

    def test_005_verify_race_meeting_which_has_a_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify race meeting which has a 'Stream' icon displayed
        EXPECTED: 'Stream' icon ![](index.php?/attachments/get/2668506)(Coral) / ![](index.php?/attachments/get/2668533) (Ladbrokes) is displayed for a race if at least one event within the race has a mapped stream:
        EXPECTED: *   **'drilldownTagNames'** in SiteServe response for the event(from a viewed Race) contains one or more flags from the list in Preconditions.
        EXPECTED: ![](index.php?/attachments/get/3050942)
        """
        pass

    def test_006_verify_race_meeting_which_doesnt_have_a_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Race> meeting which doesn't have a 'Stream' icon displayed
        EXPECTED: 'Stream' icon is NOT displayed for a race if it doesn't have at least one event within itself with a mapped stream.
        EXPECTED: *   **'drilldownTagNames'** in SiteServe response for all events(from a viewed Race) doesn't contain any of the mentioned flags from the list in Preconditions.
        """
        pass
