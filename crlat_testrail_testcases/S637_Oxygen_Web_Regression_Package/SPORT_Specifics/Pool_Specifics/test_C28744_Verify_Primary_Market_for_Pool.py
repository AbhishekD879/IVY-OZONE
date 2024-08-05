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
class Test_C28744_Verify_Primary_Market_for_Pool(Common):
    """
    TR_ID: C28744
    NAME: Verify Primary Market for Pool
    DESCRIPTION: This test case verifies Primary Market for 'Pool' Sport.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs (for Desktop)
    PRECONDITIONS: *Load Oxygen app
    """
    keep_browser_open = True

    def test_001_tappool_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Pool' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: * Pool Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: **Mobile:**
        EXPECTED: * Pool Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        pass

    def test_002_verify_list_of_events__on_matches___today_tab_for_desktop__on_matches_tab_on_mobile(self):
        """
        DESCRIPTION: Verify list of events
        DESCRIPTION: - on Matches -> Today tab for Desktop
        DESCRIPTION: - on Matches tab on Mobile
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   ****dispSortName="HH"****
        """
        pass

    def test_003_verify_priceodds_button_for_2_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 2-Way Market
        EXPECTED: For **Match Betting** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home ***'Win'***
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'*Win'***
        """
        pass

    def test_004_tap_in_play_tab_desktopnote_for_mobile_view_in_play_events_are_displayed_in_in_play_module_on_landing_page(self):
        """
        DESCRIPTION: Tap '**In-Play**' tab (Desktop)
        DESCRIPTION: Note: for Mobile view In-Play events are displayed in In-Play module on landing page.
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   ****dispSortName="HH"****
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_005_repeat_step_3_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat step №3 for events that are not Outrights
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_3_fortomorrow_tab_for_desktop_onlyfuture_tab_for_desktop_onlycompetition_tab_mobile_onlycompetition_detailed_page_mobile_where_applicablelive_stream_pagetab___live_now_and_upcoming_filtershighlights_carousel_module_created_on_homepage_landing_pagefeatured_tab_module_created_by_typeidlive_stream_widget(self):
        """
        DESCRIPTION: Repeat steps №1-3 for:
        DESCRIPTION: 'Tomorrow' tab (for desktop only)
        DESCRIPTION: 'Future' tab (for desktop only)
        DESCRIPTION: 'Competition' tab (mobile only)
        DESCRIPTION: 'Competition Detailed' page (mobile, where applicable)
        DESCRIPTION: 'Live Stream' page/tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: 'Highlights carousel' module created on Homepage/ Landing page
        DESCRIPTION: Featured tab module created by typeID
        DESCRIPTION: Live Stream widget
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_13_and_5_6_forin_play_tab___live_now_and_upcoming_filtersin_play_sport_page___live_now_and_upcoming_filtersin_play_widget_on_desktop(self):
        """
        DESCRIPTION: Repeat steps №1,3 and №5-6 for:
        DESCRIPTION: In-Play tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: In Play widget on Desktop
        EXPECTED: 
        """
        pass
