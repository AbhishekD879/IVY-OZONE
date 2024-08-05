import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.mobile_only
@pytest.mark.insprint_auto
@pytest.mark.additional_navigation
@vtest
# this test case is covering C66137592, C66137593, C66137594, C66137595, C66137596
class Test_C66137591_Verify_the_location_of_In_Play_score_copy_disclaimer_under_open(BaseBetSlipTest):
    """
    TR_ID: C66137591
    NAME: Verify the location of In-Play score copy disclaimer under open
    DESCRIPTION: This test case is to Verify the location of In-Play score copy disclaimer under open
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have bets for sports/races/lottos/pools under all tabs (open/cashout/settled)
        """
        system_config = self.cms_config.get_system_configuration_structure()

        cashout = system_config.get('CashOut')
        if not cashout.get('terms'):
            self.cms_config.update_system_configuration_structure(config_item='CashOut',
                                                                  field_name='terms',
                                                                  field_value=True)
        if not cashout.get('isCashOutTabEnabled'):
            self.cms_config.update_system_configuration_structure(config_item='CashOut',
                                                                  field_name='isCashOutTabEnabled',
                                                                  field_value=True)

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch Application
        EXPECTED: Application shold be launched succesfully
        """
        pass

    def test_002_login_to_applicaiton_with_valid_credentials(self):
        """
        DESCRIPTION: Login to applicaiton with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        self.place_single_bet_on_cashout_selection()

    def test_003_navigate_to_mybets(self, tab_name='Open'):
        """
        DESCRIPTION: Navigate to Mybets
        EXPECTED: Should be able to see recently placed bets under open  Note: Open bets willl be selected by default
        """
        if tab_name == 'Open':
            self.site.open_my_bets_open_bets()
        elif tab_name == 'Cashout':
            self.site.open_my_bets_cashout()
        elif tab_name == 'Settled':
            self.site.open_my_bets_settled_bets()

    def test_004_verify_in_play_score_copy_disclaimer_under_open_by_scrolling_the_bets(self, tab_name='Open'):
        """
        DESCRIPTION: Verify In-Play score copy disclaimer under open by scrolling the bets
        EXPECTED: In-Play score copy disclaimer should be displayed at the bottom of open bets page
        """
        tab_content = None
        if tab_name == 'Open':
            tab_content = self.site.open_bets.tab_content
        elif tab_name == 'Cashout':
            tab_content = self.site.cashout.tab_content
        elif tab_name == 'Settled':
            tab_content = self.site.bet_history.tab_content

        self.assertTrue(tab_content.has_terms_and_conditions(), f'Terms and Conditions Panel is not found under the "{tab_name}" tab')
        self.__class__.terms_and_conditions = tab_content.terms_and_conditions
        self.terms_and_conditions.scroll_to_we()
        self.assertTrue(self.terms_and_conditions.has_in_play_disclaimer, f'In-Play Disclaimer is not found under the "{tab_name}" tab')
        expected_in_play_disclaimer_text = 'In-Play score information is for guidance only and can be subject to a delay.'
        in_play_disclaimer_text = self.terms_and_conditions.in_play_disclaimer.text.strip().upper()
        self.assertEqual(in_play_disclaimer_text, expected_in_play_disclaimer_text.upper(),
                        f'Actual In-Play Disclaimer Text is not Matched with CMS\n'
                        f'FE : "{in_play_disclaimer_text}"\n'
                        f'CMS: "{expected_in_play_disclaimer_text.upper()}"')

    def test_005_verify_the_location_of__in_play_score_copy_disclaimer_under_open(self):
        """
        DESCRIPTION: verify the location of  In-Play score copy disclaimer under open
        EXPECTED: Location of  In-Play score copy disclaimer should be left justified below the Cash Out T&amp;Cs and Edit My Acca T&amp;Cs quick links
        EXPECTED: ![](index.php?/attachments/get/64e57811-3f69-4733-a24f-c9e1b72ca2d1)
        """
        terms = self.terms_and_conditions.terms
        for term_name, term in terms.items():
            self.assertTrue(term.has_info_icon(), f'Info Icon is not displayed on "{term_name}"')

        cashout_tac_location = terms.get('Cash Out T&Cs').location
        edit_my_acca_tac = terms.get('Edit My Acca T&Cs').location
        self.assertEqual(cashout_tac_location.get('y'), edit_my_acca_tac.get('y'),
                         msg=f'"Cashout T&C" and "Edit My Acca Terms and Conditions" are not in-line')
        self.assertLess(cashout_tac_location.get('x'), edit_my_acca_tac.get('x'),
                        msg=f'"Cashout T&C" is not before the "Edit My Acca Terms and Conditions"')

        in_play_disclaimer_location = self.terms_and_conditions.in_play_disclaimer.location.get('y')
        self.assertLess(cashout_tac_location.get('y'), in_play_disclaimer_location,
                        msg='In-Play Disclaimer is located above the Cashout T&C and Edit My Acca T&C')

    def test_006_repeat_step_3_to_step_5_for_all_lottos_pools_under_open_along_with_sportsraces(self):
        """
        DESCRIPTION: Repeat step 3 to step 5 for all lottos, pools under open along with sports/races
        EXPECTED: Result should be same as above
        """
        # lotto and pools are not verifying those tabs are descoping

    def test_007_repeat_above_steps_for_cashout_tab(self):
        """
        DESCRIPTION: Repeat above steps for cashout tab
        EXPECTED: Result should be same as above
        """
        self.test_003_navigate_to_mybets(tab_name='Cashout')
        self.test_004_verify_in_play_score_copy_disclaimer_under_open_by_scrolling_the_bets(tab_name='Cashout')
        self.test_005_verify_the_location_of__in_play_score_copy_disclaimer_under_open()

    def test_008_repeat_above_steps_for_settled_tab(self):
        """
        DESCRIPTION: Repeat above steps for Settled tab
        EXPECTED: Result should be same as above
        """
        self.test_003_navigate_to_mybets(tab_name='Settled')
        self.test_004_verify_in_play_score_copy_disclaimer_under_open_by_scrolling_the_bets(tab_name='Settled')
        self.test_005_verify_the_location_of__in_play_score_copy_disclaimer_under_open()
