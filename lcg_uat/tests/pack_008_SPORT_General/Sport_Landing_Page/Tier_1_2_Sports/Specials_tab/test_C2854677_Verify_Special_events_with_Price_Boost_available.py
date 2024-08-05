import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   #Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2854677_Verify_Special_events_with_Price_Boost_available(Common):
    """
    TR_ID: C2854677
    NAME: Verify Special events with Price Boost available
    DESCRIPTION: This test case verifies how Special event with 'Price Boost' flag is displayed on 'Specials' tab
    DESCRIPTION: **Will be available from 102.0 Coral and 102.0 Ladbrokes**
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: **Special** events should contain the following settings:
    PRECONDITIONS: - |Not Primary market| should be created
    PRECONDITIONS: - Set the **drilldownTagNames = MKTFLAG_SP** for |Not Primary market| on market level ('Specials' flag to be ticked on market level in TI)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available on SS
    PRECONDITIONS: 2. 'Special' event is created with:
    PRECONDITIONS: - 'Price Boost' flag ticked on Market level in TI
    PRECONDITIONS: - Selection name should contain 'Was price' in brackets e.g. |Antalyaspor, Altinordu and Krylia Sovetov All To Win (Was 12/1)|
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True
    selection_name = '|PB_S1(Was 12/1)|'
    created_sel_name = 'PB_S1'
    created_was_price = 'Was12/1'

    def test_000_preconditions(self):
        event = self.ob_config.add_autotest_premier_league_football_event(default_market_name='|Draw No Bet|',
                                                                          selection_names=self.selection_name,
                                                                          selection_types=['H'])
        self.__class__.created_event = event.ss_response['event']['name']
        start_time = event.ss_response['event']['startTime']
        self.__class__.event_start_time = self.convert_time_to_local(date_time_str=start_time,
                                                                     ob_format_pattern=self.ob_format_pattern,
                                                                     ss_data=True)
        price = event.ss_response['event']['children'][0]['market']['children'][0]['outcome']['children'][0]['price']
        self.__class__.created_odd = price['priceNum'] + '/' + price['priceDen']
        self.__class__.league_name = self.get_accordion_name_for_event_from_ss(event=event.ss_response)
        market_template_id = next(iter(self.ob_config.football_config.autotest_class.
                                       autotest_premier_league.markets.get("draw_no_bet").values()))
        self.ob_config.make_market_special(
            market_id=event.default_market_id,
            market_template_id=market_template_id,
            event_id=event.event_id,
            sort_market='DN',
            flags='PB,SM,SP')

    def test_001_verify_special_event_with_rice_boost_displaying(self):
        """
        DESCRIPTION: Verify 'Special' event with 'Rice Boost' displaying
        EXPECTED: Event contains:
        EXPECTED: * Selection name
        EXPECTED: * Event start date and time
        EXPECTED: * 'Price/odds' button
        EXPECTED: * 'Was price' part
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=vec.football.FOOTBALL_TITLE)

        specials_tab_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials
        specials_tab_name = self.get_sport_tab_name(name=specials_tab_cms_name,
                                                    category_id=self.ob_config.football_config.category_id)

        self.site.football.tabs_menu.click_button(specials_tab_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, specials_tab_name,
                         msg=f'Actual opened tab "{current_tab} '
                             f'is not as expected "{specials_tab_name}"')

        league = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(self.league_name.upper())
        events = league.items_as_ordered_dict
        for event_name, event in events.items():
            if event_name == self.created_sel_name:
                sel_name = event.template.name
                self.assertEqual(sel_name, self.created_sel_name,
                                 msg=f'Actual selection name: "{sel_name}" is not same as Expected selection name: "{self.created_sel_name}"')

                event_date_time = event.template.event_time
                self.assertEqual(event_date_time, self.event_start_time,
                                 msg=f'Actual event date and time: "{event_date_time}" is not same as Expected date and time: "{self.event_start_time}"')

                bet_button = event.template.bet_button
                self.assertTrue(bet_button, msg='price/odds button is not displayed')
                self.assertEqual(bet_button.name, self.created_odd,
                                 msg=f'Actual price: "{bet_button.name}" is not same as Expected price: "{self.created_odd}"')

                was_price = event.template.was_price
                self.assertEqual(was_price, self.created_was_price,
                                 msg=f'Actual was price: "{was_price}" is not same as Expected was price: "{self.created_was_price}"')

                event.click()
                self.site.wait_content_state(state_name='EventDetails', timeout=20)
                if self.device_type == 'desktop':
                    event_on_EDP = self.site.sport_event_details.header_line.page_title.title
                else:
                    event_on_EDP = self.site.sport_event_details.event_name
                self.assertEqual(event_on_EDP.title(), self.created_event.title(),
                                 msg=f'Current EDP page with event: "{event_on_EDP.title()}" is not same as expected EDP page: "{self.created_event.title()}"')

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: * Selection name corresponds to 'name' attribute on 'outcome' level
        EXPECTED: * Selection name doesn't contain 'Was price' part
        """
        #  covered in step 1

    def test_003_verify_start_date_and_time(self):
        """
        DESCRIPTION: Verify start date and time
        EXPECTED: Event start date and time corresponds to event 'startTime' attribute
        """
        # covered in step 1

    def test_004_verify_priceodds_button(self):
        """
        DESCRIPTION: Verify 'Price/odds' button
        EXPECTED: Value on 'Price/odds' button corresponds to 'priceNum'/'priceDen' attributes for fractional and 'priceDec' attribute for decimal
        """
        # covered in step 1

    def test_005_verify_was_price(self):
        """
        DESCRIPTION: Verify 'Was price'
        EXPECTED: * 'Was price' is displayed below 'Price/odds' button in strikethrough text
        EXPECTED: * Corresponds to 'Was price' part from selection name e.g. Was 12/1
        """
        # covered in step 1

    def test_006_tapclick_on_special_event_with_rice_boost(self):
        """
        DESCRIPTION: Tap/click on 'Special' event with 'Rice Boost'
        EXPECTED: Corresponding event details page is opened
        """
        #  covered in step 1
