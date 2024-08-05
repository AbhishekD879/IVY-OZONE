import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # Can not update CMS configuration in PROD/BETA
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60004609_Verify_display_of_New_Label_Market_Description(Common):
    """
    TR_ID: C60004609
    NAME: Verify display of New Label- Market Description
    DESCRIPTION: Verify that New Label is displayed below the Market header along with the description when enabled in CMS
    PRECONDITIONS: 1. Horse racing & Greyhound racing events & markets should be available.
    PRECONDITIONS: 2.Market Descriptions should be configured and enabled in CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        if self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled', field_value=True)

    def test_002_navigate_to_system_configuration__structure_and_enable_new_label(self):
        """
        DESCRIPTION: Navigate to System Configuration > Structure and enable New Label
        EXPECTED: User should be able to save the changes in CMS
        """
        self.cms_config.create_and_update_markets_with_description(name='Win or Each Way', description='An each way '
                                                                                                       'bet is a bet '
                                                                                                       'made up of '
                                                                                                       'two parts: a '
                                                                                                       'WIN bet and a '
                                                                                                       'PLACE bet',
                                                                   HR=True, GH=True, New_badge=True)
        self.__class__.event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.event2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)

    def test_003_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("Homepage")

    def test_004_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn(vec.sb.HORSERACING.upper(), sports.keys(),
                          msg=f'"{vec.sb.HORSERACING.upper()}" is not found in the header sport menu')
            sports.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_005_click_on_any_race_which_has_the_market_template_available_for_which_description_is_added_and_new_label_is_configured_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market template available for which description is added and New label is configured in CMS
        EXPECTED: User should be navigated to EDP page
        """
        self.navigate_to_edp(event_id=self.event.event_id, sport_name='horse-racing')
        self.site.wait_content_state_changed()

    def test_006_validate_the_description_and_new_label_displayedindexphpattachmentsget120830386indexphpattachmentsget120830387(self, expected_badge=True):
        """
        DESCRIPTION: Validate the description and New Label displayed![](index.php?/attachments/get/120830386)
        DESCRIPTION: ![](index.php?/attachments/get/120830387)
        EXPECTED: 1: User should be able to view the description below the Market Header
        EXPECTED: 2: New Label should be displayed and CSS should be as mentioned in Zeplin
        """
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        market_description = self.site.racing_event_details.has_market_description_text()
        self.assertTrue(market_description, msg='Market description is not displayed')
        new_badge = self.site.racing_event_details.has_market_desc_new_badge()
        if expected_badge:
            self.assertTrue(new_badge, msg='"NEW" badge is not displayed')
        else:
            self.assertFalse(new_badge, msg='"NEW" badge is displayed')

    def test_007_navigate_to_grey_hound_racing_and_repeat_5__6_steps(self, expected_badge=True):
        """
        DESCRIPTION: Navigate to Grey Hound racing and repeat 5 & 6 steps
        EXPECTED:
        """
        self.navigate_to_page("greyhound-racing")
        self.site.wait_splash_to_hide(timeout=10)
        self.navigate_to_edp(event_id=self.event2.event_id, sport_name='greyhound-racing')
        self.site.wait_content_state_changed()
        self.market_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        market_description = self.site.greyhound_event_details.has_market_description_text()
        self.assertTrue(market_description, msg='Market description is not displayed')
        new_badge = self.site.greyhound_event_details.has_market_desc_new_badge()
        if expected_badge:
            self.assertTrue(new_badge, msg='"NEW" badge is not displayed')
        else:
            self.assertFalse(new_badge, msg='"NEW" badge is displayed')

    def test_008_now_disable_the_new_label_configuration_in_cms_and_repeat_4567_stepsvalidate_that_new_label_is_not_displayed(self):
        """
        DESCRIPTION: Now disable the New label configuration in CMS and Repeat 4,5,6,7 Steps
        DESCRIPTION: Validate that New Label is not displayed
        EXPECTED: New Label should not be displayed when disabled in CMS
        """
        self.cms_config.create_and_update_markets_with_description(name='Win or Each Way', description='An each way '
                                                                                                       'bet is a bet '
                                                                                                       'made up of '
                                                                                                       'two parts: a '
                                                                                                       'WIN bet and a '
                                                                                                       'PLACE bet',
                                                                   HR=True, GH=True, New_badge=False)
        self.test_004_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing()
        self.test_005_click_on_any_race_which_has_the_market_template_available_for_which_description_is_added_and_new_label_is_configured_in_cms()
        self.test_006_validate_the_description_and_new_label_displayedindexphpattachmentsget120830386indexphpattachmentsget120830387(expected_badge=False)
        self.test_007_navigate_to_grey_hound_racing_and_repeat_5__6_steps(expected_badge=False)
