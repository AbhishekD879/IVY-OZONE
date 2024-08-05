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
class Test_C18636116_Vanilla_Verify_Adding_More_than_Allowed_Selections_via_Direct_Link(Common):
    """
    TR_ID: C18636116
    NAME: [Vanilla] Verify Adding More than Allowed Selections via Direct Link
    DESCRIPTION: This test case verifies how more than allowed number of selections can be added to the Bet slip via direct link
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
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_choose_any_sport__race_events_on_site_server(self):
        """
        DESCRIPTION: Choose any <Sport> / <Race>  event(s) on Site Server
        EXPECTED: 
        """
        pass

    def test_003_enter_direct_urlin_address_bar_with_total_amount_ofvalidoutcome_ids_that_exceeds_the_max_allowed_number_of_possible_selections_in_the_bet_slip___press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL in address bar with total amount of valid outcome id's that exceeds the max allowed number of possible selections in the Bet Slip -> press Enter key
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Just max allowed quantity of selections is shown in the bet slip (**first from the URL**) with all detailed info (rest outcomes are ignored and not added)
        EXPECTED: 3.  Error pop up is shown on the Bet Slip:
        EXPECTED: **'Maximum number of selections allowed on betslip is <max_bet number>'**
        """
        pass

    def test_004_repeat_step__3_for_several_sportsraces(self):
        """
        DESCRIPTION: Repeat step # 3 for several <Sports>/<Races>
        EXPECTED: 
        """
        pass
