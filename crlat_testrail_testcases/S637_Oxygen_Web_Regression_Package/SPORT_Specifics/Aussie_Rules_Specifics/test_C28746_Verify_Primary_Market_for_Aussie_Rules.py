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
class Test_C28746_Verify_Primary_Market_for_Aussie_Rules(Common):
    """
    TR_ID: C28746
    NAME: Verify Primary Market for Aussie Rules
    DESCRIPTION: This test case verifies Primary Market for 'Aussie Rules' Sport
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs (Desktop)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapaussie_rules_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Aussie Rules' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: * Aussie Rules Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile:**
        EXPECTED: * Aussie Rules Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   **dispSortName="HH"**
        """
        pass

    def test_004_verify_priceodds_button_for_2_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 2-Way Market
        EXPECTED: For **Match Betting** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home ***'Win'***
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'*Win'***
        """
        pass

    def test_005_tap_in_play_tab_desktopnote_for_mobile_view_in_play_events_are_displayed_in_in_play_module_on_landing_page(self):
        """
        DESCRIPTION: Tap 'In-Play' tab (Desktop)
        DESCRIPTION: Note: for Mobile view In-Play events are displayed in In-Play module on landing page.
        EXPECTED: **'In-Play' **tab is opened
        """
        pass

    def test_006_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   **dispSortName="HH"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        pass

    def test_007_repeat_step_4_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat step №4 for events that are not Outrights
        EXPECTED: 
        """
        pass

    def test_008_tap_tomorrow_tab_desktop(self):
        """
        DESCRIPTION: Tap 'Tomorrow' tab (Desktop)
        EXPECTED: '**Tomorrow**' tab is opened
        """
        pass

    def test_009_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps №3-4
        EXPECTED: 
        """
        pass

    def test_010_tap_future_tab_desktop(self):
        """
        DESCRIPTION: Tap 'Future' tab (Desktop)
        EXPECTED: '**Future**' tab is opened
        """
        pass

    def test_011_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps №3-4
        EXPECTED: 
        """
        pass

    def test_012_taplive_stream_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Live Stream' icon on the Sports Menu Ribbon
        EXPECTED: *   **'LIVE STREAM'** page is opened
        EXPECTED: *   **'LIVE NOW'** tab is opened by default
        """
        pass

    def test_013_find_aussie_rules_event_and_repeat_steps_6_7(self):
        """
        DESCRIPTION: Find Aussie Rules event and repeat steps №6-7
        EXPECTED: 
        """
        pass

    def test_014_tap_aussie_rules_icon_from_in_play_page_and_repeat_steps_6_7(self):
        """
        DESCRIPTION: Tap 'Aussie Rules' icon from In-Play page and repeat steps №6-7
        EXPECTED: 
        """
        pass
