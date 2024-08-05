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
class Test_C18636114_Vanilla_Verify_Adding_the_Same_Selections_Several_Times_via_Direct_Link(Common):
    """
    TR_ID: C18636114
    NAME: [Vanilla] Verify Adding the Same Selections Several Times via Direct Link
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

    def test_002_choose_any_sportrace_events_on_site_server(self):
        """
        DESCRIPTION: Choose any <Sport>/<Race> event(s) on Site Server
        EXPECTED: 
        """
        pass

    def test_003_enter_direct_url_with_valid_outcome_ids_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) in address bar -> press Enter key
        EXPECTED: Bet Slip with bet details is opened automatically
        EXPECTED: Entered selection(s) are added to the Bet Slip
        """
        pass

    def test_004_add_the_same_selections_to_the_bet_slip_via_direct_linkin_the_direct_url_enter_the_same_outcome_ids(self):
        """
        DESCRIPTION: Add the same selection(s) to the Bet Slip via direct link:
        DESCRIPTION: in the direct URL enter the same outcome id('s)
        EXPECTED: Bet Slip is opened automatically
        EXPECTED: Same selection(s) are present in the Bet Slip (they are not doubled)
        """
        pass

    def test_005_reload_bet_slip_page(self):
        """
        DESCRIPTION: Reload Bet Slip page
        EXPECTED: Same added selection(s) are present in the Bet Slip
        """
        pass

    def test_006_try_to_add_the_same_selections_several_times_via_direct_link(self):
        """
        DESCRIPTION: Try to add the same selection(s) several times via direct link
        EXPECTED: No matter how many times the same selection(s) are added to the Bet Slip -> Same added the first time selection(s) are present in the Bet Slip
        """
        pass

    def test_007_place_a_bet_for_added_selections(self):
        """
        DESCRIPTION: Place a bet for added selection(s)
        EXPECTED: Bet is placed successfully
        EXPECTED: User account is decreased only by total amount which was entered in a stake fields
        """
        pass

    def test_008_repeat_steps__1_7_for_justone_outcome_idin_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-7 for just **ONE outcome id** in direct URL
        EXPECTED: 
        """
        pass
