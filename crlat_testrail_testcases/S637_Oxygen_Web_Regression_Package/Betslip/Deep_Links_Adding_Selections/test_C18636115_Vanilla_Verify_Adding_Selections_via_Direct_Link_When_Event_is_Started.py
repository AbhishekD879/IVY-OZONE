import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C18636115_Vanilla_Verify_Adding_Selections_via_Direct_Link_When_Event_is_Started(Common):
    """
    TR_ID: C18636115
    NAME: [Vanilla] Verify Adding Selections via Direct Link When Event is Started
    DESCRIPTION: This test case verifies how selections can be added to the Bet slip via direct link when event is started
    DESCRIPTION: **Jira tickets for non-Vanilla implementation (before OX101): ** BMA-6941 (Deeplink Multiple Selections Into Betslip)
    DESCRIPTION: **Jira tickets for Vanilla implementation (OX101): **
    DESCRIPTION: BMA-42727
    PRECONDITIONS: 1) To see detailed information about event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXX?translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: /betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: https://qa2.sports.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - use this link for testing this functionality on Oxygen application for adding multiple selections
    PRECONDITIONS: OR
    PRECONDITIONS: https://qa2.sports.coral.co.uk/betslip/add/XXXXXX - use this link for testing this functionality on Oxygen application for adding one selection
    PRECONDITIONS: NOTE:
    PRECONDITIONS: <Race> events should have: **isStarted=true** attribute
    PRECONDITIONS: <Sport> events should have: **isStarted=true, isMarketBetInRun = false** attributes and should not have **drilldownTagNames=EVFLAG_BL**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_choose_any_sport_events_on_site_server_which_are_started_and_live_served_withisstartedtrueismarketbetinrun__true_anddrilldowntagnamesevflag_bl_bet_in_play_list_attributes(self):
        """
        DESCRIPTION: Choose any <Sport> event(s) on Site Server which are started and Live Served (with **isStarted=true**, **isMarketBetInRun = true** and **drilldownTagNames=EVFLAG_BL** (Bet in Play list) attributes)
        EXPECTED: 
        """
        pass

    def test_003_enter_direct_url_with_valid_outcome_ids_from_started_live_served_events_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) from started Live Served event(s) in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are shown in the Bet Slip
        EXPECTED: 3.  No errors are shown for started Live Served <Sport> events, they are shown as regular selections in the bet slip
        EXPECTED: 4.  Corresponding 'Multiples' selections are present and shown correctly (if available)
        """
        pass

    def test_004_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_005_choose_any_sport_events_on_site_server_which_are_started_and_not_live_served_with_isstartedtrue_ismarketbetinrun__false_attributes_and_nodrilldowntagnamesevflag_bl_attribute(self):
        """
        DESCRIPTION: Choose any <Sport> event(s) on Site Server which are started and NOT Live Served (with **isStarted=true**, **isMarketBetInRun = false** attributes and **NO drilldownTagNames=EVFLAG_BL** attribute)
        EXPECTED: 
        """
        pass

    def test_006_enter_direct_url_with_valid_outcome_ids_from_started_not_live_served_sport_events_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) from started NOT Live Served <Sport> event(s) in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed info are present
        EXPECTED: 3.  All buttons, fields etc. are greyed out and disabled
        EXPECTED: 4.  Error message is shown on the Bet Slip for each selection from started event(s):
        EXPECTED: **'Event Has Already Started.' / 'The Event/Market/Outcome Has Been Suspended.'** (error message text depends on what comes in response from server - check error message in the dev console)
        EXPECTED: **From OX99**
        EXPECTED: Messages:
        EXPECTED: Coral:
        EXPECTED: * 'Event Has Already Started.'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * 'Event Has Already Started.'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_007_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Place bet(s) for added selection(s)
        EXPECTED: It is impossible to place bet on any selection from started events
        """
        pass

    def test_008_choose_any_race_events_on_site_server_which_are_started_withisstartedtrue_attribute(self):
        """
        DESCRIPTION: Choose any <Race> event(s) on Site Server which are started (with **isStarted=true** attribute)
        EXPECTED: 
        """
        pass

    def test_009_enter_direct_url_with_valid_outcome_ids_from_started_not_live_served_sport_events_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) from started NOT Live Served <Sport> event(s) in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed info are present
        EXPECTED: 3.  All buttons, fields etc. are greyed out and disabled
        EXPECTED: 4.  Error message is shown on the Bet Slip for each selection from started event(s):
        EXPECTED: **'Event Has Already Started.' / 'The Event/Market/Outcome Has Been Suspended.'** (error message text depends on what comes in response from server - check error message in the dev console)
        EXPECTED: **From OX99**
        EXPECTED: Messages:
        EXPECTED: Coral:
        EXPECTED: * 'Event Has Already Started.'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * 'Event Has Already Started.'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_010_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Place bet(s) for added selection(s)
        EXPECTED: It is impossible to place bet on any selection from started events
        """
        pass

    def test_011_repeat_steps__1_10_for_justone_outcome_idin_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-10 for just **ONE outcome id** in direct URL
        EXPECTED: 
        """
        pass
