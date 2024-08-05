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
class Test_C10530953_Verify_Event_Data_on_Outright_page(Common):
    """
    TR_ID: C10530953
    NAME: Verify Event Data on Outright page
    DESCRIPTION: This test case verifies event data on Outright page and EDP(Event Details Page) for an Outright event
    PRECONDITIONS: 1) Following Tabs should be enabled in Sports Pages - SPORT CATEGORIES - #TIER_2_SPORT_NAME within CMS: Matches, Competitions, Outrights
    PRECONDITIONS: 2) At least 1 LIVE 'Outright' event should be created and active for the chosen TIER_2_SPORT
    PRECONDITIONS: 3) Aforementioned event should have at least 1 market being set for it (Primary Market is 'Outright') with a 'CashOut Available' option being enabled for it.
    PRECONDITIONS: ['Event', 'Type', 'Class', 'Category' within which the market exists should all have 'CashOut Available' option being enabled; 'Market Template' of the chosen market should also have CashOut Available' option being enabled]
    PRECONDITIONS: 4) Load Oxygen app
    PRECONDITIONS: 5) Navigate to a chosen 'Tier 2' Sports Landing Page
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_switch_to_outrights_tab(self):
        """
        DESCRIPTION: Switch to 'Outrights' tab
        EXPECTED: League dropdown(lane) is shown below the 'Tabs' lane
        EXPECTED: All League dropdowns(lanes) are collapsed by default with a '#DOWN_ARROW' element being shown in the right side of the dropdown(lane)
        EXPECTED: Name of each League dropdown has a following structure: '#SPORT_NAME - #LEAGUE_NAME
        """
        pass

    def test_002_expand_the_league_that_contains_the_event_created_in_the_preconditions(self):
        """
        DESCRIPTION: Expand the League that contains the event created in the preconditions
        EXPECTED: League dropdown(lane) becomes expanded
        EXPECTED: '#DOWN_ARROW' element is no longer shown in the right side of the dropdown(lane)
        EXPECTED: Event cards are shown under the league lane(dropdown)
        """
        pass

    def test_003_verify_outrights_event_card_of_the_event_created_in_the_preconditions(self):
        """
        DESCRIPTION: Verify 'Outrights' Event card of the event created in the preconditions
        EXPECTED: Event name corresponds to '**name**' attribute
        EXPECTED: Event name is shown on it left side
        EXPECTED: '#RIGHT_ARROW' element shown on its right side
        EXPECTED: Time and Date is not shown on the 'Outrights' Event card
        EXPECTED: 'Show All' button is not shown on the 'Outrights' Event card
        """
        pass

    def test_004_clicktap_on_event_card_of_the_event_created_in_the_preconditions(self):
        """
        DESCRIPTION: Click(Tap) on event card of the event created in the preconditions
        EXPECTED: 'Outright' Event details page is opened
        EXPECTED: All Market dropdowns(lanes) are expanded by default with an '#UP_ARROW' element being shown before the 'Outright' text
        """
        pass

    def test_005_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: * It is displayed below the Event name
        EXPECTED: * Event start date corresponds to '**startTime**' attribute
        EXPECTED: * Event start date is shown in following format: ** HH:MM, ## MMM **
        EXPECTED: <HH:MM> is a 24 hour time range(i.e. 23:59)
        EXPECTED: <##> is the date integer value(i.e. 21, 31, 11)
        EXPECTED: <MMM> is the shortened name of the month(i.e. Mar, Apr, May)
        """
        pass

    def test_006_verify_live_label_presence(self):
        """
        DESCRIPTION: Verify 'LIVE' label presence
        EXPECTED: 'LIVE' label is shown on the left side of the Event Start time
        EXPECTED: Event should have following parameters in its backend response:
        EXPECTED: rawIsOffCode="Y" OR rawIsOffCode="-" AND isStarted="true"
        """
        pass

    def test_007_verify_cash_out_icon_presence(self):
        """
        DESCRIPTION: Verify 'Cash Out' icon presence
        EXPECTED: 'CASH OUT' icon is shown on the right side of the 'Market' dropdown(lane)
        """
        pass
