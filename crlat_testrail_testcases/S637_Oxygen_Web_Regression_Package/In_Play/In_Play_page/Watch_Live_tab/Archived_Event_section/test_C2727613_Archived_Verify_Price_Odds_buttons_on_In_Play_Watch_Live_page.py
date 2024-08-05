import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C2727613_Archived_Verify_Price_Odds_buttons_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727613
    NAME: [Archived]  Verify 'Price/Odds' buttons on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies 'Price/Odds' buttons on 'In-Play' page > 'Watch Live' tab
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 1. Load application and log in
    PRECONDITIONS: 2. Navigate to 'In-pLay' page > 'Watch Live' tab > 'Live now' section
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * For 'Outrights'/'Races' events Price/Odds buttons are NOT available.
    PRECONDITIONS: * For DESKTOP: 'Price/Odds' button size depends on screen resolution (see https://ladbrokescoral.testrail.com/index.php?/cases/view/1474609 test case).
    """
    keep_browser_open = True

    def test_001_verify_data_of_priceodds_buttons_for_verified_event(self):
        """
        DESCRIPTION: Verify data of 'Price/Odds' buttons for verified event
        EXPECTED: *   'Price/Odds' corresponds to the 'priceNum/priceDen' if eventStatusCode="A" in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the 'priceDec' if eventStatusCode="A" in decimal format
        EXPECTED: *   Disabled 'Prcie/Odds' button is displayed with  'priceNum/priceDen' (for fractional format)  or 'priceDec' (for Decimal format if eventStatusCode="S"
        """
        pass

    def test_002_verify_priceodds_buttons_for_2_way_market(self):
        """
        DESCRIPTION: Verify 'Price/Odds' buttons for 2-Way Market
        EXPECTED: For 2-way primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away
        """
        pass

    def test_003_verify_priceodd_buttons_for_3_way_market(self):
        """
        DESCRIPTION: Verify 'Price/Odd' buttons for 3-Way Market
        EXPECTED: For 3-way primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home
        EXPECTED: *   outcomeMeaningMinorCode="D" is a Draw
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away
        """
        pass

    def test_004_add_selection_to_the_betslip_from_any_event_card(self):
        """
        DESCRIPTION: Add selection to the Betslip from any event card
        EXPECTED: * 'Price/Odd' button is displayed as selected
        EXPECTED: * Bet Slip counter is increased **For Mobile/Tablet**
        """
        pass

    def test_005_open_the_betslip_pagewidget(self):
        """
        DESCRIPTION: Open the Betslip page/widget
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_006_place_a_betby_clickingtapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by clicking/tapping 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_007_on_in_play_page__watch_live_tab_scroll_down_tillupcoming_eventssection(self):
        """
        DESCRIPTION: On 'In-play' page > 'Watch Live' tab scroll down till 'Upcoming events' section
        EXPECTED: The list of upcoming events is displayed on the page
        """
        pass

    def test_008_repeat_steps_1_6(self):
        """
        DESCRIPTION: Repeat steps #1-6
        EXPECTED: 
        """
        pass
