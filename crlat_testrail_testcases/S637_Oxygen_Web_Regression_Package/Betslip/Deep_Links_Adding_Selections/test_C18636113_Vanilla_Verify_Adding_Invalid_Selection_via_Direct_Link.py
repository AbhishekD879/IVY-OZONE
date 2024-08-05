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
class Test_C18636113_Vanilla_Verify_Adding_Invalid_Selection_via_Direct_Link(Common):
    """
    TR_ID: C18636113
    NAME: [Vanilla] Verify Adding Invalid Selection via Direct Link
    DESCRIPTION: This test case describes what should be shown if user enters invalid outcome id in the direct link
    PRECONDITIONS: **1)** To see detailed information about event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXX?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **2) **In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: {invictusAppDomain.com}/betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - *use this link for adding multiple selections***
    PRECONDITIONS: ***OR***
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX - *use this link for adding one selection***
    """
    keep_browser_open = True

    def test_001_enter_direct_url_for_adding_selection_to_the_bet_slip_but_instead_of_outcome_id_enter_one_invalid_id(self):
        """
        DESCRIPTION: Enter direct URL for adding selection to the Bet Slip, but instead of outcome id enter one invalid id
        EXPECTED: User sees an error message:
        EXPECTED: **'One or more of your selections are currently unavailable'**
        """
        pass

    def test_002_enter_direct_url_for_adding_selections_to_the_bet_slip_but_enter_several_invalid_ids(self):
        """
        DESCRIPTION: Enter direct URL for adding selections to the Bet Slip, but enter several invalid id's
        EXPECTED: User sees an error message:
        EXPECTED: **'One or more of your selections are currently unavailable'**
        """
        pass

    def test_003_enter_direct_url_for_adding_selections_to_the_bet_slip_but_enter_invalid_ids_and_valid_ids(self):
        """
        DESCRIPTION: Enter direct URL for adding selections to the Bet Slip, but enter invalid id's and valid id('s)
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  **Only valid added selection(s)** with all detailed info are shown
        EXPECTED: 3.  Invaid id's are ignored
        """
        pass
