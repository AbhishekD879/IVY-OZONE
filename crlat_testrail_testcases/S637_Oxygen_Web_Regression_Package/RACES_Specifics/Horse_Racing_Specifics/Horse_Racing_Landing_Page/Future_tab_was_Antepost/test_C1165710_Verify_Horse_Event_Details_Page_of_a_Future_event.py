import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1165710_Verify_Horse_Event_Details_Page_of_a_Future_event(Common):
    """
    TR_ID: C1165710
    NAME: Verify Horse Event Details Page of a Future event
    DESCRIPTION: This test case verifies Horse Racing 'Future' event details page
    DESCRIPTION: AUTOTEST: [C1799749]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Horse Racing' landing page ('Future' tab is available)
    PRECONDITIONS: **OB configurations:**
    PRECONDITIONS: In order to create HR Future event use TI tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: 1) 'Antepost' check box should be checked on event level ('drilldownTagNames'='EVFLAG_AP' in SS response)
    PRECONDITIONS: with only one of the following:
    PRECONDITIONS: - 'Flat' check box should be checked on event level ('drilldownTagNames'='EVFLAG_FT' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'National Hunt' check box should be checked on event level ('drilldownTagNames'='EVFLAG_NH' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'International' check box should be checked on event level ('drilldownTagNames'='EVFLAG_IT' in SS response)
    PRECONDITIONS: 2) 'Antepost' checkbox should be checked on market level (Market Template= 'Outright' with name 'Ante-post')
    PRECONDITIONS: 3) Event start time should be in the future (like 2 days from now)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - If flags 'Flat', 'National Hunt', 'International' are not checked on event level, events are not displayed on the landing page
    PRECONDITIONS: - If flag 'Antepost' is not checked on market level, new designs do not apply on HR EDP
    PRECONDITIONS: - For checking info regarding event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: 2) To observe LiveServe changes make sure:
    PRECONDITIONS: - LiveServ updates is checked on 'Class' and 'Type' levels in TI
    PRECONDITIONS: - 'Bet In Play List' flag is checked on 'Event' level in TI
    PRECONDITIONS: - 'Bet in Running' is checked on 'Market' level in TI
    PRECONDITIONS: Request to check data on 'Future' tab:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-09T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-08-07T11:22:30.000Z&simpleFilter=event.classId:notIntersects:227&simpleFilter=event.drilldownTagNames:intersects:EVFLAG_FT,EVFLAG_IT,EVFLAG_NH&simpleFilter=event.drilldownTagNames:contains:EVFLAG_AP&externalKeys=event&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_clicktap_on_future_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Future' tab
        EXPECTED: - 'Future' tab is opened
        EXPECTED: - Switchers are displayed: 'Flat', 'National Hunt' and 'International' (if containing at least one event that meets Preconditions). Default opened switcher tab setups in CMS (if not the first switcher is opened by default)
        """
        pass

    def test_002_clicktap_on_one_of_the_available_events(self):
        """
        DESCRIPTION: Click/Tap on one of the available events
        EXPECTED: - Horse Racing Future event details page is opened
        EXPECTED: - isAntepost="true" attribute is received in response on market level
        EXPECTED: - 'Horse Racing' header with ***'Back' icon (navigates back to Future landing page, where first available switcher is opened)*** and ***'Bet Filter' link***
        EXPECTED: - 'Meetings' subheader: 'Horse Racing / [Event Name]' breadcrumb + 'Down' arrow
        EXPECTED: - Time switcher
        EXPECTED: - RaceCard area:
        EXPECTED: ANTEPOST
        EXPECTED: Event 'name' (taken from event 'name' from SS response)
        EXPECTED: Each Way: <nom>/<den> Odds - Places e.g. 1, 2, 3 (if available)
        EXPECTED: (For desktop): E/W: <nom>/<den> Places e.g. 1, 2, 3 (if available)
        EXPECTED: - List of selections with fractional Odds (taken from 'Antepost' market only, see Preconditions)
        EXPECTED: - Selections are ordered by prices (from lowest to highest), if prices are the same then by selection name in ascending order
        EXPECTED: On tablet/desktop:
        EXPECTED: - ANTEPOST Event 'name' (located on separate area below the time switcher)
        EXPECTED: - EACH WAY: <nom>/<den> ODDS - PlASES e.g. 1, 2, 3, CLASS # (if available) (located in the selections area)
        EXPECTED: On tablet:
        EXPECTED: - Selections are displayed in 2 columns view
        EXPECTED: On desktop:
        EXPECTED: - Selections are displayed in 3 columns view
        """
        pass

    def test_003_in_ti_change_price_for_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections with enabled liveServe updates (see Preconditions) > Navigate to application and observe changes
        EXPECTED: - Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they will change their color if price has decreased/increased
        EXPECTED: - Previous Odds, under Price/Odds button, are updated/added respectively
        """
        pass

    def test_004_in_ti_suspend_marketone_of_the_selections_with_enabled_liveserve_updates_see_preconditions__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend market/one of the selections with enabled liveServe updates (see Preconditions) > Navigate to application and observe changes
        EXPECTED: - ***If market is suspended:*** All Price/Odds buttons are displayed immediately as greyed out and become disabled for selected market but still displaying the prices
        EXPECTED: - ***If some selections are suspended:***
        EXPECTED: Price/Odds button of changed outcome are displayed immediately as greyed out and become disabled on Event Details page.
        EXPECTED: The rest outcomes and market tabs are not changed
        """
        pass

    def test_005_add_selections_with_lpsp_prices_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) with LP/SP prices to the Betslip
        EXPECTED: Added selection(s) is/are displayed within the 'Quick Bet' (for 1 selection)/'Betslip' (for more than 1 selection)
        """
        pass

    def test_006_enter_stake_for_a_singlemultipleforecasttricast_bet_manually_or_using_quick_stakes_buttons_tap_place_bet__in_quick_betbet_now_in_betslip(self):
        """
        DESCRIPTION: Enter 'Stake' for a Single/Multiple/Forecast/Tricast bet manually or using 'Quick Stakes' buttons> Tap 'Place Bet'  in 'Quick Bet'/'Bet Now' in Betslip
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: - Balance is decreased accordingly
        """
        pass

    def test_007_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_3___7(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and Repeat steps 3 - 7
        EXPECTED: All Prices/Odds are displayed in Decimal format
        """
        pass
