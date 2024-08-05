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
class Test_C28735_Verify_Primary_Market_for_UFC_MMA(Common):
    """
    TR_ID: C28735
    NAME: Verify Primary Market for UFC/MMA
    DESCRIPTION: This test case verifies Primary Market for 'UFC/MMA' Sport
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs (for Desktop)
    PRECONDITIONS: * Load Oxygen app
    """
    keep_browser_open = True

    def test_001_tapufcmma_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'UFC/MMA' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: * UFC/MMA Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: **Mobile:**
        EXPECTED: * UFC/MMA Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        pass

    def test_002_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Fight Betting"**
        EXPECTED: *   **dispSortName="HH"**
        """
        pass

    def test_003_verify_priceodds_button_for_2_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 2-Way Market
        EXPECTED: For **Fight Betting** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home ***'Win'***
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'*Win'***
        """
        pass

    def test_004_tap_in_play_tab_desktopnote_for_mobile_in_play_events_are_displayed_in_in_play_module(self):
        """
        DESCRIPTION: Tap 'In-Play' tab ((Desktop)
        DESCRIPTION: note: for mobile in-play events are displayed in In-Play module)
        EXPECTED: **'In-Play'** tab is opened
        """
        pass

    def test_005_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Fight Betting"**
        EXPECTED: *   **dispSortName="HH"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_006_repeat_step_3_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat step №3 for events that are not Outrights
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_2_for_tomorrow_tab_for_desktop_only_future_tab_for_desktop_only_competition_tab_mobile_only_competition_detailed_page_mobile_where_applicable_live_stream_pagetab___live_now_and_upcoming_filters_highlights_carousel_module_created_on_homepage_landing_page_featured_tab_module_created_by_typeid_live_stream_widget(self):
        """
        DESCRIPTION: Repeat steps №1-2 for:
        DESCRIPTION: * 'Tomorrow' tab (for desktop only)
        DESCRIPTION: * 'Future' tab (for desktop only)
        DESCRIPTION: * 'Competition' tab (mobile only)
        DESCRIPTION: * 'Competition Detailed' page (mobile, where applicable)
        DESCRIPTION: * 'Live Stream' page/tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * 'Highlights carousel' module created on Homepage/ Landing page
        DESCRIPTION: * Featured tab module created by typeID
        DESCRIPTION: * Live Stream widget
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_2_and_4_5_for_in_play_tab___live_now_and_upcoming_filters_in_play_sport_page___live_now_and_upcoming_filters_in_play_widget_on_desktop(self):
        """
        DESCRIPTION: Repeat steps №1-2 and №4-5 for:
        DESCRIPTION: * In-Play tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        EXPECTED: 
        """
        pass
