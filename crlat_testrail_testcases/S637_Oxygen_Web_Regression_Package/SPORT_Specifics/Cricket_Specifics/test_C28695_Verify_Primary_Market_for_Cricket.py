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
class Test_C28695_Verify_Primary_Market_for_Cricket(Common):
    """
    TR_ID: C28695
    NAME: Verify Primary Market for Cricket
    DESCRIPTION: This test case verifies Primary Market for 'Cricket' Sport
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs (for desktop)/ 'Matches' tab (for mobile)
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Go to Cricket landing page
    """
    keep_browser_open = True

    def test_001_verify_list_of_events__on_matches___today_tab_for_desktop__on_matches_tab_on_mobile(self):
        """
        DESCRIPTION: Verify list of events
        DESCRIPTION: - on Matches -> Today tab for **Desktop**
        DESCRIPTION: - on Matches tab on **Mobile**
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: ****OR****
        EXPECTED: *   **name="Match Betting Head/Head"**
        EXPECTED: *   **dispSortName="HH"**
        """
        pass

    def test_002_verify_priceodds_buttons_for_2_way_marketwhere_dispsortnamehh(self):
        """
        DESCRIPTION: Verify Price/Odds buttons for 2-Way Market (where dispSortName="HH")
        EXPECTED: For **2-way Match Betting Head/Head** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home ***'Win'***
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'*Win'***
        """
        pass

    def test_003_verify_priceodds_buttons_for_3_way_market_where_dispsortnamemr(self):
        """
        DESCRIPTION: Verify Price/Odds buttons for 3-Way Market (where dispSortName="MR")
        EXPECTED: For  **3-way Match Betting** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home ***'Win'***
        EXPECTED: *   outcomeMeaningMinorCode="D" is a ***'Draw'***
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'*Win'***
        """
        pass

    def test_004_tap_in_play_tabin_play_module_on_matches_tab_for_mobile(self):
        """
        DESCRIPTION: Tap 'In-Play' tab
        DESCRIPTION: (In-Play module on Matches tab for Mobile)
        EXPECTED: '**In-Play**' tab is opened
        """
        pass

    def test_005_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: **OR**
        EXPECTED: *   **name="Match Betting Head/Head"**
        EXPECTED: *   **dispSortName="HH"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_006_repeat_steps_2_3_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat steps №2-3 for events that are not Outrights
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_3_for_tomorrow_tab_for_desktop_only_future_tab_for_desktop_only_competition_tab_mobile_only_competition_detailed_page_mobile_where_applicable_live_stream_pagetab___live_now_and_upcoming_filters_highlights_carousel_module_created_on_homepage_landing_page_featured_tab_module_created_by_typeid_live_stream_widget(self):
        """
        DESCRIPTION: Repeat steps №1-3 for:
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

    def test_008_repeat_steps_1_3_and_4_5_for_in_play_tab___live_now_and_upcoming_filters_in_play_sport_page___live_now_and_upcoming_filters_in_play_widget_on_desktop(self):
        """
        DESCRIPTION: Repeat steps №1-3 and №4-5 for:
        DESCRIPTION: * In-Play tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        EXPECTED: 
        """
        pass
