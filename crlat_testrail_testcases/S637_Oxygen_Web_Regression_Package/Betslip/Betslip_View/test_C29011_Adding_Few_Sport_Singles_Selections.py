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
class Test_C29011_Adding_Few_Sport_Singles_Selections(Common):
    """
    TR_ID: C29011
    NAME: Adding  Few <Sport> Singles Selections
    DESCRIPTION: This test case verifies how several single selections should be added to the Bet Slip
    PRECONDITIONS: 1.User is logged out
    PRECONDITIONS: 2.To retrieve information from the Site Server use the following steps:
    PRECONDITIONS: To get class IDs and type IDs for Football sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: - XX- Category ID (Sport ID)
    PRECONDITIONS: - X.XX - current supported version of OpenBet release
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: To get a list of events for types use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: - XXX - the type ID
    PRECONDITIONS: - X.XX - current supported version of OpenBet release
    PRECONDITIONS: - ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH)
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. To get a list of events' details use link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: - XXXX is the event ID
    PRECONDITIONS: - X.XX - current supported version of OpenBet release
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: - 'name' to see the event name
    PRECONDITIONS: - 'name' on the market level - to see the market name
    PRECONDITIONS: - 'name' on the outcome level - to see selection name
    PRECONDITIONS: - 'livePriceNum'/'livePriceDen' in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: - 'priceDec' in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True

    def test_001_tapsport_icon_on_the_sports_menu_ribbon_and_proceed_to_edp(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon and proceed to EDP
        EXPECTED: <Sport> EDP is opened
        """
        pass

    def test_002_add_few_selections_from_the_same_market(self):
        """
        DESCRIPTION: Add few selections from the same market
        EXPECTED: 1.  Selected price / odds buttons are highlighted in green
        EXPECTED: 2.  Betslip counter is increased to value which is equal to quantity of added selections
        """
        pass

    def test_003_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip with bets details is opened
        """
        pass

    def test_004_verify_selections_displaying(self):
        """
        DESCRIPTION: Verify selections displaying
        EXPECTED: All single selections are displayed
        """
        pass

    def test_005_verify_selections_information(self):
        """
        DESCRIPTION: Verify selections information
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name ( **'name'** attribute on event level)
        EXPECTED: - Format for Sports: 'Team_A v/vs Team_B'
        EXPECTED: 4.  Selection odds ('livePriceNum'/'livePriceDen' attributes in fraction format OR 'price Dec' in decimal format)
        """
        pass

    def test_006_verify_remove_all_linklogin__place_bet_button(self):
        """
        DESCRIPTION: Verify 'REMOVE ALL' link/'LOGIN & PLACE BET' button
        EXPECTED: 1. 'REMOVE ALL' link is present on the right at the top of Betslip
        EXPECTED: 2.'LOGIN & PLACE BET' button is present at the bottom of the page and always visible
        """
        pass

    def test_007_addmax_num_of_selection_to_bet_slip_eg_3max_num__max_number_of_singles_selection_iscms_configurable_system_configuration__maxbetnumber_value(self):
        """
        DESCRIPTION: Add <Max_num> of selection to Bet Slip (eg. 3)
        DESCRIPTION: Max_num - Max number of singles selection is CMS configurable (System configuration -> maxBetNumber value)
        EXPECTED: Max number of selections is added to Betslip
        """
        pass

    def test_008_try_to_add_max_num_plus_1selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Try to add <Max_num> + 1 selection to the Bet Slip
        EXPECTED: 1.  Ability to add selection is restricted
        EXPECTED: 2.  Pop up dialogue with error message: "Maximum number of selections allowed on betslip is < max number of singles selection>" appears
        """
        pass

    def test_009_close_the_pop_up_and_unselect_1_selection_on_the_event_page(self):
        """
        DESCRIPTION: Close the pop up and unselect 1 selection on the event page
        EXPECTED: 1.  Selection becomes unselected (not highlighted)
        EXPECTED: 2.  Bet Slip counter is decreased by 1
        """
        pass

    def test_010_log_in_to_the_application_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Log in to the application and Repeat steps №2-10
        EXPECTED: Results are the same
        EXPECTED: Instead 'LOGIN & PLACE BET' button 'PLACE BET' button is shown
        """
        pass

    def test_011_make_selections_from_different_markets(self):
        """
        DESCRIPTION: Make selections from different markets
        EXPECTED: - All single selections are displayed in singles section (with selections information from step 5)
        EXPECTED: - Multiples are displayed in Multiples section (below singles)
        """
        pass
