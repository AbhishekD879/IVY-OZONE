import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_tst2
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone_reg_tests
@pytest.mark.desktop
@vtest
class Test_C65305507_Verify_GA_tracking_for_users_actions_onPre_login_team_confirmation_pop_up_2_CTAs(BaseDataLayerTest):
    """
    TR_ID: C65305507
    NAME: Verify GA tracking for user's actions onÂ Pre-login team confirmation pop-up (2 CTA's)
    DESCRIPTION: This test case is to verify GA tracking for user's actions on Free text input pop-up (2 CTA's)
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) User is in logged out state
    PRECONDITIONS: 4) User should be on team selection page through promotion and open console
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.aston_villa.title()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) User is in logged out state
        PRECONDITIONS: 4) User should be on team selection page through promotion and open console
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE + '!'] if not tests.settings.backend_env == 'prod' \
            else promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

    def test_001_open_team_selection_page_through_promotion(self):
        """
        DESCRIPTION: Open team selection page through promotion
        EXPECTED: Team selection page should be opened
        """
        self.__class__.promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = self.promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')

    def test_002_select_any_team_ex_arsenal(self):
        """
        DESCRIPTION: Select any team (ex: Arsenal)
        EXPECTED: Selected team should be highlighted and its login popup
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(self.teamname)
        team.click()
        self.__class__.dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
                                                                  verify_name=False)
        self.assertTrue(self.dialog_confirm,
                        msg='login popup not appeared')

    def test_003_click_on_exit_button_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on Exit button and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "confirmation screen",
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": "EXIT",
        EXPECTED: "eventDetails": "Arsenal"
        EXPECTED: })
        """
        self.dialog_confirm.select_different_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='EXIT')
        expected_response = {"event": "trackEvent",
                             "eventAction": "confirmation screen",
                             "eventCategory": "show your colors",
                             "eventLabel": "EXIT",
                             "eventDetails": self.teamname}
        self.compare_json_response(actual_response, expected_response)

    def test_004_repeat_steps_and_click_on_login_cta_buttoncheck_ga_tracking(self):
        """
        DESCRIPTION: Repeat steps and click on LOGIN CTA button
        DESCRIPTION: check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "confirmation screen",
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": "LOG IN TO CONFIRM",
        EXPECTED: "eventDetails": "Arsenal"
        EXPECTED: })
        """
        if not tests.settings.backend_env == 'prod':
            self.device.refresh_page()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        team = self.site.show_your_colors.items_as_ordered_dict.get(self.teamname)
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='LOG IN TO CONFIRM')
        expected_response = {"event": "trackEvent",
                             "eventAction": "confirmation screen",
                             "eventCategory": "show your colors",
                             "eventLabel": "LOG IN TO CONFIRM",
                             "eventDetails": self.teamname}
        self.compare_json_response(actual_response, expected_response)
