import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C18636106_Vanilla_Verify_Adding_Selections_via_Direct_Link(Common):
    """
    TR_ID: C18636106
    NAME: [Vanilla] Verify Adding Selections via Direct Link
    DESCRIPTION: This test case verifies how one/multiple single selections can be added to the Bet slip via direct link
    DESCRIPTION: **Jira tickets for non-Vanilla implementation (before OX101): **
    DESCRIPTION: BMA-6941 (Deeplink Multiple Selections Into Betslip)
    DESCRIPTION: BMA-10079 Affiliate Tracking. Adding selections to the desktop and tablet betslip
    DESCRIPTION: AUTOTEST [C527785]
    DESCRIPTION: AUTOTEST [C1501914]
    DESCRIPTION: **Jira tickets for Vanilla implementation (OX101): **
    DESCRIPTION: BMA-42727
    PRECONDITIONS: **1)** To see detailed information about event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXX?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **2) **In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: /betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: **https://qa2.sports.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - *use this link for testing this functionality on Invictus application for adding multiple selections***
    PRECONDITIONS: ***OR***
    PRECONDITIONS: **https://qa2.sports.coral.co.uk/betslip/add/XXXXXX - *use this link for testing this functionality on Invictus application for adding one selection***
    """
    keep_browser_open = True

    def test_001_go_to_sportsbook_homepage_and_find_an_event_and_selection_that_you_would_like_to_add_via_direct_link(self):
        """
        DESCRIPTION: Go to sportsbook homepage and find an event and selection that you would like to add via direct link
        EXPECTED: Homepage is opened, event is chosen
        """
        pass

    def test_002_go_to_trading_interface_search_for_the_chosen_event_find_a_chosen_selection_and_copy_the_selection_idie_event_httpbackoffice_tst2coralcouktihierarchyevent9998916market_httpbackoffice_tst2coralcouktihierarchymarket148278565selection_httpbackoffice_tst2coralcouktihierarchyselection553383894_(self):
        """
        DESCRIPTION: Go to Trading Interface, search for the chosen event, find a chosen selection and copy the selection ID
        DESCRIPTION: (i.e. event: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/9998916
        DESCRIPTION: market: http://backoffice-tst2.coral.co.uk/ti/hierarchy/market/148278565
        DESCRIPTION: selection: http://backoffice-tst2.coral.co.uk/ti/hierarchy/selection/553383894 )
        EXPECTED: Selection ID is copied
        """
        pass

    def test_003_enter_direct_url_with_active_selection_id__outcomestatuscode_a_in_address_bar__press_enter_keyhttpsyour_environmentsportscoralcoukbetslipaddxxxxxxwhere_xxxxxx__selection_id(self):
        """
        DESCRIPTION: Enter direct URL with active Selection id ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        DESCRIPTION: https://your_environment.sports.coral.co.uk/betslip/add/XXXXXX
        DESCRIPTION: where XXXXXX = selection ID
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are shown in the Bet Slip
        EXPECTED: 3.  Corresponding 'Multiples' selections are present and shown correctly (if available)
        """
        pass

    def test_004_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_005_repeat_steps__1___4_for_several_sports(self):
        """
        DESCRIPTION: Repeat steps # 1 - 4 for several <Sports>
        EXPECTED: 
        """
        pass

    def test_006_choose_any_race_event_with_pricetypecodessplp(self):
        """
        DESCRIPTION: Choose any <Race> event with **'priceTypeCodes'**='SP,LP'
        EXPECTED: 
        """
        pass

    def test_007_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are displayed
        EXPECTED: 3.  'LP' part of added selection(s) are shown by default
        EXPECTED: 4.  Dropdown control which allows switching between LP and SP parts is shown for each selection
        EXPECTED: 5.  Corresponding 'Multiples' ('Forecasts/Tricasts' before OX 98) selections are present and shown correctly within bet slip (if available)
        """
        pass

    def test_008_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_009_choose_race_event_with_pricetypecodessp(self):
        """
        DESCRIPTION: Choose <Race> event with **'priceTypeCodes'**='SP'
        EXPECTED: 
        """
        pass

    def test_010_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are displayed
        EXPECTED: 3.  'SP' price is shown for such selections
        EXPECTED: 4.  Corresponding 'Multiples' ('Forecasts/Tricasts' before OX 98) selections are present and shown correctly within bet slip (if available)
        """
        pass

    def test_011_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_012_choose_race_event_with_pricetypecodeslp(self):
        """
        DESCRIPTION: Choose <Race> event with **'priceTypeCodes'**='LP'
        EXPECTED: 
        """
        pass

    def test_013_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are displayed
        EXPECTED: 3.  'LP' price/odds are shown for such selections
        EXPECTED: 4.  Corresponding 'Multiples selections are present and shown correctly within bet slip (if available)
        """
        pass

    def test_014_log_in___place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        pass

    def test_015_repeat_steps__1_14_for_just_one_outcome_id_in_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-14 for just **ONE outcome id** in direct URL
        EXPECTED: 
        """
        pass
