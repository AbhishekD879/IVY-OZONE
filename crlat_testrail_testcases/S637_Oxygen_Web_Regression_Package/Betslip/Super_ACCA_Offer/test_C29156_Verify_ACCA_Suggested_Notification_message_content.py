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
class Test_C29156_Verify_ACCA_Suggested_Notification_message_content(Common):
    """
    TR_ID: C29156
    NAME: Verify ACCA Suggested Notification message content
    DESCRIPTION: This test case verifies Acca Suggested Notification message content and it's correspondance to CMS and response about ACCA offer
    DESCRIPTION: AUTOTEST: [C527751] [C528118]
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-10234 Acca Suggested Notification on Betslip
    DESCRIPTION: *   BMA-10235 Acca Eligibility Notification on Betslip
    PRECONDITIONS: For configuration of ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: Notes:
    PRECONDITIONS: [Number of Selections] away from a FREE BET! [Bonus Amount] if [Lose Legs] lets you down - should be CMS - configurable (static block with variables)
    PRECONDITIONS: [Number of Selections] , [Bonus Amount] and [Lose Legs]  from response of the following call e.g. (how to get this call - see INV-2968):
    PRECONDITIONS: https://bp-stg-coral.symphony-solutions.eu/Proxy/freebetOffers?freebetOfferId=<freebetoffer ID e.g.675>.
    PRECONDITIONS: For corresponding "betTypeRef":"id": "ACC5":
    PRECONDITIONS: [Number of Selections] = "freebetTriggerRank" - current number of selections in the betslip
    PRECONDITIONS: [Bonus Amount] =   "freebetTriggerMaxBonus"
    PRECONDITIONS: [Lose Legs] = "freebetTriggerMaxLoseLegs"
    PRECONDITIONS: To check potential stake go to buildBet -> bets -> betTypeRef":"id": "ACC5" -> payout -> potential
    PRECONDITIONS: Example of response:
    PRECONDITIONS: { "freebetTriggerId": "3107", "freebetTriggerType": "STLLOSE", "**freebetTriggerRank**": "5", "freebetTriggerQualification": "N", "freebetTriggerAmount": { "currency": "USD" }, "**freebetTriggerBetType**": "ACC5", "freebetTriggerMinPriceNum": "", "freebetTriggerMinPriceDen": "", "freebetTriggerMinLegPriceNum": "", "freebetTriggerMinLegPriceDen": "", "freebetTriggerMinLoseLegs": "", "**freebetTriggerMaxLoseLegs**": "1", "freebetTriggerBonus": "", "**freebetTriggerMaxBonus**": "25.00", "freebetTriggerCalcMethod": "S" }
    """
    keep_browser_open = True

    def test_001_log_in_to_cms(self):
        """
        DESCRIPTION: Log In to CMS
        EXPECTED: 
        """
        pass

    def test_002_go_to_admin_section_in_cms(self):
        """
        DESCRIPTION: Go to 'Admin' section in CMS
        EXPECTED: 'Admin' section is opened
        """
        pass

    def test_003_choose_static_blocks_tab(self):
        """
        DESCRIPTION: Choose 'Static Blocks' tab
        EXPECTED: 'Static Blocks' tab is opened
        """
        pass

    def test_004_verify_content_of_acca_suggested_notification(self):
        """
        DESCRIPTION: Verify content of ACCA Suggested Notification
        EXPECTED: The following ACCA Suggested Notification message is displayed:
        EXPECTED: \[['param1']] away from a FREE BET! (up to [['currency']\]\[['param2'\]] ) if ONE selection lets you down *ACCA odds must be at least 3/1. Min stake [['currency']]2
        EXPECTED: where
        EXPECTED: *  [['param1']] - Number of Selections
        EXPECTED: *  [['param2']] - Bonus Amount
        EXPECTED: *  [['currency']] - Currency that uses logged in user
        """
        pass

    def test_005_open_acca_suggested_notification_section_and_make_some_changes_in_content(self):
        """
        DESCRIPTION: Open ACCA Suggested Notification section and make some changes in content
        EXPECTED: It is possible to make changes in ACCA Suggested Notification section
        """
        pass

    def test_006_click_on_save_button(self):
        """
        DESCRIPTION: Click on 'Save' button
        EXPECTED: The changes are saved
        """
        pass

    def test_007_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_008_login_with_user_who_use_gbp_or_eur_currency(self):
        """
        DESCRIPTION: Login with user who use GBP or EUR currency
        EXPECTED: User is logged in
        """
        pass

    def test_009_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: ACCA Offer is received from Open Bet for the user
        """
        pass

    def test_010_verify_that_acca_suggested_notification_content_correspondsto_cms_and_response_about_acca_offer(self):
        """
        DESCRIPTION: Verify that ACCA Suggested Notification content corresponds to CMS and response about ACCA offer
        EXPECTED: ACCA Suggested Notification content corresponds to CMS and response about ACCA offer
        """
        pass

    def test_011_go_back_to_cms_and_open_static_blocks_tab_again(self):
        """
        DESCRIPTION: Go back to CMS and open 'Static Blocks' tab again
        EXPECTED: 
        """
        pass

    def test_012_verify_content_of_acca_suggested_notification_2(self):
        """
        DESCRIPTION: Verify content of ACCA Suggested Notification 2
        EXPECTED: The following ACCA Suggested Notification message is displayed:
        EXPECTED: NEARLY THERE...*ACCA odds must be 3/1. Please pick a different selection in order to qualify
        """
        pass

    def test_013_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_014_add_two_more_selections_to_betslip_that_are_applicable_for_acca_insurance_and_their_combined_odds_are_below_31(self):
        """
        DESCRIPTION: Add two more selections to Betslip that are applicable for ACCA Insurance and their combined odds are below 3/1
        EXPECTED: ACCA Suggested Notification 2 appears
        """
        pass

    def test_015_verify_that_acca_suggested_notification_2_content_correspondsto_cms_and_response_about_acca_offer(self):
        """
        DESCRIPTION: Verify that ACCA Suggested Notification 2 content corresponds to CMS and response about ACCA offer
        EXPECTED: ACCA Suggested Notification content corresponds to CMS and response about ACCA offer
        """
        pass

    def test_016_go_back_to_cms_and_open_static_blocks_tab_again(self):
        """
        DESCRIPTION: Go back to CMS and open 'Static Blocks' tab again
        EXPECTED: 
        """
        pass

    def test_017_verify_content_of_acca_eligibility_notification(self):
        """
        DESCRIPTION: Verify content of ACCA Eligibility Notification
        EXPECTED: The following ACCA Suggested Notification message is displayed:
        EXPECTED: GET IN! Place this acca to earn a FREE BET (up to \[['currency']\]\[['param2'\]]) if ONE lets you down. Min stake [['currency']]2
        EXPECTED: where
        EXPECTED: *  [['param2']] - Bonus Amount [['currency']] - Currency that uses logged in user
        """
        pass

    def test_018_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_019_add_two_more_selections_to_betslip_that_are_applicable_for_acca_insurance_and_their_combined_odds_are_above_31(self):
        """
        DESCRIPTION: Add two more selections to Betslip that are applicable for ACCA Insurance and their combined odds are above 3/1
        EXPECTED: ACCA Eligible Notification appears
        """
        pass

    def test_020_verify_that_acca_eligible_notification_content_correspondsto_cms_and_response_about_acca_offer(self):
        """
        DESCRIPTION: Verify that ACCA Eligible Notification content corresponds to CMS and response about ACCA offer
        EXPECTED: ACCA Eligible Notification content corresponds to CMS and response about ACCA offer
        """
        pass
