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
class Test_C44870377_Verify_the_Footer_Menu_links_and_contents(Common):
    """
    TR_ID: C44870377
    NAME: "Verify the Footer Menu links and contents.
    DESCRIPTION: This TC is to verify footer content and all links.
    PRECONDITIONS: 
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
        pass

    def test_002__verify_the_footer_text_area_providing_license_no_ref_54743_and_ref_010_012_copyright_and_compliance_information(self):
        """
        DESCRIPTION: -Verify the Footer text area providing License No (ref: 54743) and (ref 010, 012), copyright and compliance information
        EXPECTED: User is able to see License No ref: 54743) and (ref 010, 012), copyright and compliance information.
        """
        pass

    def test_003__check_the_footer_logo_links_these_links_are_all_logo_based_as_per_design_for_payment_providers_responsible_gaming_gamcare_fun_stop_gamstop_etc(self):
        """
        DESCRIPTION: -Check the footer logo links, these links are all logo based as per design for payment providers, responsible gaming, Gamcare, Fun stop /Gamstop etc
        EXPECTED: User is able to see logos for payment providers, Responsible Gambling, Gamcare, Fun Stop/Gamstop etc.
        """
        pass
