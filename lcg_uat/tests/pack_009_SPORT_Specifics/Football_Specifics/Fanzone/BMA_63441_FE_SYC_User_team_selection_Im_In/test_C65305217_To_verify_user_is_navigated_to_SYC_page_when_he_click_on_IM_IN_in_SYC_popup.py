import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305217_To_verify_user_is_navigated_to_SYC_page_when_he_click_on_IM_IN_in_SYC_popup(Common):
    """
    TR_ID: C65305217
    NAME: To verify user is navigated to SYC page when he click on IM IN in SYC popup
    DESCRIPTION: This test case is to verify user is navigated to SYC page when he click on IM IN in SYC popup
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        fanzone_teams = self.cms_config.get_fanzones()
        for fanzone_team in fanzone_teams:
            self.cms_config.update_fanzone(fanzone_team['name'])

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: User should be navigate to Football slp
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)

    def test_003_verify_syc_popup_is_displayed(self):
        """
        DESCRIPTION: Verify SYC popup is displayed
        EXPECTED: SYC popup should be displayed
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)

    def test_004_verify_ui_of_syc_popup(self):
        """
        DESCRIPTION: Verify UI of SYC popup
        EXPECTED: SYC popup should be as per the designs provided by UI/UX
        EXPECTED: Link: https://app.Zeplin.io/project/609b99f3e39d17baed699db1/screen/60abd02280a570be0bb052f7
        """
        # Cannot validate zeplin design

    def test_005_click_on_im_in_cta_button(self):
        """
        DESCRIPTION: Click on IM IN CTA button
        EXPECTED: User is navigated to Show Your Colors page
        """
        # Covered in above step
