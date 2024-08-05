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
class Test_C29095_Verify_Adding_Selections_via_Direct_Link(Common):
    """
    TR_ID: C29095
    NAME: Verify Adding Selections via Direct Link
    DESCRIPTION: This test case verifies how one/multiple single selections can be added to the Bet slip via direct link
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: BMA-6941 (Deeplink Multiple Selections Into Betslip)
    DESCRIPTION: BMA-10079 Affiliate Tracking. Adding selections to the desktop and tablet betslip
    DESCRIPTION: AUTOTEST [C527785]
    DESCRIPTION: AUTOTEST [C1501914]
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

    def test_002_choose_any_sport_events_on_site_server(self):
        """
        DESCRIPTION: Choose any <Sport> event(s) on Site Server
        EXPECTED: 
        """
        pass

    def test_003_enter_direct_url_with_active_outcome_ids__outcomestatuscode_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are shown in the Bet Slip
        EXPECTED: 3.  Corresponding 'Multiples'/('Forecasts/Tricasts' before OX 98) selections are present and shown correctly (if available)
        EXPECTED: 4.  Numeric keyboard with 'quick stakes' buttons are shown if one selection was added
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
        EXPECTED: 6.  Numeric keyboard with 'quick stakes' buttons are shown if one selection was added
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
        EXPECTED: 5.  Numeric keyboard with quick stakes' buttons are shown if one selection was added
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
        EXPECTED: 4.  Corresponding 'Multiples'/('Forecasts/Tricasts' before OX 98) selections are present and shown correctly within bet slip (if available)
        EXPECTED: 5.  Numeric keyboard with 'quick stakes' buttons are shown if one selection was added
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
