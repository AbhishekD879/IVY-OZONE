import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C59918233_CMS_configuration_of_static_blocks_for_My_Bets_Footer_and_Live_Stats_Tracking_pop_up(Common):
    """
    TR_ID: C59918233
    NAME: CMS configuration of static blocks for My Bets Footer and Live Stats Tracking pop-up
    DESCRIPTION: This test case verifies the ability to change the description text, logo and pop-up content of My Bets Footer and Live Stats Tracking pop-up in CMS Static blocks
    PRECONDITIONS: In CMS
    PRECONDITIONS: Load CMS and log in
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: Create a Football event in OpenBet (TI)
    PRECONDITIONS: Request Banach side to map data including Player Bets markets
    PRECONDITIONS: Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: Place at least 1 bet with few markets (from BYB tab) on created Football event
    PRECONDITIONS: In OpenBet (TI) start the event (Is OFF = yes)
    """
    keep_browser_open = True

    def test_001_go_to_the_static_blocks_in_cms(self):
        """
        DESCRIPTION: Go to the Static blocks in CMS
        EXPECTED: Opta Disclaimer short text and Opta Disclaimer Pop-up blocks are present in the list
        """
        pass

    def test_002_observe_opta_disclaimer_short_text_my_bets_footer_block(self):
        """
        DESCRIPTION: Observe Opta disclaimer short text (My Bets Footer) block
        EXPECTED: Opta disclaimer short text (My Bets Footer) block contains of:
        EXPECTED: * Title: Opta disclaimer short text
        EXPECTED: * Description text : Statistical totals are always subject to change.
        """
        pass

    def test_003_edit_html_markup_field_in_opta_disclaimer_short_text_my_bets_footer_blocksave_changes(self):
        """
        DESCRIPTION: Edit 'Html Markup' field in Opta disclaimer short text (My Bets Footer) block
        DESCRIPTION: Save changes
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_004_go_to_app___open_my_betsopen_bets_tabobserve_my_bets_footer(self):
        """
        DESCRIPTION: Go to app -> open My Bets/Open Bets tab
        DESCRIPTION: Observe My Bets Footer
        EXPECTED: Changes made for the Opta disclaimer short text (My Bets Footer) static block in CMS are reflected
        """
        pass

    def test_005_go_back_to_the_static_blocks_in_cmsobserve_opta_disclaimer_popup_block(self):
        """
        DESCRIPTION: Go back to the Static blocks in CMS
        DESCRIPTION: Observe Opta Disclaimer Popup block
        EXPECTED: Opta Disclaimer Popup block contains of:
        EXPECTED: * Pop-up title : Opta Disclaimer Popup
        EXPECTED: * Pop-up description: "Live Statistics are sourced from our data provider Opta and are to be used as a guide only. Statistical totals are always subject to change, and in some scenarios may be altered after the event has finished."
        """
        pass

    def test_006_edit_html_markup_field_in_opta_disclaimer_popup_blocksave_changes(self):
        """
        DESCRIPTION: Edit 'Html Markup' field in Opta Disclaimer Popup block
        DESCRIPTION: Save changes
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_007_go_to_app___open_my_betsopen_bets_tabtap_on_the_see_more_buttonobserve_live_stats_tracking_pop_up(self):
        """
        DESCRIPTION: Go to app -> open My Bets/Open Bets tab
        DESCRIPTION: Tap on the 'See More' button
        DESCRIPTION: Observe Live Stats Tracking pop-up
        EXPECTED: Changes made for the Opta Disclaimer Popup static block in CMS are reflected
        """
        pass

    def test_008_go_to_image_manager_in_cmssearch_for_opta_logo(self):
        """
        DESCRIPTION: Go to Image Manager in CMS
        DESCRIPTION: Search for Opta logo
        EXPECTED: * Opta Logo svg icon is upload (in additional sprite)
        EXPECTED: ![](index.php?/attachments/get/119601431)
        """
        pass

    def test_009_go_to_system_configuration___structure_in_cmssearch_for_bettracking_configturn_off_bettracking_uncheck_the_checkboxsave_changes(self):
        """
        DESCRIPTION: Go to System configuration -> Structure in CMS
        DESCRIPTION: Search for BetTracking config
        DESCRIPTION: Turn OFF BetTracking (uncheck the checkbox)
        DESCRIPTION: Save changes
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_010_go_to_app___open_my_betsopen_bets_tabobserve_my_bets_footer(self):
        """
        DESCRIPTION: Go to app -> open My Bets/Open Bets tab
        DESCRIPTION: Observe My Bets Footer
        EXPECTED: The short description text in the footer is not displayed
        """
        pass
