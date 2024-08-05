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
class Test_C29105_Adding_Selections_via_Direct_Link_on_Desktop_Tablet(Common):
    """
    TR_ID: C29105
    NAME: Adding Selections via Direct Link on Desktop/Tablet
    DESCRIPTION: This test case verifies adding Selections via Direct Link on Desktop/Tablet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-10079
    DESCRIPTION: Affiliate Tracking. Adding selections to the desktop and tablet betslip
    DESCRIPTION: AUTOTEST [C9697670]
    PRECONDITIONS: 1) In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: {invictusAppDomain.com}/#/betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: https://invictus.coral.co.uk/#/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - use this link for testing this functionality on Invictus application for adding multiple selections
    PRECONDITIONS: OR
    PRECONDITIONS: https://invictus.coral.co.uk/#/betslip/add/XXXXXX - use this link for testing this functionality on Invictus application for adding one selection
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_choose_ane_sport_event_on_siteserver(self):
        """
        DESCRIPTION: Choose ane <Sport> event on SiteServer
        EXPECTED: 
        """
        pass

    def test_003_enter_direct_url_with_active_outcome_ids_outcomestatuscodea_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ('outcomeStatusCode'='A') in address bar -> press Enter key
        EXPECTED: 1.  Added via Direct link Outcome is displayed in Betslip module
        EXPECTED: 2.  Users stays on the same page and is NOT redirected to Betslip mobile page version
        EXPECTED: 3.  Added selection(s) with all detailed information is shown in the Bet Slip
        EXPECTED: 4.  Corresponding 'Multiples'(/'Forecasts/Tricasts' before OX 98)  selections are present and shown correctly (if available)
        """
        pass

    def test_004_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_005_repeat_steps__2___4_for_several_sports(self):
        """
        DESCRIPTION: Repeat steps # 2 - 4 for several <Sports>
        EXPECTED: 
        """
        pass

    def test_006_choose_any_race_event_withpricetypecodes_splp(self):
        """
        DESCRIPTION: Choose any <Race> event with **'priceTypeCodes'** ='SP,LP'
        EXPECTED: 
        """
        pass

    def test_007_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Added via Direct link selection(s) are displayed in Betslip
        EXPECTED: 2.  User stays on the same page and is NOT redirected to Betslip mobile page version
        EXPECTED: 3.  Added selection(s) with all detailed information are displayed
        EXPECTED: 4.  'LP' part of added selection(s) are shown by default
        EXPECTED: 5.  Dropdown control which allows switching between LP and SP parts is shown for each selection
        EXPECTED: 6.  Corresponding 'Multiples'/('Forecasts/Tricasts' before OX 98) selections are present and shown correctly within bet slip (if available)
        """
        pass

    def test_008_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_009_choose_race_event_withpricetypecodes_sp(self):
        """
        DESCRIPTION: Choose <Race> event with **'priceTypeCodes'** ='SP'
        EXPECTED: 
        """
        pass

    def test_010_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Added via Direct link selection(s) are displayed in Betslip
        EXPECTED: 2.  User stays on the same page and is NOT redirected to Betslip mobile page version
        EXPECTED: 3.  'SP' price is shown for such selections
        EXPECTED: 4.  Corresponding 'Multiples'/('Forecasts/Tricasts' before OX 98)selections are present and shown correctly within bet slip (if available)
        """
        pass

    def test_011_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_012_choose_race_event_withpricetypecodes_lp(self):
        """
        DESCRIPTION: Choose <Race> event with **'priceTypeCodes'** ='LP'
        EXPECTED: 
        """
        pass

    def test_013_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Added via Direct link selection(s) are displayed in Betslip
        EXPECTED: 2.  User stays on the same page and is NOT redirected to Betslip mobile page version
        EXPECTED: 3.  'LP' price/odds are shown for such selections
        EXPECTED: 4.  Corresponding 'Multiples' (/'Forecasts/Tricasts' before OX 98) selections are present and shown correctly within bet slip (if available)
        """
        pass

    def test_014_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass
