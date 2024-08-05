import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.sports
@pytest.mark.horseracing
@pytest.mark.greyhounds
@pytest.mark.reg167_fix
@pytest.mark.desktop
@vtest
class Test_C60094950_Verify_the_CSS_styles_for_Market_description(Common):
    """
    TR_ID: C60094950
    NAME: Verify the CSS styles for Market description
    DESCRIPTION: Verify the CSS styles for Market description displayed in EDP for both Horse Racing & Grey Hounds
    PRECONDITIONS: 1. Horse racing & Greyhound racing events & markets should be available.
    PRECONDITIONS: 2.Market Descriptions should be configured and enabled in CMS
    """
    keep_browser_open = True

    def verify_css_result(self, market_description, expected_color, expected_font_family, expected_font_size, expected_font_weight):
        font_color = market_description.css_property_value('color')
        actual_font_color = self.rgba_to_hex(font_color)
        self.assertEqual(actual_font_color, expected_color, msg=f'Actual color "{actual_font_color}" is not same as Expected "{expected_color}"')
        font_family = market_description.css_property_value('font-family')
        self.assertIn(expected_font_family, font_family, msg=f'Actual font family "{font_family}" is not same as Expected "{expected_font_family}"')
        font_size = market_description.css_property_value('font-size')
        self.assertEqual(font_size, expected_font_size, msg=f'Actual font size "{font_size}" is not same as Expected "{expected_font_size}"')
        font_weight = market_description.css_property_value('font-weight')
        self.assertEqual(font_weight, expected_font_weight, msg=f'Actual font weight "{font_weight}" is not same as Expected "{expected_font_weight}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Market Descriptions should be configured and enabled in CMS
        """
        if not self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled',
                                                                  field_value=True)
        if tests.settings.backend_env == 'prod':
            self.__class__.event = self.get_active_events_for_category(category_id=21)[0]
            self.__class__.event2 = self.get_active_events_for_category(category_id=19)[0]
        else:
            self.__class__.event = self.ob_config.add_UK_racing_event(number_of_runners=1)
            self.__class__.event2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        self.cms_config.create_and_update_markets_with_description(name='Win or Each Way', description='An each way bet is a bet made up of two parts: a WIN bet and a PLACE bet', New_badge=True)

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        self.site.open_sport(name='Horse Racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_race_which_has_the_market_templates_available_for_which_description_are_added_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description are added in CMS
        EXPECTED: User should be navigated to EDP page
        """
        event_id = self.event['event']['id'] if tests.settings.backend_env == 'prod' else self.event.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)

    def test_004_validate_css(self):
        """
        DESCRIPTION: Validate CSS
        EXPECTED: CSS styles should be as per Zeplin designs
        """
        result = wait_for_result(lambda: self.site.racing_event_details.market_description_text,
                                 name='Market Description is not available', timeout=30)
        if self.brand == 'bma':
            self.verify_css_result(market_description=result, expected_color='#41494e', expected_font_family='Lato', expected_font_size='12px', expected_font_weight='400')
        else:
            self.verify_css_result(market_description=result, expected_color='#5a5a5a', expected_font_family='Helvetica Neue', expected_font_size='12px', expected_font_weight='400')

    def test_005_navigate_to_grey_hounds_and_repeat_3__4_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Repeat 3 & 4 Steps
        EXPECTED: CSS styles should be as per Zeplin designs
        """
        self.navigate_to_page('homepage')
        self.site.open_sport(name='Greyhounds')
        self.site.wait_content_state('greyhound-racing')
        event_id = self.event2['event']['id'] if tests.settings.backend_env == 'prod' else self.event2.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        result = self.site.greyhound_event_details.market_description_text
        if self.brand == 'bma':
            self.verify_css_result(market_description=result, expected_color='#41494e', expected_font_family='Lato', expected_font_size='12px', expected_font_weight='400')
        else:
            self.verify_css_result(market_description=result, expected_color='#5a5a5a', expected_font_family='Helvetica Neue', expected_font_size='12px', expected_font_weight='400')
