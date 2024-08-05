import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C29222_Stream_buttons_on_Event_Details_Pages(Common):
    """
    TR_ID: C29222
    NAME: 'Stream' buttons on Event Details Pages
    DESCRIPTION: This test case verifies Stream button displaying on <Sport>/<Race> Event Details page.
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

    def test_001_all_devicesgo_to_sport_landing_page(self):
        """
        DESCRIPTION: **All devices**
        DESCRIPTION: Go to <Sport> Landing page
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_002_click_on_sport_event_which_has_a_stream_icon_displayed(self):
        """
        DESCRIPTION: Click on <Sport> event which has a 'Stream' icon displayed
        EXPECTED: Event Details page is opened
        """
        pass

    def test_003_verify_presence_of_a_stream_button(self):
        """
        DESCRIPTION: Verify presence of a 'Stream' button
        EXPECTED: * Desktop:
        EXPECTED: 'Watch Live' ![](index.php?/attachments/get/3050948) (Coral) / ![](index.php?/attachments/get/3050949) (Ladbrokes) button is shown in both case of scoreboard/visualization being present.
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Watch Live' button is shown when scoreboard is present(for both brands);
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050950) (Coral) / ![](index.php?/attachments/get/3050951) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_004_desktop_onlyverify_absence_of_a_stream_button(self):
        """
        DESCRIPTION: **Desktop Only**
        DESCRIPTION: Verify absence of a 'Stream' button
        EXPECTED: Streaming is started once EDP is opened
        EXPECTED: XHR doesn't contain response from visualization or scoreboard requests(filter keywords are **vis** and **scoreb**)
        EXPECTED: Stream button is not shown
        EXPECTED: -
        EXPECTED: There is also a case when visualization response is present but contains an error or no data linking which also counts as 'visualization' absence
        EXPECTED: ![](index.php?/attachments/get/13737893)
        """
        pass

    def test_005_all_devicesgo_to_race_landing_page(self):
        """
        DESCRIPTION: **All devices**
        DESCRIPTION: Go to <Race> Landing page
        EXPECTED: <Race> Landing page is opened
        """
        pass

    def test_006_verify_race_meeting_which_has_a_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify race meeting which has a 'Stream' icon displayed
        EXPECTED: **'drilldownTagNames'** in SiteServe response for the event(from a viewed Race) contains one or more flags from the list in Preconditions.
        EXPECTED: ![](index.php?/attachments/get/3050942)
        """
        pass

    def test_007_click_on_race_event_with_the_appropriate_drilldowntagnames_being_present_in_its_siteserve_response(self):
        """
        DESCRIPTION: Click on <Race> event with the appropriate **'drilldownTagNames'** being present in its SiteServe response
        EXPECTED: Event Details page is opened
        """
        pass

    def test_008_verify_presence_of_a_stream_button(self):
        """
        DESCRIPTION: Verify presence of a 'Stream' button
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_009_repeat_step_3_on_edp_of_the_sport_event_that_doesnt_have_a_stream_icon_displayed(self):
        """
        DESCRIPTION: Repeat step 3 on EDP of the <Sport> event that DOESN'T have a 'Stream' icon displayed
        EXPECTED: 'Watch Live'/'Watch' button is not shown on EDP
        """
        pass

    def test_010_repeat_step_3_on_edp_of_the_race_event_without_the_appropriate_drilldowntagnames_being_present_in_its_siteserve_response(self):
        """
        DESCRIPTION: Repeat step 3 on EDP of the <Race> event WITHOUT the appropriate **'drilldownTagNames'** being present in its SiteServe response
        EXPECTED: 'Live Stream'/'Watch' button is not shown on EDP
        """
        pass
