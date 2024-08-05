import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.p2
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.uat
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870377_Verify_the_Footer_Menu_links_and_contents(Common):
    """
    TR_ID: C44870377
    NAME: "Verify the Footer Menu links and contents.
    DESCRIPTION: This TC is to verify footer content and all links.
    """
    keep_browser_open = True

    def test_001_verify_the_footer_menu_terms_and_conditions_responsible_gaming_cookie_policy_privacy_policy(self):
        """
        DESCRIPTION: "Verify the Footer Menu
        DESCRIPTION: -Terms and Conditions
        DESCRIPTION: -Responsible Gaming
        DESCRIPTION: -Cookie Policy
        DESCRIPTION: -Privacy Policy
        EXPECTED: User should be able to see
        EXPECTED: -Terms and Conditions
        EXPECTED: -Responsible Gaming
        EXPECTED: -Cookie Policy
        EXPECTED: -Privacy Policy
        """
        self.site.wait_content_state('HomePage')
        footer_menu = self.site.footer.footer_section_top.items_as_ordered_dict

        terms_and_conditions = footer_menu.get(vec.SB.TERMS_AND_CONDITIONS_LABEL)
        self.assertTrue(terms_and_conditions.is_displayed(),
                        msg=f'"{vec.SB.TERMS_AND_CONDITIONS_LABEL}" is not available in the footer')

        responsible_gaming = footer_menu.get(vec.SB.GAMBLING)
        self.assertTrue(responsible_gaming.is_displayed(),
                        msg=f'"{vec.SB.GAMBLING}" is not available in the footer')

        cookie_policy = footer_menu.get(vec.GVC.COOKIE_POLICY_FOOTER)
        self.assertTrue(cookie_policy.is_displayed(),
                        msg=f'"{vec.GVC.COOKIE_POLICY_FOOTER}" is not available in the footer')

        privacy_policy = footer_menu.get(vec.GVC.PRIVACY_POLICY_FOOTER)
        self.assertTrue(privacy_policy.is_displayed(),
                        msg=f'"{vec.GVC.PRIVACY_POLICY_FOOTER}" is not available in the footer')

    def test_002__verify_the_footer_text_area_providing_license_no_ref_54743_and_copyright_and_compliance_information(self):
        """
        DESCRIPTION: -Verify the Footer text area providing License No (ref: 54743) copyright and compliance information
        EXPECTED: User is able to see License No ref: 54743, copyright and compliance information.
        """
        actual_ref_54743 = list(self.site.footer.footer_content_section.text_links_dict.keys())[0]
        self.assertEqual(actual_ref_54743, vec.GVC.EXPECTED_REF_LINK_54743,
                         msg=f'Actual ref:"{actual_ref_54743}" is not same as'
                             f'Expected ref:"{vec.GVC.EXPECTED_REF_LINK_54743}"')

        copy_right = self.site.footer.footer_copy_right
        self.assertTrue(copy_right.is_displayed(),
                        msg=f'"copy right" is not available in the footer text')

        if self.brand == 'bma':
            expected_text = vec.GVC.COMPLIANCE_INFORMATION
        else:
            expected_text = vec.GVC.COMPLIANCE_INFORMATION.replace('Coral', 'Ladbrokes')

        actual_text = self.site.footer.footer_content_section.footer_text.text
        self.assertEqual(actual_text, expected_text,
                         msg=f'Actual text: "{actual_text}" is not same as '
                             f'Expected text: "{expected_text}"')

    def test_003__check_the_footer_logo_links_these_links_are_all_logo_based_as_per_design_for_payment_providers_responsible_gaming_gamcare_fun_stop_gamstop_etc(self):
        """
        DESCRIPTION: -Check the footer logo links, these links are all logo based as per design for payment providers, responsible gaming, Gamcare, Fun stop /Gamstop etc
        EXPECTED: User is able to see logos for payment providers, Responsible Gambling, Gamcare, Fun Stop/Gamstop etc.
        """
        # todo: payment methods not avaiable in ladbrokes need to add when added methods
        if self.brand == 'bma':
            payment_providers = self.site.footer.footer_content_section.payment_methods_dict
            for provider_name, provider in list(payment_providers.items()):
                self.assertTrue(provider.is_displayed(),
                                msg=f'"{provider_name}" logo is not displayed in the footer')

        footer_logo_links = self.site.footer.footer_section_bottom.items_as_ordered_dict
        for logo_name, logo in list(footer_logo_links.items()):
            self.assertTrue(logo.is_displayed(),
                            msg=f'"{logo_name}" logo is not displayed in the footer')
