import pytest
from fractions import Fraction
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.specials_carousel
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C2592685_Price_updating_for_LP_selection_in_Specials_carousel(BaseRacing):
    """
    TR_ID: C2592685
    VOL_ID: C9690172
    NAME: Price updating for LP selection in Specials carousel
    DESCRIPTION: This test case verifies live price updates for LP selection in Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked LP selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    PRECONDITIONS: To get SiteServer info about event use the following url: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: YYYYYYY- event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes which defines price type for an event:
    PRECONDITIONS: 'priceTypeCodes' = 'LP'
    PRECONDITIONS: 'priceTypeCodes' = 'SP'
    PRECONDITIONS: 'priceTypeCodes' = 'LP,SP'
    """
    keep_browser_open = True
    lp_prices = {0: '1/2', 1: '2/3'}
    new_price = '3/4'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events in OB TI and link them
        EXPECTED: Events created and linked
        EXPECTED: LP selection is linked to <Race> event is displayed in Specials Carousel on EDP
        """
        cms_config = self.get_initial_data_system_configuration().get('RacingSpecialsCarousel', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('RacingSpecialsCarousel')
        is_racing_specials_carousel_enabled = cms_config.get('enable')
        if not is_racing_specials_carousel_enabled:
            raise CmsClientException('Racing specials carousel is not enabled in CMS')

        if cms_config.get('label') == '':
            self.__class__.cms_racing_specials_label = vec.racing.RACING_SPECIALS_CAROUSEL_LABEL
        else:
            self.__class__.cms_racing_specials_label = cms_config.get('label', None)

        event_params_1 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.lp_prices)
        self._logger.info('*** Created Horse racing event with params {}'.format(event_params_1))
        self.__class__.selection_name, self.__class__.selection_id = list(event_params_1.selection_ids.items())[0]

        event_params_2 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.lp_prices)
        self._logger.info('*** Created Horse racing event with params {}'.format(event_params_2))
        self.__class__.eventID = event_params_2.event_id

        self.ob_config.link_selection_to_event(selection_id=self.selection_id, eventID=self.eventID)

        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        sections = self.site.racing_event_details.tab_content.specials_carousel.items_as_ordered_dict
        self.assertTrue(sections, msg=f'Can not find any race card')

        expected_specials_racecard = [f'{self.cms_racing_specials_label.upper()} - {self.selection_name}']
        self.assertEqual(list(sections.keys()), expected_specials_racecard,
                         msg=f'Actual section name: "{list(sections.keys())}" '
                         f'is not as expected: "{expected_specials_racecard}"')

    def test_001_in_ti_tool_increase_the_price_for_linked_lp_selection_in_application_verify_live_price_update(self):
        """
        DESCRIPTION: - In TI tool increase the price for linked LP selection
        DESCRIPTION: - In application verify live price update
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to red for a few seconds
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price)

        sections = self.site.racing_event_details.tab_content.specials_carousel.items_as_ordered_dict
        self.assertTrue(sections, msg=f'Can not find any race card')

        special_section = list(sections.values())[0]
        self.assertTrue(special_section.bet_button.is_price_changed(expected_price=self.new_price, timeout=30),
                        msg=f'Actual price: {special_section.bet_button.name} is not as expected: {self.new_price}')

    def test_002_in_ti_tool_decrease_the_price_for_linked_lp_selection_in_application_verify_live_price_update(self):
        """
        DESCRIPTION: - In TI tool decrease the price for linked LP selection
        DESCRIPTION: - In application verify live price update
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to blue for a few seconds
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.lp_prices[1])

        sections = self.site.racing_event_details.tab_content.specials_carousel.items_as_ordered_dict
        self.assertTrue(sections, msg=f'Can not find any race card')

        special_section = list(sections.values())[0]
        self.assertEqual(float(Fraction(special_section.bet_button.name)), float(Fraction(self.lp_prices[1])),
                         msg=f'Actual price: {float(Fraction(special_section.bet_button.name))} is not as expected: {float(Fraction(self.lp_prices[1]))}')
