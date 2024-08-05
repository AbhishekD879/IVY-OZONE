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
class Test_C29096_Verify_Adding_Suspended_Selections_via_Direct_Link(Common):
    """
    TR_ID: C29096
    NAME: Verify Adding Suspended Selections via Direct Link
    DESCRIPTION: This test case verifies how suspended selections can be added to the Bet slip via direct link
    DESCRIPTION: **Jira tickets: **BMA-6941 (Deeplink Multiple Selections Into Betslip)
    PRECONDITIONS: **1)** To see detailed information about event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXX?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **2) **In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: {invictusAppDomain.com}/betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - *use this link for testing this functionality on Invictus application for adding multiple selections***
    PRECONDITIONS: ***OR***
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX - *use this link for testing this functionality on Invictus application for adding one selection***
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_choose_any_sport__race_events_on_site_server_which_have_suspended_outcomes__outcomestatuscode_s(self):
        """
        DESCRIPTION: Choose any <Sport> / <Race>  event(s) on Site Server which have suspended outcomes ( **outcomeStatusCode** ='S')
        EXPECTED: 
        """
        pass

    def test_003_enter_direct_url_with_suspended_outcome_ids__outcomestatuscode_sin_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with suspended outcome id('s) ( **outcomeStatusCode** ='S') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed info are present
        EXPECTED: 3.  All buttons, fields etc. are grayed out and disabled for suspended selections
        EXPECTED: 4.  Error message on red background is shown on the Bet Slip for each suspended selection:
        EXPECTED: **'Sorry, the Event/Market/Outcome Has Been Suspended.'** (error message text depends on what comes in response from server - check error message in the dev console)
        EXPECTED: **From OX99**
        EXPECTED: Message:
        EXPECTED: Coral:
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_004_place_bets_for_this_selections(self):
        """
        DESCRIPTION: Place bet(s) for this selection(s)
        EXPECTED: It is impossible to place bet on any suspended selection
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
