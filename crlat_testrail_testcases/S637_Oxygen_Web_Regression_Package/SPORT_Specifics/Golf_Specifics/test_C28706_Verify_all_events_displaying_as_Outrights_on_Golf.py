import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28706_Verify_all_events_displaying_as_Outrights_on_Golf(Common):
    """
    TR_ID: C28706
    NAME: Verify all events displaying as Outrights on Golf
    DESCRIPTION: This test case verifies all events displaying as Outrights.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Go to Golf landing page
    """
    keep_browser_open = True

    def test_001_verify_list_of_events__on_matches___today_tab_for_desktop__on_golf_landing_page_single_view_on_mobile(self):
        """
        DESCRIPTION: Verify list of events
        DESCRIPTION: - on Matches -> Today tab for **Desktop**
        DESCRIPTION: - on Golf Landing Page (single view) on **Mobile**
        EXPECTED: Events are displayed as Outrights and have 2 sets of attributes:
        EXPECTED: 1) '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)'
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *Market Sort = To-Win*
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        EXPECTED: 2) '**eventSortCode="MATCH"**
        EXPECTED: *   **templateMarketName / name = "3 Ball Betting"**
        EXPECTED: *Market Sort = To-Win*
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_002_repeat_steps_1_for_in_play_tab_on_sport_ladning_page_desktop_only_in_play_tab_on_homepage__live_now_and_upcoming_filters_in_play_sport_page___live_now_and_upcoming_filters_in_play_widget_on_desktop_tomorrow_tab_for_desktop_only_future_tab_for_desktop_only_outrighs_tab_mobile_only_competition_detailed_page___outrighs_tabmobile_where_applicable_live_stream_pagetab___live_now_and_upcoming_filters_highlights_carousel_module_created_on_homepage_landing_page_featured_tab_module_created_by_typeid(self):
        """
        DESCRIPTION: Repeat steps №1 for:
        DESCRIPTION: * In Play tab on Sport Ladning page (Desktop ONLY)
        DESCRIPTION: * In-Play tab on Homepage-> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        DESCRIPTION: * 'Tomorrow' tab (for desktop only)
        DESCRIPTION: * 'Future' tab (for desktop only)
        DESCRIPTION: * 'Outrighs' tab (mobile only)
        DESCRIPTION: * 'Competition Detailed' page -> Outrighs tab(mobile, where applicable)
        DESCRIPTION: * 'Live Stream' page/tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * 'Highlights carousel' module created on Homepage/ Landing page
        DESCRIPTION: * Featured tab module created by typeID
        EXPECTED: 
        """
        pass
