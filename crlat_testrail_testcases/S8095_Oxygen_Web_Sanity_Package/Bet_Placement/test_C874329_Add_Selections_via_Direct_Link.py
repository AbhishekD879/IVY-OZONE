import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C874329_Add_Selections_via_Direct_Link(Common):
    """
    TR_ID: C874329
    NAME: Add Selections via Direct Link
    DESCRIPTION: This test case verifies how one/multiple single selections can be added to the Bet slip via direct link
    DESCRIPTION: AUTOTESTS [C47660470]
    PRECONDITIONS: **In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: {invictusAppDomain.com}/betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - *use this link for testing this functionality on Oxygen application for adding multiple selections***
    PRECONDITIONS: ***OR***
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX - *use this link for testing this functionality on Oxygen application for adding one selection***
    PRECONDITIONS: To find selection Id type 'Buildbet' in Network
    """
    keep_browser_open = True

    def test_001_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1. Oxygen app with Bet Slip page is opened
        EXPECTED: 2.  Added selection(s) are shown in the Bet Slip
        EXPECTED: 3.  Corresponding 'Multiples'/(Before OX98'Forecasts/Tricasts') selections are present and shown correctly (if available)
        EXPECTED: 4.  Numeric keyboard with 'quick stakes' buttons are shown if one selection was added (before OX100)
        """
        pass

    def test_002_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_003_choose_any_race_event_with_pricetypecodessplp(self):
        """
        DESCRIPTION: Choose any <Race> event with **'priceTypeCodes'**='SP,LP'
        EXPECTED: 
        """
        pass

    def test_004_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) are shown in the Bet Slip
        EXPECTED: 3.  'LP' part of added selection(s) are shown by default
        EXPECTED: 4.  Dropdown control which allows switching between LP and SP parts is shown for each selection
        EXPECTED: 5.  Corresponding 'Multiples'/(Before OX98: 'Forecasts/Tricasts' selections are present and shown correctly within bet slip (if available)
        EXPECTED: 6.  Numeric keyboard with 'quick stakes' buttons are shown if one selection was added
        """
        pass

    def test_005_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_006_choose_race_event_with_pricetypecodessp(self):
        """
        DESCRIPTION: Choose <Race> event with **'priceTypeCodes'**='SP'
        EXPECTED: 
        """
        pass

    def test_007_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are displayed
        EXPECTED: 3.  'SP' price is shown for such selections
        EXPECTED: 4.  Corresponding 'Multiples'/(Before OX98 'Forecasts/Tricasts' selections are present and shown correctly within bet slip (if available)
        EXPECTED: 5.  Numeric keyboard with quick stakes' buttons are shown if one selection was added (before OX 100)
        """
        pass

    def test_008_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass
