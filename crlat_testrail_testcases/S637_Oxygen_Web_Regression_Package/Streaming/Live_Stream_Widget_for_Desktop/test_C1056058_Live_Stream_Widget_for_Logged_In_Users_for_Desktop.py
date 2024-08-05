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
class Test_C1056058_Live_Stream_Widget_for_Logged_In_Users_for_Desktop(Common):
    """
    TR_ID: C1056058
    NAME: 'Live Stream' Widget for Logged In Users for Desktop
    DESCRIPTION: This test case verifies 'Live Stream' Widget for logged in users for Desktop.
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Live Stream is mapped
    PRECONDITIONS: To get information about event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/xxxx?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * x.xx latest supported SiteServer version
    PRECONDITIONS: * xxxx event id
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: **startTime** attribute - to see start time of event
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
        EXPECTED: * First available event from current <Sport>, that has live streaming mapped, is displayed (see **startTime** attribute)
        EXPECTED: * Events with identical start time are sorted in the following way:
        EXPECTED: 1) competition 'displayOrder' in ascending
        EXPECTED: 2) Alphabetical order
        """
        pass

    def test_003_verify_live_stream_widget_content(self):
        """
        DESCRIPTION: Verify Live Stream widget content
        EXPECTED: Live Stream widget consists of:
        EXPECTED: * Header
        EXPECTED: * Main content area
        EXPECTED: * Footer
        """
        pass

    def test_004_verify_live_stream_widget_header(self):
        """
        DESCRIPTION: Verify Live Stream widget header
        EXPECTED: Live Stream widget header consists of:
        EXPECTED: * 'Watch live' icon(There is no 'Watch live' icon for Ladbrokes)
        EXPECTED: * 'Watch live' text
        EXPECTED: * Expand/collapse icon(only expand icon is shown for Ladbrokes)
        """
        pass

    def test_005_verify_live_stream_widget_main_content_area(self):
        """
        DESCRIPTION: Verify Live Stream widget main content area
        EXPECTED: Live Stream widget main content area contains 1 live streaming event of respective sport and consists of:
        EXPECTED: * Background image (the same for all sports, not clickable)
        EXPECTED: * Class/type that event belongs to
        EXPECTED: * 'Live'/'Timer'/'Sets' badge highlighted in red (next to class/type)
        EXPECTED: * 'Cash Out' icon at the top right corner in the same row as Class/Type name (if cashout available)
        EXPECTED: * Event name
        EXPECTED: * Scores (next to event name)
        EXPECTED: * 'Play' icon
        EXPECTED: * Fixture header ('Home'/'Draw'/'Away' options for 3-way Primary Market; '1'/'2' for 2-way Primary Market)
        EXPECTED: * Price/odds buttons below Fixture header in 1 row
        """
        pass

    def test_006_verify_live_stream_widget_footer(self):
        """
        DESCRIPTION: Verify Live Stream widget footer
        EXPECTED: * Live Stream widget footer contains 'View all live streaming events' link
        EXPECTED: * Link takes user to 'Live Stream' page
        """
        pass

    def test_007_click_on_play_icon_in_the_main_content_area(self):
        """
        DESCRIPTION: Click on 'Play' icon in the main content area
        EXPECTED: * User is taken to event details page where live streaming can be watched
        EXPECTED: * Streaming starts automatically on EDP
        """
        pass

    def test_008_click_on_header_area_or_collapseexpand_icon(self):
        """
        DESCRIPTION: Click on header area or collapse/expand icon
        EXPECTED: Live Stream widget gets collapsed/expanded
        """
        pass
