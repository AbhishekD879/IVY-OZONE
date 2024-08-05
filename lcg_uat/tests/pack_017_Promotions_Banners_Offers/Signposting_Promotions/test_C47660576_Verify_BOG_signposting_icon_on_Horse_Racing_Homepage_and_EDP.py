import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@vtest
class Test_C47660576_Verify_BOG_signposting_icon_on_Horse_Racing_Homepage_and_EDP(BaseRacing):
    """
    TR_ID: C47660576
    NAME: Verify "BOG" signposting icon on Horse Racing Homepage and EDP
    DESCRIPTION: This test case verifies "BOG" signposting icon on Horse Racing  event level
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: [BMA-49331] [1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-49331
    PRECONDITIONS: - BOG icon has been enabled in CMS
    PRECONDITIONS: - Events with market configured to show BOG flag available (Market should have 'GP Available' and 'LP Available' checkmarks)
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '1/3', 2: '2/3', 3: '2/7', 4: '1/9'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Created event
        """
        bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']

        if not bog_toggle:
            self.cms_config.update_system_configuration_structure(config_item='BogToggle', field_name='bogToggle',
                                                                  field_value=True)
            bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']
        self.assertTrue(bog_toggle, msg='"Bog toggle" is not enabled in CMS')

        event = self.ob_config.add_UK_racing_event(cashout=True, gp=True, lp_prices=self.prices)
        no_bog_event = self.ob_config.add_UK_racing_event(cashout=True, lp_prices=self.prices)
        self.__class__.event_id = event.event_id
        self.__class__.no_bog_event_id = no_bog_event.event_id

    def test_001_navigate_to_horse_racing_homepage(self):
        """
        DESCRIPTION: Navigate to Horse Racing homepage
        EXPECTED: * BOG icon is displayed on the right side of Race Grid
        EXPECTED: Ladbrokes designs:
        EXPECTED: https://app.zeplin.io/project/5dca842a25a59d8e77bdad7f/dashboard
        EXPECTED: Coral designs:
        EXPECTED: https://app.zeplin.io/project/5de6962b0c68b753005a2b58/dashboard
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')
        section = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(self.uk_and_ire_type_name)
        self.assertTrue(section, msg='Can not find section: "%s"' % self.uk_and_ire_type_name)
        autotest_racing_meeting = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
        autotest_racing_meeting = autotest_racing_meeting.upper() if self.brand == 'bma' else autotest_racing_meeting
        meeting = section.items_as_ordered_dict.get(autotest_racing_meeting)
        self.assertTrue(meeting.bog_icon.is_displayed(), msg='BOG icon is not displayed')

    def test_002_navigate_to_event_with_bog_icon(self):
        """
        DESCRIPTION: Navigate to Event with BOG icon
        EXPECTED: * BOG icon is displayed on top Horse Racing EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.assertTrue(market.section_header.is_bpg_icon_present(), msg='BPG icon is not shown')

    def test_003_return_to_horse_racing_homepage(self):
        """
        DESCRIPTION: Return to Horse Racing homepage
        EXPECTED: * BOG icon is remains displayed on the right side of Race Grid
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')
        section = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(
            self.uk_and_ire_type_name)
        self.assertTrue(section, msg='Can not find section: "%s"' % self.uk_and_ire_type_name)
        autotest_racing_meeting = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
        autotest_racing_meeting = autotest_racing_meeting.upper() if self.brand == 'bma' else autotest_racing_meeting
        meeting = section.items_as_ordered_dict.get(autotest_racing_meeting)
        self.assertTrue(meeting.bog_icon.is_displayed(), msg='BOG icon is not displayed')

    def test_004_navigate_to_event_without_bog_icon(self):
        """
        DESCRIPTION: Navigate to Event without BOG icon
        EXPECTED: * BOG icon is NOT displayed on top of event header
        """
        self.navigate_to_edp(event_id=self.no_bog_event_id, sport_name='horse-racing')
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.assertFalse(market.section_header.is_bpg_icon_present(), msg='BPG icon is shown')
