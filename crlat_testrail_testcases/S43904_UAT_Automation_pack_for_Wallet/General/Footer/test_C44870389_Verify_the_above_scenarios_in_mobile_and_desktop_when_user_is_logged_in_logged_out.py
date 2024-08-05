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
class Test_C44870389_Verify_the_above_scenarios_in_mobile_and_desktop_when_user_is_logged_in_logged_out(Common):
    """
    TR_ID: C44870389
    NAME: Verify the above scenarios in mobile and desktop, when user is logged in /logged out
    DESCRIPTION: 
    PRECONDITIONS: Scenarios:
    PRECONDITIONS: 1. When the user is logged in and
    PRECONDITIONS: 2. When the user is logged out.
    """
    keep_browser_open = True

    def test_001_load_application_and_navigate_to_footer(self):
        """
        DESCRIPTION: Load application and navigate to footer.
        EXPECTED: Application is loaded and navigated to footer.
        """
        pass

    def test_002_verify_that_text_about_us_coralcontact_ushelpsports_statsaffiliatesjobsonline_rulesshop_rulesprivacy_policycookie_policyfairnessfinancial_controlsresponsible_gamblingterms__conditionsquick_links_are_displayed_followed_by_anchors_that_link_to_the_correct_pages_fully_functional_and_aligned_as_per_cms(self):
        """
        DESCRIPTION: Verify that text About us (Coral),
        DESCRIPTION: Contact Us
        DESCRIPTION: Help
        DESCRIPTION: Sports stats
        DESCRIPTION: Affiliates
        DESCRIPTION: Jobs
        DESCRIPTION: Online Rules
        DESCRIPTION: Shop Rules
        DESCRIPTION: Privacy policy
        DESCRIPTION: Cookie Policy
        DESCRIPTION: Fairness
        DESCRIPTION: Financial controls
        DESCRIPTION: Responsible gambling
        DESCRIPTION: Terms & Conditions
        DESCRIPTION: Quick Links are displayed followed by anchors that link to the correct pages, fully functional and aligned as per CMS.
        EXPECTED: User is able to see text
        EXPECTED: About Us (Coral)
        EXPECTED: Quick Link are displayed and link to the correct pages, fully functional and aligned.
        EXPECTED: "Financial controls" quick link is seen only when the user is logged in.
        """
        pass
