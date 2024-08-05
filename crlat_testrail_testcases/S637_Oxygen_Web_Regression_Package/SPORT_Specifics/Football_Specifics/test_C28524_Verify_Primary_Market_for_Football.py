import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28524_Verify_Primary_Market_for_Football(Common):
    """
    TR_ID: C28524
    NAME: Verify Primary Market for Football
    DESCRIPTION: This test case verifies Primary Market for 'Football' Sport
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Go to Football landing page
    """
    keep_browser_open = True

    def test_001_verify_todays_matches_page_for_desktop(self):
        """
        DESCRIPTION: Verify Today's Matches page for **Desktop**
        EXPECTED: * Today's Matches page is opened
        EXPECTED: * Events are grouped by **classId** and typeId
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining accordions are collapsed by default
        EXPECTED: * If no events to show, the message No events found is displayed
        """
        pass

    def test_002_verify_list_of_events__on_matches__gt_today_tab_for_desktop__on_matches_tab_on_mobile(self):
        """
        DESCRIPTION: Verify list of events
        DESCRIPTION: - on Matches -&gt; Today tab for **Desktop**
        DESCRIPTION: - on Matches tab on **Mobile**
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: or
        EXPECTED: *   **name="Match Result"
        EXPECTED: *   **dispSortName="MR"**
        """
        pass

    def test_003_verify_priceodds_button_for_3_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 3-Way Market
        EXPECTED: For **Match Betting/Match Result** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home **'Win'**
        EXPECTED: *   outcomeMeaningMinorCode="D" is a **'Draw'**
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'Win'**
        """
        pass

    def test_004_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap 'In-Play' tab
        EXPECTED: **'In-Play'** tab is opened
        """
        pass

    def test_005_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: or
        EXPECTED: *   **name="Match Result"
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_006_repeat_step_4_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat step №4 for events that are not Outrights
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_3_step_3_only_for_tomorrow_and_future_tabs_for_desktop_for_tomorrow_tab_for_desktop_only_future_tab_for_desktop_only_competition_tab_mobile_only_competition_detailed_page_mobile_where_applicable_live_stream_pagetab__gt_live_now_and_upcoming_filters_highlights_carousel_module_created_on_homepage_landing_page_featured_tab_module_created_by_typeid_live_stream_widget(self):
        """
        DESCRIPTION: Repeat steps №1-3 (step 3 only for Tomorrow and Future tabs for Desktop) for:
        DESCRIPTION: * 'Tomorrow' tab (for desktop only)
        DESCRIPTION: * 'Future' tab (for desktop only)
        DESCRIPTION: * 'Competition' tab (mobile only)
        DESCRIPTION: * 'Competition Detailed' page (mobile, where applicable)
        DESCRIPTION: * 'Live Stream' page/tab -&gt; 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * 'Highlights carousel' module created on Homepage/ Landing page
        DESCRIPTION: * Featured tab module created by typeID
        DESCRIPTION: * Live Stream widget
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_3_and_5_6_for_in_play_tab__gt_live_now_and_upcoming_filters_in_play_sport_page__gt_live_now_and_upcoming_filters_in_play_widget_on_desktop(self):
        """
        DESCRIPTION: Repeat steps №2-3 and №5-6 for:
        DESCRIPTION: * In-Play tab -&gt; 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -&gt; 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        EXPECTED: 
        """
        pass
