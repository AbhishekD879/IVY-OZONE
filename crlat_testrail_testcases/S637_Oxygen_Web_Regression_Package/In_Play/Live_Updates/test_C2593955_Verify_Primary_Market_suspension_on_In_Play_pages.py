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
class Test_C2593955_Verify_Primary_Market_suspension_on_In_Play_pages(Common):
    """
    TR_ID: C2593955
    NAME: Verify Primary Market suspension on In-Play pages
    DESCRIPTION: This test case verifies Primary Market suspension on In-Play pages
    DESCRIPTION: AUTOTEST Mobile: [C2594012]
    DESCRIPTION: AUTOTEST Desktop: [C2594013]
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (**Mobile/Tablet**) or 'Main Navigation' menu at the 'Universal Header' (**Desktop**) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (**Mobile/Tablet**) or when 'Live Now' switcher is selected (** Desktop**)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (**Mobile/Tablet**) or select 'Upcoming' switcher (**Desktop**)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify suspension check new received value in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection
    PRECONDITIONS: ![](index.php?/attachments/get/40328)
    """
    keep_browser_open = True

    def test_001_need_to_be_updated_find_an_event_with_priceodds_buttons_displaying_prices(self):
        """
        DESCRIPTION: (NEED TO BE UPDATED!) Find an event with Price/Odds buttons displaying prices
        EXPECTED: 
        """
        pass

    def test_002__trigger_the_following_situation_for_this_eventmarketstatuscodes_for_primary_market_market_type_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Trigger the following situation for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>' market type
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: 
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled but still displaying prices
        EXPECTED: * The following attribute is received in WS -> ?EIO=3&transport=websocket response with type "EVMKT":
        EXPECTED: **status: "S"**
        """
        pass

    def test_004__trigger_the_following_situation_for_this_eventmarketstatuscodea_for_primary_market_market_type_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Trigger the following situation for this event:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>' market type
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * All Price/Odds buttons of this event are no more disabled, they become active immediately
        EXPECTED: * The following attribute is received in WS -> ?EIO=3&transport=websocket response with type "EVMKT":
        EXPECTED: **status: "A"**
        """
        pass

    def test_005__collapse_sectiontype_accordion_and_trigger_the_primary_market_status_change_marketstatuscodes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Collapse section/type accordion and trigger the '<Primary market>' status change **marketStatusCode="S"**
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events that belong to collapsed section/type accordion are received in in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscription that was triggered
        """
        pass

    def test_006__expand_the_sectiontype_accordion_with_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Expand the section/type accordion with the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * All Price/Odds buttons of this event are displayed as greyed out and become disabled on Football In-Play page but still displaying the prices
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: status: "S" attribute is received in response with type "EVMKT"
        """
        pass

    def test_007__collapse_sectiontype_accordion_and_trigger_the_primary_market_status_change_marketstatuscodea_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Collapse section/type accordion and trigger the '<Primary market>' status change **marketStatusCode="A"**
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events that belong to collapsed section/type accordion are received in in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscription that was triggered
        """
        pass

    def test_008__expand_the_sectiontype_accordion_with_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Expand the section/type accordion with the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * All Price/Odds buttons of this event are no more disabled, they become active
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: status: "A" attribute is received in response with type "EVMKT"
        """
        pass

    def test_009__leave_the_in_play_page_and_trigger_the_primary_market_status_change_marketstatuscodes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Leave the In-Play page and trigger the '<Primary market>' status change **marketStatusCode="S"**
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events that belong to collapsed section/type accordion are received in in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscription that was triggered
        """
        pass

    def test_010__open_in_play_page_again_find_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Open In-Play page again, find the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * All Price/Odds buttons of this event are displayed as greyed out and become disabled on Football In-Play page but still displaying the prices
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: status: "S" attribute is received in response with type "EVMKT"
        """
        pass

    def test_011__leave_the_in_play_page_again_and_trigger_the_primary_market_status_change_marketstatuscodea_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Leave the In-Play page again and trigger the '<Primary market>' status change **marketStatusCode="A"**
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events that belong to collapsed section/type accordion are received in in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscription that was triggered
        """
        pass

    def test_012__open_in_play_page_again_find_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Open In-Play page again, find the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * All Price/Odds buttons of this event are no more disabled, they become active
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: status: "A" attribute is received in response with type "EVMKT"
        """
        pass

    def test_013_need_to_be_updated_repeat_steps_1_12_for_events_from_upcoming_section(self):
        """
        DESCRIPTION: (NEED TO BE UPDATED!) Repeat steps 1-12 for events from 'Upcoming' section
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_1_13_for_the_following_pages_home_page__in_play_tab_mobiletablet_sports_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-13 for the following pages:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        EXPECTED: 
        """
        pass

    def test_015_desktoprepeat_steps_1_2_on_home_page_for_in_play__live_stream_section_for_both_switchers_sport_landing_page_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Repeat steps 1-2 on:
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers
        DESCRIPTION: * Sport Landing page for 'In-play' widget
        EXPECTED: 
        """
        pass
