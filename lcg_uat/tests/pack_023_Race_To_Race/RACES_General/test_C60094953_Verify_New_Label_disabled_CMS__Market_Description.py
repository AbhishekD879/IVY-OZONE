import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # Cannot edit the market description in prod cms
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.greyhounds
@pytest.mark.races
@pytest.mark.races_negative_p2  # Marker for testcases having blank market description
@vtest
class Test_C60094953_Verify_New_Label_disabled_CMS__Market_Description(Common):
    """
    TR_ID: C60094953
    NAME: Verify New Label disabled CMS - Market Description
    DESCRIPTION: This test case verifies toggle option for "New" label if market  descripton table is blank
    PRECONDITIONS: 1. Horse racing & Grey Hound racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Market Description should be enabled in CMS
    PRECONDITIONS: 4: Market description table should have description blank
    PRECONDITIONS: 5: New Label should be enabled in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Enable Racing EDP Markets Description and new label and market description is empty
        EXPECTED: Enable market description, new label and market description is empty
        """
        if not self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled', field_value=True)
        self.cms_config.create_and_update_markets_with_description(name='Win or Each Way',
                                                                   description='',
                                                                   New_badge=True)
        self.__class__.event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.event2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("Homepage")

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
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

    def test_003_click_on_any_race_which_has_the_market_template_available_for_which_description_is_added_and_new_label_is_configured_in_cms(
            self):
        """
        DESCRIPTION: Click on any race which has the Market template available for which description is added and New label is configured in CMS
        EXPECTED: User should be navigated to EDP page
        """
        event_id = self.event.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)

    def test_004_validate_the_description_and_new_label_displayed(self):
        """
        DESCRIPTION: Validate the description and New Label displayed
        EXPECTED: New Label should not be displayed as the description is blank
        """
        market_description = self.site.racing_event_details.has_market_description_text(expected_result=False)
        self.assertFalse(market_description, msg='Description is not empty')
        self.assertFalse(self.site.racing_event_details.has_market_desc_new_badge(expected_result=False),
                         msg=f'"New label" is displayed')

    def test_005_navigate_to_grey_hound_racing_and_repeat_5__6_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hound racing and repeat 5 & 6 steps
        """
        self.navigate_to_page('homepage')
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing')
        event_id = self.event2.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        market_description = self.site.greyhound_event_details.has_market_description_text(expected_result=False)
        self.assertFalse(market_description, msg='Description is not empty')
        self.assertFalse(self.site.greyhound_event_details.has_market_desc_new_badge(expected_result=False),
                         msg=f'"New label" is displayed')
