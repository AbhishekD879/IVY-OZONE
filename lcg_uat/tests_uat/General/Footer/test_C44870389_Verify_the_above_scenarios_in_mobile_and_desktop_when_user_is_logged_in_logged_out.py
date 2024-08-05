import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.p2
@pytest.mark.other
@vtest
class Test_C44870389_Verify_the_above_scenarios_in_mobile_and_desktop_when_user_is_logged_in_logged_out(Common):
    """
    TR_ID: C44870389
    NAME: Verify the above scenarios in mobile and desktop, when user is logged in /logged out
    """
    keep_browser_open = True

    def test_001_load_application_and_navigate_to_footer(self):
        """
        DESCRIPTION: Load application and navigate to footer.
        EXPECTED: Application is loaded and navigated to footer.
        """
        self.site.login()
        self.site.close_all_dialogs(timeout=5)
        self.site.wait_content_state('homepage')
        self.site.header.scroll_to_bottom()

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
        """
        # we can not automate CMS related functionality as the quick links are configured through GVC CMS
        footer_menu = list(self.site.footer.footer_section_top.items_as_ordered_dict.keys())
        self.assertTrue(footer_menu, msg="Quick Links are not displayed")
        expected_links_list = list(vec.bma.EXPECTED_LINKS_LIST)
        if self.brand == 'ladbrokes':
            expected_links_list.pop(5)
            expected_links_list.pop(5)
            vec.bma.FOOTER_LINK_UNIQUE_WORD.pop(5)
            vec.bma.FOOTER_LINK_UNIQUE_WORD.pop(5)
        for index in range(len(expected_links_list)):
            self.assertEqual(footer_menu[index], expected_links_list[index],
                             msg=f'"{expected_links_list[index]}" is not available in the footer came {footer_menu[index]}')
            footer_links = self.site.footer.footer_section_top.items_as_ordered_dict
            key, value = list(footer_links.items())[index]
            value.click()
            if self.brand == 'ladbrokes':
                if key not in [vec.bma.EXPECTED_LINKS_LIST.contact_us, vec.bma.EXPECTED_LINKS_LIST.terms_and_Conditions, vec.bma.EXPECTED_LINKS_LIST.financial_controls]:
                    self.device.switch_to_new_tab()
            else:
                if key == vec.bma.EXPECTED_LINKS_LIST.help:
                    self.device.switch_to_new_tab()

            wait_for_result(lambda: vec.bma.FOOTER_LINK_UNIQUE_WORD[index] in self.device.get_current_url(),
                            name=f'Navigate to "{vec.bma.FOOTER_LINK_UNIQUE_WORD[index]}"', timeout=30)
            current_url = self.device.get_current_url()
            self.assertIn(vec.bma.FOOTER_LINK_UNIQUE_WORD[index], current_url,
                          msg=f'User is redirected to the wrong page: "{current_url}", '
                              f'expected is: "{vec.bma.FOOTER_LINK_UNIQUE_WORD[index]}"')
            if self.brand == 'ladbrokes':
                if key not in [vec.bma.EXPECTED_LINKS_LIST.contact_us, vec.bma.EXPECTED_LINKS_LIST.terms_and_Conditions, vec.bma.EXPECTED_LINKS_LIST.financial_controls]:
                    self.device.driver.switch_to.window(self.device.driver.window_handles[0])
                else:
                    self.device.go_back()
            else:
                if key == vec.bma.EXPECTED_LINKS_LIST.help:
                    self.device.driver.switch_to.window(self.device.driver.window_handles[0])
                else:
                    self.device.go_back()
            self.site.wait_content_state("Homepage")
