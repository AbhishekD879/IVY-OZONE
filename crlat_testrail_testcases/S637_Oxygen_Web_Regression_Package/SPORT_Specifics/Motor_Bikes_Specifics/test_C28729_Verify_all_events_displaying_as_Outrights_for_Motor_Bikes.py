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
class Test_C28729_Verify_all_events_displaying_as_Outrights_for_Motor_Bikes(Common):
    """
    TR_ID: C28729
    NAME: Verify all events displaying as Outrights for Motor Bikes
    DESCRIPTION: This test case verifies all events displaying as Outrights.
    DESCRIPTION: Story related: BMA-2280 Create a Motor Bikes sport within the Application
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Category ID: 23 for Motor Bikes
    PRECONDITIONS: * Load Oxygen app
    """
    keep_browser_open = True

    def test_001_tapmotor_bikes_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Motor Bikes' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: *   Motor Bikes Landing Page is opened
        EXPECTED: *   '**Events**'->''**Today**' tab is opened by default
        EXPECTED: **Mobile:**
        EXPECTED: * Motor Bikes Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        pass

    def test_002_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: All events are displayed as Outrights and have an attribute:
        EXPECTED: '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)'
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_003_repeat_steps_2_for_in_play_tab_on_sport_ladning_page_desktop_only_in_play_tab_on_homepage__live_now_and_upcoming_filters_in_play_sport_page___live_now_and_upcoming_filters_in_play_widget_on_desktop_tomorrow_tab_for_desktop_only_future_tab_for_desktop_only_outrights_tab_mobile_only_competition_detailed_page___outrights_tabmobile_where_applicable_live_stream_pagetab___live_now_and_upcoming_filters_highlights_carousel_module_created_on_homepage_landing_page_featured_tab_module_created_by_typeid(self):
        """
        DESCRIPTION: Repeat steps №2 for:
        DESCRIPTION: * In Play tab on Sport Ladning page (Desktop ONLY)
        DESCRIPTION: * In-Play tab on Homepage-> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        DESCRIPTION: * 'Tomorrow' tab (for desktop only)
        DESCRIPTION: * 'Future' tab (for desktop only)
        DESCRIPTION: * 'Outrights' tab (mobile only)
        DESCRIPTION: * 'Competition Detailed' page -> Outrights tab(mobile, where applicable)
        DESCRIPTION: * 'Live Stream' page/tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * 'Highlights carousel' module created on Homepage/ Landing page
        DESCRIPTION: * Featured tab module created by typeID
        EXPECTED: 
        """
        pass
