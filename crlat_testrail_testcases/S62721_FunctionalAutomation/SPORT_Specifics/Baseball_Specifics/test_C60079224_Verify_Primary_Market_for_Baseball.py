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
class Test_C60079224_Verify_Primary_Market_for_Baseball(Common):
    """
    TR_ID: C60079224
    NAME: Verify Primary Market for Baseball
    DESCRIPTION: This test case verifies Primary Market for 'Baseball' Sport.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-15231: Changes to behaviour and display of US Sport events][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-15231
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Notes:**
    PRECONDITIONS: *   Outright events are NOT shown on Matches tab
    PRECONDITIONS: *   Current supported version of OB release can be found in the request by the list of events (Dev tools -> Network -> request URL in the "Headers" section of the request by the list of events)
    PRECONDITIONS: * Oxygen app should be loaded
    """
    keep_browser_open = True

    def test_001_tapbaseball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Baseball' icon on the Sports Menu Ribbon
        EXPECTED: Desktop:
        EXPECTED: * Baseball Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: Mobile:
        EXPECTED: * Baseball Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        pass

    def test_002_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Money Line"**
        EXPECTED: *   **dispSortName="HH"**
        """
        pass

    def test_003_verify_fixture_header(self):
        """
        DESCRIPTION: Verify fixture header
        EXPECTED: *   "1" and "2" are shown in the fixture header
        EXPECTED: *   Primary market selections for home team are shown under "**1**" label
        EXPECTED: *   Primary market selections for away team are shown under "**2**" label
        """
        pass

    def test_004_verify_order_of_priceodds_buttons_for_us_and_non_us_events(self):
        """
        DESCRIPTION: Verify order of Price/Odds buttons for US and Non-US Events
        EXPECTED: For **Money Line** primary market selections are ordered by the rule:
        EXPECTED: 1. **US** flag is included in the **typeFlagCodes** tag for US events:
        EXPECTED: *   outcomeMeaningMinorCode="A" is Away
        EXPECTED: *   outcomeMeaningMinorCode="H" is Home
        EXPECTED: 2. **US** flag is not included in the **typeFlagCodes** tag for Non-US events:
        EXPECTED: *   outcomeMeaningMinorCode="H" is Home
        EXPECTED: *   outcomeMeaningMinorCode="A" is Away
        """
        pass

    def test_005_tap_in_play_tab_for_desktop_onlynote_for_mobile_in_play_module_on_single_view_page(self):
        """
        DESCRIPTION: Tap '**In-Play**' tab (For desktop only)
        DESCRIPTION: Note: for mobile: In-Play module on single view page
        EXPECTED: **'In-Play' **tab is opened
        """
        pass

    def test_006_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Money Line"**
        EXPECTED: *   **dispSortName="HH"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_007_repeat_step_5_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat step №5 for events that are not Outrights
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_4_for_tomorrow_tab_for_desktop_only_future_tab_for_desktop_only_competition_tab_mobile_only_competition_detailed_page_mobile_where_applicable_live_stream_pagetab___live_now_and_upcoming_filters_highlights_carousel_module_created_on_homepage_landing_page_featured_tab_module_created_by_typeid_live_stream_widget(self):
        """
        DESCRIPTION: Repeat steps №2-4 for:
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

    def test_009_repeat_steps_2_4_and_6_7_for_in_play_tab___live_now_and_upcoming_filters_in_play_sport_page___live_now_and_upcoming_filters_in_play_widget_on_desktop(self):
        """
        DESCRIPTION: Repeat steps №2-4 and №6-7 for:
        DESCRIPTION: * In-Play tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        EXPECTED: 
        """
        pass
