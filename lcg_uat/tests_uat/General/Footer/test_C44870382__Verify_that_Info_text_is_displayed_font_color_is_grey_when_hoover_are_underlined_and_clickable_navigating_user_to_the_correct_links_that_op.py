import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870382__Verify_that_Info_text_is_displayed_font_color_is_grey_when_hoover_are_underlined_and_clickable_navigating_user_to_the_correct_links_that_opens_in_another_window_Gibraltar_Gambling_Commissioner_https_(Common):
    """
    TR_ID: C44870382
    NAME: " Verify that Info text is displayed, font color is grey, when hoover are underlined and clickable, navigating user to the correct links that opens in another window.:  Gibraltar Gambling Commissioner https:/
    DESCRIPTION: " Verify that Info text is displayed, font color is Grey, when hoover are underlined and clickable, navigating user to the correct links that opens in another window.:
    DESCRIPTION: Gibraltar Gambling Commissioner https://www.gibraltar.gov.gi/finance-gaming-and-regulations/remote-gambling
    DESCRIPTION: British Gambling Commission: https://secure.gamblingcommission.gov.uk/PublicRegister/Search/Detail/54743
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is opened
        """
        self.site.wait_content_state('homepage')

    def test_002_navigate_to_the_bottom_of_the_page_and_look_for_british_gambling_commission__gibraltar_gambiling_commission_links(self):
        """
        DESCRIPTION: -Verify the Footer text area providing License No (ref: 54743) copyright and compliance information
        EXPECTED: User is able to see License No ref: 54743, copyright and compliance information.
        """
        self.site.header.scroll_to_bottom()
        actual_ref_54743 = list(self.site.footer.footer_content_section.text_links_dict.keys())[0]
        self.assertEqual(actual_ref_54743, vec.GVC.EXPECTED_REF_LINK_54743,
                         msg=f'Actual ref:"{actual_ref_54743}" is not same as'
                             f'Expected ref:"{vec.GVC.EXPECTED_REF_LINK_54743}"')

    def test_003_verify_that_info_text_is_displayed_font_color_is_grey_when_hoover_are_underlined_and_clickable_navigating_user_to_the_correct_links_that_opens_in_another_windowgibraltar_gambling_commissioner_httpswwwgibraltargovgifinance_gaming_and_regulationsremote_gamblingbritish_gambling_commission_httpssecuregamblingcommissiongovukpublicregistersearchdetail54743coral_is_operated_by_lc_international_limited_suite_6_atlantic_suites_gibraltar_and_licensed_ref_54743_and_regulated_by_the_british_gambling_commission_for_persons_gambling_in_great_britain_for_persons_gambling_outside_great_britain_ladbrokes_is_licensed_ref_010_012_by_the_government_of_gibraltar_and_regulated_by_the_gibraltar_gambling_commissioner(self):
        """
        DESCRIPTION: Verify that Info text is displayed, font color is Grey, when hoover are underlined and clickable, navigating user to the correct links that opens in another window.:
        DESCRIPTION: Coral is operated by LC International Limited who are licensed and regulated in Great Britain by the Gambling Commission under account number 54743.
        EXPECTED: When clicked on (ref 54743), the user is navigated to
        EXPECTED: Gambling Commission: https://secure.gamblingcommission.gov.uk/PublicRegister/Search/Detail/54743
        """
        footer_content = self.site.footer.footer_content_section
        footer_text_links = footer_content.text_links_dict
        if self.brand == 'ladbrokes':
            expected_text = vec.gvc.COMPLIANCE_INFORMATION.replace('Coral', 'Ladbrokes')
            expected_color = vec.colors.LADBROKES_COMPLIANCE_INFO_FONT_COLOR
        else:
            expected_text = vec.gvc.COMPLIANCE_INFORMATION
            expected_color = vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY
        self.assertEqual(footer_content.footer_text.text, expected_text,
                         msg=f'Actual text: "{footer_content.footer_text.text}" is not same as'
                             f'Expected text: "{expected_text}"')
        self.assertEqual(footer_content.text_color_value, expected_color,
                         msg=f'Default text color "{footer_content.text_color_value}" is not equal to expected'
                             f'"{expected_color}"')
        footer_text_links.get(vec.gvc.EXPECTED_REF_LINK_54743).click()
        wait_for_result(lambda: self.device.switch_to_new_tab(), timeout=10)
        actual_url = self.device.get_current_url()
        self.assertIn(vec.gvc.FOOTER_LOGO_URL.gambling_comission, actual_url,
                      msg='Not navigated to "Gambling Commission" page')
        self.device.driver.switch_to.window(self.device.driver.window_handles[0])
