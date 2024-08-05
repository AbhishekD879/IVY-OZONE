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
class Test_C29099_Verify_Adding_Selections_via_Direct_Link_when_Bet_Slip_is_NOT_Empty(Common):
    """
    TR_ID: C29099
    NAME: Verify Adding Selections via Direct Link when Bet Slip is NOT Empty
    DESCRIPTION: This test case verifies how selections will be added to the Bet Slip if it already contains selections in it
    DESCRIPTION: **Jira tickets: **BMA-6941 (Deeplink Multiple Selections Into Betslip)
    PRECONDITIONS: **1)** To see detailed information about event use link:
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

    def test_002_add_several_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add several selections to the Bet Slip
        EXPECTED: Bet Slip counter is increased
        """
        pass

    def test_003_choose_any_sport__race_events_on_the_site_server(self):
        """
        DESCRIPTION: Choose any <Sport> / <Race> event(s) on the Site Server
        EXPECTED: 
        """
        pass

    def test_004_enter_direct_urlwith_validoutcome_ids_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  Selection(s) which were added directly are shown in the Bet Slip
        EXPECTED: 3.  Selections which were added previously are shown correctly
        EXPECTED: 4.  Corresponding 'Multiples'(/'Forecasts/Tricasts' only to OX 96) selections are present and shown correctly (if available)
        """
        pass

    def test_005_go_to_the_homepage____verify_bet_slip_icon(self):
        """
        DESCRIPTION: Go to the homepage - > verify Bet Slip icon
        EXPECTED: Bet Slip counter is equal to the quantity of selections in the Bet Slip
        """
        pass

    def test_006_add_the_max_allowed_quantity_of_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add the max allowed quantity of selections to the Bet Slip
        EXPECTED: Bet Slip counter in increased by value added to the Bet Slip
        """
        pass

    def test_007_try_to_add_one_or_more_selections_via_direct_link(self):
        """
        DESCRIPTION: Try to add one or more selections via direct link
        EXPECTED: 1. Bet Slip is opened automatically
        EXPECTED: 2. Error message is shown: **'Maximum number of selections allowed on betslip is <max_bet number>'**
        EXPECTED: 3. Selection(s) are NOT added to the Bet Slip
        """
        pass

    def test_008_repeat_steps__1_7_for_justone_outcome_idin_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-7 for just **ONE outcome id** in direct URL
        EXPECTED: 
        """
        pass
