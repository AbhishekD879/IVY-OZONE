import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870385_Verify_that_text_About_us_Contact_us_Help_etc_under_Help_Information_is_displayed_followed_by_anchors_that_link_to_the_correct_pages_fully_functional_and_aligned_as_follows(Common):
    """
    TR_ID: C44870385
    NAME: Verify that text About us, Contact us, Help etc under 'Help & Information'  is displayed followed by anchors that link to the correct pages, fully functional and aligned as follows:
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application
        EXPECTED: Application is opened.
        """
        pass

    def test_002_navigate_to_footer__under_help__informationverify_that_text_about_us_contact_us_help_sports_stats_affiliates_jobs_online_rules_shop_rules_privacy_policy_cookie_policy_fairness_financial_controls_responsible_gambling_terms__conditions_are_displayed_and_when_clicked_are_fully_functional_and_aligned_as_per_cms(self):
        """
        DESCRIPTION: Navigate to footer > under 'Help & Information'
        DESCRIPTION: Verify that text About us, Contact us, Help, Sports stats, Affiliates, Jobs, Online rules, Shop rules, Privacy policy, Cookie policy, Fairness, Financial controls, Responsible gambling, Terms & Conditions are displayed and when clicked are fully functional and aligned as per CMS.
        EXPECTED: Text About us, Contact us, Help, Sports stats, Affiliates, Jobs, Online rules, Shop rules, Privacy policy, Cookie policy, Fairness, Financial controls, Responsible gambling, Terms & Conditions are displayed as per CMS and when clicked the user is navigated to appropriate pages.
        """
        pass
