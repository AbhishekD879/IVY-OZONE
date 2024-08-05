import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304966_To_verify_UI_of_SYC_popup(Common):
    """
    TR_ID: C65304966
    NAME: To verify UI of SYC popup
    DESCRIPTION: To verify UI of SYC popup
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
        PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
        PRECONDITIONS: 5)User has not performed any action on SYC overlay
        PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to Football page
        """
        self.site.login()
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                             timeout=30)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')

    def test_003_verify_syc_ui(self):
        """
        DESCRIPTION: Verify SYC UI
        EXPECTED: Below data should be on SYC overlay :
        EXPECTED: 1) SHOW US YOUR COLOURS
        EXPECTED: 2)Description
        EXPECTED: "Time to show your colours! Tell us
        EXPECTED: which English Premier League
        EXPECTED: team you support and gain access
        EXPECTED: to FANZONE where you will see
        EXPECTED: exclusive markets and offers, stats, and
        EXPECTED: what fans of other teams are saying!"
        EXPECTED: 3)Team color icon in horizontal mode
        EXPECTED: 4)REMING ME LATER(In bold)
        EXPECTED: 5)I'M IN (In bold), Yellow color CTA button
        EXPECTED: 6)DON'T SHOW ME THIS AGAIN in blue color
        """
        self.assertEqual(self.dialog_fb.name, vec.fanzone.SYC_POP_UP_NAME,
                         msg=f'Actual popup name is "{self.dialog_fb.name}" is not same as '
                             f'Expected popup name "{vec.fanzone.SYC_POP_UP_NAME}"')
        self.assertEqual(self.dialog_fb.syc_description, vec.fanzone.SYC_POP_UP_DESCRIPTION,
                         msg=f'Actual popup description is "{self.dialog_fb.syc_description}" is not same as '
                             f'Expected popup description "{vec.fanzone.SYC_POP_UP_DESCRIPTION}"')
        self.assertTrue(self.dialog_fb.team_color_icon,
                        msg='Team Color icon is not displayed')
        self.assertEqual(self.dialog_fb.remind_later_button.name, vec.fanzone.SYC_POP_UP_REMINED_ME_LATER,
                         msg=f'Actual popup remind later button name is "{self.dialog_fb.remind_later_button.name}" is not same as '
                             f'Expected popup remind later button name "{vec.fanzone.SYC_POP_UP_REMINED_ME_LATER}"')
        self.assertEqual(self.dialog_fb.imin_button.name, vec.fanzone.SYC_POP_UP_I_M_IN,
                         msg=f'Actual popup i\'m in button name is "{self.dialog_fb.imin_button.name}" is not same as '
                             f'Expected popup i\'m in button name "{vec.fanzone.SYC_POP_UP_I_M_IN}"')
        self.assertEqual(self.dialog_fb.dont_show_me_button.name, vec.fanzone.SYC_POP_UP_DONT_SHOW_ME_AGAIN,
                         msg=f'Actual popup dont show me button name is "{self.dialog_fb.dont_show_me_button.name}" is not same as '
                             f'Expected popup dont show me button name "{vec.fanzone.SYC_POP_UP_DONT_SHOW_ME_AGAIN}"')



