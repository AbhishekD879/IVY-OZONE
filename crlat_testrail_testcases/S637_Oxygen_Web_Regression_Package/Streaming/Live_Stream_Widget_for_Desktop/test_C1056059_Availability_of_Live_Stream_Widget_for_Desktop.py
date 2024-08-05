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
class Test_C1056059_Availability_of_Live_Stream_Widget_for_Desktop(Common):
    """
    TR_ID: C1056059
    NAME: Availability of 'Live Stream' Widget for Desktop
    DESCRIPTION: This test case verifies availability of 'Live Stream' Widget for Desktop.
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Live streaming is mapped for one type of sport
    PRECONDITIONS: * Live streaming is NOT mapped for another type of sport
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
        EXPECTED: * First available event from current <Sport>, that has live streaming mapped, is displayed (see **startTime** attribute);
        EXPECTED: * Events with identical start time are sorted in the following way:
        EXPECTED: 1) competition 'displayOrder' in ascending
        EXPECTED: 2) Alphabetical order
        """
        pass

    def test_003_navigate_to_other_sport_sub_tabs_within_sport_landing_page_where_live_streaming_is_mapped_eg_competitions_coupons_etc(self):
        """
        DESCRIPTION: Navigate to other sport sub tabs within <Sport> Landing page where live streaming is mapped e.g. 'Competitions', 'Coupons', etc.
        EXPECTED: Live Stream widget is NOT present in the Main view column 2
        """
        pass

    def test_004_navigate_to_other_pages_within_the_app(self):
        """
        DESCRIPTION: Navigate to other pages within the app
        EXPECTED: Live Stream widget is NOT present in the Main view column 2
        """
        pass

    def test_005_navigate_to_sport_landing_page_where_live_streaming_is_not_mapped(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page where live streaming is NOT mapped
        EXPECTED: Live Stream widget is NOT present
        """
        pass

    def test_006_navigate_back_to_sport_landing_page_where_live_streaming_is_mapped(self):
        """
        DESCRIPTION: Navigate back to <Sport> Landing page where live streaming is mapped
        EXPECTED: * <Sport> Landing page is opened
        EXPECTED: * 'Matches' tab is opened by default
        EXPECTED: * Live Stream widget is present in the Main view column 2
        EXPECTED: * Live Stream widget is expanded
        EXPECTED: * First available event from current <Sport>, that has live streaming mapped, is displayed (see **startTime** attribute);
        """
        pass

    def test_007_verify_live_stream_widget_at_1279_px_screen_resolution(self):
        """
        DESCRIPTION: Verify Live Stream widget at <=1279 px screen resolution
        EXPECTED: Live Stream widget is NOT present in the Main view column 2 but moved to the bottom of the Main view (column 1 + column 2)
        """
        pass

    def test_008_verify_live_stream_widget_at_1280_px_screen_resolution(self):
        """
        DESCRIPTION: Verify Live Stream widget at >=1280 px screen resolution
        EXPECTED: Live Stream widget is present in the Main view column 2
        """
        pass
