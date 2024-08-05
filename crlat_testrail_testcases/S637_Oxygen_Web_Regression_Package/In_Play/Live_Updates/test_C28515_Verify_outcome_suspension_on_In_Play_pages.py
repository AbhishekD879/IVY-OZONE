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
class Test_C28515_Verify_outcome_suspension_on_In_Play_pages(Common):
    """
    TR_ID: C28515
    NAME: Verify outcome suspension on  In-Play pages
    DESCRIPTION: This test case verifies Outcome Suspension on In-Play pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify suspension check new received value in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection
    PRECONDITIONS: ![](index.php?/attachments/get/39924)
    """
    keep_browser_open = True

    def test_001_find_an_event_with_priceodds_buttons_displaying_prices(self):
        """
        DESCRIPTION: Find an event with Price/Odds buttons displaying prices
        EXPECTED: 
        """
        pass

    def test_002__trigger_the_following_situation_for_this_eventoutcomestatuscodes_for_one_of_the_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Trigger the following situation for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Only Price/Odds button of changed outcome is displayed immediately as greyed out and becomes disabled on the page but still displaying the price, the rest Price/Odds buttons of the same market remain not changed
        EXPECTED: * The following attribute is received in WS -> ?EIO=3&transport=websocket response with type "SELCN":
        EXPECTED: **status: "S"**
        """
        pass

    def test_003__trigger_the_following_situation_for_this_eventoutcomestatuscodea_for_one_of_the_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Trigger the following situation for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for one of the outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Price/Odds button of changed outcome becomes active on the In-Play page and still displaying the price
        EXPECTED: * The following attribute is received in WS -> ?EIO=3&transport=websocket response with type "SELCN":
        EXPECTED: **status: "A"**
        """
        pass

    def test_004__collapse_any_sectiontype_accordion_and_trigger_the_outcome_status_change_to_outcomestatuscodes_for_the_event_in_collapsed_sectiontype_accordion_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Collapse any section/type accordion and trigger the outcome status change to **outcomeStatusCode="S"** for the event in collapsed section/type accordion
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events that belong to collapsed section/type accordion are received in WS -> ?EIO=3&transport=websocket response
        EXPECTED: * Updates are NOT received in WS due to unsubscription that was triggered
        """
        pass

    def test_005__expand_the_sectiontype_accordion_with_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Expand the section/type accordion with the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Only Price/Odds button of changed outcome is displayed immediately as greyed out and becomes disabled on <Sports> In-Play page but still displaying the price, the rest Price/Odds buttons of the same market remain not changed
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: * **status: "S"** attribute is received in response with type "SELCN"
        """
        pass

    def test_006__collapse_any_sectiontype_accordion_and_trigger_the_outcome_status_change_to_outcomestatuscodea_for_the_event_in_collapsed_sectiontype_accordion_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Collapse any section/type accordion and trigger the outcome status change to **outcomeStatusCode="A"** for the event in collapsed section/type accordion
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscriptions from updates for the events that belong to the collapsed section (Type accordion) are received in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscription that was triggered
        """
        pass

    def test_007__expand_the_sectiontype_accordion_with_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Expand the section/type accordion with the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Price/Odds button of changed outcome becomes active on the In-Play page and still displaying the price
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: * **status: "A"** attribute is received in response with type "SELCN"
        """
        pass

    def test_008__leave_the_in_play_page_and_trigger_the_outcome_status_change_to_outcomestatuscodes_for_the_live_event_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Leave the In-Play page and trigger the outcome status change to **outcomeStatusCode="S"** for the live event
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscription from updates for the event is received in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscriptions that were triggered in the previous step
        """
        pass

    def test_009__open_in_playpage_again_find_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Open In-Play page again, find the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Only Price/Odds button of changed outcome is displayed immediately as greyed out and becomes disabled on <Sports> In-Play page but still displaying the price, the rest Price/Odds buttons of the same market remain not changed
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: * **status: "S"** attribute is received in response with type "SELCN"
        """
        pass

    def test_010__leave_the_in_play_page_and_trigger_the_outcome_status_change_to_outcomestatuscodea_for_the_live_event_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Leave the In-Play page and trigger the outcome status change to **outcomeStatusCode="A"** for the live event
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Unsubscription from updates for the event is received in WS -> ?EIO=3&transport=websocket
        EXPECTED: * Updates are NOT received in WS due to unsubscriptions that were triggered in the previous step
        """
        pass

    def test_011__open_in_playpage_again_find_the_event_and_verify_its_outcomes_verify_updates_receiving_in_ws(self):
        """
        DESCRIPTION: * Open In-Play page again, find the event and verify its outcomes
        DESCRIPTION: * Verify updates receiving in WS
        EXPECTED: * Price/Odds button of changed outcome becomes active on the In-Play page and still displaying the price
        EXPECTED: * Subscriptions to updates for the events that belong to expanded section/type accordion occurs
        EXPECTED: * **status: "A"** attribute is received in response with type "SELCN"
        """
        pass

    def test_012_verify_the_outcome_status_change_to_outcomestatuscodes_before_the_application_is_opened(self):
        """
        DESCRIPTION: Verify the outcome status change to **outcomeStatusCode="S"** before the application is opened
        EXPECTED: If the application was not started/opened and Outcome status was changed, after opening application and In-Play page - 'Price/Odds' button with updated status will be shown there
        """
        pass

    def test_013_repeat_steps_1_12_for_events_from_upcoming_section(self):
        """
        DESCRIPTION: Repeat steps 1-12 for events from 'Upcoming' section
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_1_13_for_the_following_pages_home_page__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-13 for the following pages:
        DESCRIPTION: * Home page > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        EXPECTED: 
        """
        pass

    def test_015_for_desktoprepeat_steps_1_2_on_home_page_for_in_play__live_stream_section_for_both_switchers_sport_landing_page_for_in_play_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 1-2 on:
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers
        DESCRIPTION: * Sport Landing page for 'In-play' widget
        EXPECTED: 
        """
        pass
