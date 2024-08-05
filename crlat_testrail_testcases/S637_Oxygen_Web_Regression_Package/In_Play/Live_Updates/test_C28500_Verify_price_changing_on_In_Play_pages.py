import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28500_Verify_price_changing_on_In_Play_pages(Common):
    """
    TR_ID: C28500
    NAME: Verify price changing on In-Play pages
    DESCRIPTION: This test case verifies price changing on In-Play pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (**Mobile/Tablet**) or 'Main Navigation' menu at the 'Universal Header' (**Desktop**) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (**Mobile//Tablet**) or when 'Live Now' switcher is selected (**Desktop**)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (**Mobile/Tablet**) or select 'Upcoming' switcher (**Desktop**)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify price updates check new received values in "lp_den" and "lp_num" attributes using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: PRICE
    PRECONDITIONS: ![](index.php?/attachments/get/40084)
    """
    keep_browser_open = True

    def test_001__trigger_price_change_for_primary_market_outcome_for_one_of_the_events_within_live_now_section_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Trigger price change for <Primary market> outcome for one of the events within 'Live now' section
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: - blue **Coral**/green **Ladbrokes** color if price has decreased
        EXPECTED: - pink **Coral**/red **Coral** color if price has increased
        EXPECTED: The whole button changes color on Coral, only digits change color on Ladbrokes
        EXPECTED: * The following attributes are received in WS -> ?EIO=3&transport=websocket response with type "PRICE":
        EXPECTED: **lp_den: "X"**
        EXPECTED: **lp_num: "Y"**
        """
        pass

    def test_002__collapse_any_sectiontype_accordion_and_trigger_price_change_for_primary_market_outcome_for_the_event_in_collapsed_sectiontype_accordion_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Collapse any section/type accordion and trigger price change for <Primary market> outcome for the event in collapsed section/type accordion
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events that belong to collapsed section (Type accordion) are received in in WS -> ?EIO=3&transport=websocket response
        EXPECTED: * Updates are NOT received in WS due to unsubscription that was triggered
        """
        pass

    def test_003__expand_the_sectiontype_accordion_with_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Expand the section/type accordion with the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: - blue **Coral**/green **Ladbrokes** color if price has decreased
        EXPECTED: - pink **Coral**/red **Coral** color if price has increased
        EXPECTED: The whole button changes color on Coral, only digits change color on Ladbrokes
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: * Updated prices are received in response with type "PRICE" in the next format:
        EXPECTED: **lp_den: "X"**
        EXPECTED: **lp_num: "Y"**
        """
        pass

    def test_004__leave_the_in_playpage_and_trigger_price_change_for_a_live_event_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Leave the In-Play page and trigger price change for a live event
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events are received in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscriptions that were triggered in the previous step
        """
        pass

    def test_005__open_in_playpage_again_find_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Open In-Play page again, find the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: - blue **Coral**/green **Ladbrokes** color if price has decreased
        EXPECTED: - pink **Coral**/red **Coral** color if price has increased
        EXPECTED: The whole button changes color on Coral, only digits change color on Ladbrokes
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: * Updated prices are received in response with type "PRICE" in the next format:
        EXPECTED: **lp_den: "X"**
        EXPECTED: **lp_num: "Y"**
        """
        pass

    def test_006_verify_prices_changes_before_application_is_opened(self):
        """
        DESCRIPTION: Verify prices changes before application is opened
        EXPECTED: If application was not started/opened and price was changed for live sports event market 'Match Betting', after opening application and In-Play Sports page - updated price will be shown there
        """
        pass

    def test_007_repeat_steps_1_6_but_trigger_price_change_for_several_outcomes_of_primary_market_market_for_the_same_event_from_the_current_page(self):
        """
        DESCRIPTION: Repeat steps 1-6 but trigger price change for several outcomes of '<Primary market>' market for the same event from the current page
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_6_but_trigger_price_change_for_primary_market_market_outcome_for_several_events_from_the_current_page(self):
        """
        DESCRIPTION: Repeat steps 1-6 but trigger price change for '<Primary market>' market outcome for several events from the current page
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_1_8_for_events_from_upcoming_section(self):
        """
        DESCRIPTION: Repeat steps 1-8 for events from 'Upcoming' section
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_1_9_for_the_following_pages_home_page__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-9 for the following pages:
        DESCRIPTION: * Home page > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        EXPECTED: 
        """
        pass

    def test_011_for_desktoprepeat_steps_1_8_on_home_page_for_in_play__live_stream_section_for_both_switchers_sport_landing_page_for_in_play_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 1-8 on:
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers
        DESCRIPTION: * Sport Landing page for 'In-play' widget
        EXPECTED: 
        """
        pass
