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
class Test_C18636112_Vanilla_Verify_Adding_Different_Selections_via_Direct_Link_Several_times(Common):
    """
    TR_ID: C18636112
    NAME: [Vanilla] Verify Adding Different Selections via Direct Link Several times
    DESCRIPTION: This test case verifies how selections which are added via direct link will be shown on the Bet Slip if add different selections several times
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
    PRECONDITIONS: https://qa2.sports.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - use this link for testing this functionality on sportsbook application for adding multiple selections
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

    def test_002_enter_direct_url_valid_outcome_ids_in_address_bar_including_active_and_suspendedstarted_ids___press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL valid outcome id('s) in address bar including active and suspended/started id('s) -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  All added selections are present
        EXPECTED: 3.  Active added selection(s) with all detailed information are shown in the Bet Slip correctly
        EXPECTED: 4.  Error message is shown on the Bet Slip for each suspended/started selection
        EXPECTED: 5.  Corresponding 'Multiples'/ selections formed from active outcomes are present and shown correctly (if available)
        """
        pass

    def test_003_go_back_to_the_homepage(self):
        """
        DESCRIPTION: Go back to the homepage
        EXPECTED: 
        """
        pass

    def test_004_repeat_step__2(self):
        """
        DESCRIPTION: Repeat step # 2
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Selection(s) which were added directly are shown in the Bet Slip
        EXPECTED: 3.  Selections which were added previously are shown correctly
        EXPECTED: 4.  Corresponding 'Multiples' selections formed from active outcomes are present and shown correctly (if available)
        """
        pass

    def test_005_log_in___place_bets_on_active_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) on active selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_006_repeat_steps__2___4for_several_sportsraces(self):
        """
        DESCRIPTION: Repeat steps # 2 - 4 for several <Sports>/<Races>
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps__1_6_for_justone_outcome_idin_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-6 for just **ONE outcome id** in direct URL
        EXPECTED: 
        """
        pass
