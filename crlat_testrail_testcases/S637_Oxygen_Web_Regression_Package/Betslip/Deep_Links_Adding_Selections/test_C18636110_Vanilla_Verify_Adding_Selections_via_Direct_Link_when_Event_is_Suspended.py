import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C18636110_Vanilla_Verify_Adding_Selections_via_Direct_Link_when_Event_is_Suspended(Common):
    """
    TR_ID: C18636110
    NAME: [Vanilla] Verify Adding Selections via Direct Link when Event is Suspended
    DESCRIPTION: This test case verifies how selections can be added to the Bet slip via direct link when event is suspended
    DESCRIPTION: **Jira tickets for non-Vanilla implementation (before OX101): ** BMA-6941 (Deeplink Multiple Selections Into Betslip)
    DESCRIPTION: **Jira tickets for Vanilla implementation (OX101): ** BMA-42727
    PRECONDITIONS: 1) To see detailed information about event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXX?translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: /betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: https://qa2.sports.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - use this link for testing this functionality on sportsbook for adding multiple selections
    PRECONDITIONS: OR
    PRECONDITIONS: https://qa2.sports.coral.co.uk/betslip/add/XXXXXX - use this link for testing this functionality on sportsbook for adding one selection
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_choose_any_sport__race_events_on_site_server_which_are_suspended__eventstatuscode_s(self):
        """
        DESCRIPTION: Choose any <Sport> / <Race> event(s) on Site Server which are suspended ( **eventStatusCode** ='S')
        EXPECTED: 
        """
        pass

    def test_003_enter_direct_urlwith_valid_outcome_ids_fro_suspended_eventseventstatuscodesin_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) fro suspended event(s) **(eventStatusCode='S')** in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed info are present
        EXPECTED: 3.  All buttons, fields etc. are grayed out and disabled
        EXPECTED: 4.  Error message is shown on the Bet Slip for each selection from suspended event(s):
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'*
        """
        pass

    def test_004_place_bets_for_this_selections(self):
        """
        DESCRIPTION: Place bet(s) for this selection(s)
        EXPECTED: It is impossible to place bet on any selection from suspended events
        """
        pass

    def test_005_repeat_steps__3___4_for_several_sportsraces(self):
        """
        DESCRIPTION: Repeat steps # 3 - 4 for several <Sports>/<Races>
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps__1_5_for_justone_outcome_idin_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-5 for just **ONE outcome id** in direct URL
        EXPECTED: 
        """
        pass
