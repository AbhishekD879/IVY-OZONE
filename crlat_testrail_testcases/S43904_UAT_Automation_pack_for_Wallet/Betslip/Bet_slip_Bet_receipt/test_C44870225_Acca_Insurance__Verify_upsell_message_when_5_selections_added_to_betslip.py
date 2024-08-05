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
class Test_C44870225_Acca_Insurance__Verify_upsell_message_when_5_selections_added_to_betslip(Common):
    """
    TR_ID: C44870225
    NAME: Acca Insurance - Verify upsell message when 5 selections added to betslip
    DESCRIPTION: 
    PRECONDITIONS: App or site is loaded and the user is logged in
    """
    keep_browser_open = True

    def test_001_user_launches_the_siteapp_and_logs_in(self):
        """
        DESCRIPTION: User launches the site/app and logs in
        EXPECTED: User is able to place a bet as logged in customer
        """
        pass

    def test_002_user_adds_4_selections_in_the_betslip_and_does_not_see_an_acca_insurance_qualification(self):
        """
        DESCRIPTION: User adds 4 selections in the betslip and does not see an Acca Insurance Qualification
        EXPECTED: User has added 4 selections in the betslip and does not see an Acca Insurance Qualification
        """
        pass

    def test_003_user_adds_a_fifth_selection_to_the_betslip(self):
        """
        DESCRIPTION: User adds a fifth selection to the betslip
        EXPECTED: A new selection has been selected and added to betslip
        """
        pass

    def test_004_user_navigates_to_the_betslip_and_verifies_that_the_following_message_appearyour_selections_qualify_for_acca_insurance(self):
        """
        DESCRIPTION: User navigates to the betslip and verifies that the following message appear:
        DESCRIPTION: "Your selections qualify for Acca Insurance"
        EXPECTED: hen betslip is displayed to the user, the following message must be displayed:
        EXPECTED: "Your selections qualify for Acca Insurance"
        """
        pass
