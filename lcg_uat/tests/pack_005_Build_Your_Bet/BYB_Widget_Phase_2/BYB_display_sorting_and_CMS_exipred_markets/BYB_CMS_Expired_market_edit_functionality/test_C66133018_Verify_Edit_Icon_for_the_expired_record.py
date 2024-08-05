import pytest
from tests.base_test import vtest
from tests.Common import Common
from datetime import datetime
from tzlocal import get_localzone
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.byb_widget
@pytest.mark.OZONE_15083
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.insprint_auto
@pytest.mark.desktop
@vtest
# Covered C66133019, C66133020, C66133021
class Test_C66133018_Verify_Edit_Icon_for_the_expired_record(Common):
    """
    TR_ID: C66133018
    NAME: Verify 'Edit Icon' for the expired record
    DESCRIPTION: This test case is to verify 'Edit Icon' of expired records under 'Expired Market Cards'
    PRECONDITIONS: 1. BYB Widget sub section should be created under BYB main section
    PRECONDITIONS: 2. Navigation to go CMS -> BYB -> BYB Widget
    PRECONDITIONS: 3.Expired Market Cards should be present
    """
    keep_browser_open = True
    timezone = str(get_localzone())

    def date_from(self):
        # Time Zone validation
        if self.timezone.upper() == "UTC":
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, minutes=-1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, hours=-1, minutes=-1)[:-3] + 'Z'
        else:
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, hours=-5.5, minutes=-1)[:-3] + 'Z'
        return date_from

    def date_to(self,minutes):
        # Time Zone validation

        if self.timezone.upper() == "UTC":
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, minutes=minutes)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-1, minutes=minutes)[:-3] + 'Z'
        else:
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-5.5, minutes=minutes)[:-3] + 'Z'
        return date_to

    def verify_BYB_widget_FE(self, byb_name: str,expected_result=True,):
        byb_container = self.site.home.has_byb_widget
        if byb_container:
            byb_widget_containers = self.site.home.byb_widget.items_as_ordered_dict
            for byb_widget_container_name, byb_widget_container in byb_widget_containers.items():
                # Verifying BYB Widget accordions
                byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup

                if self.device_type == 'mobile' and not byb_widgets:
                    if expected_result:
                        self.assertFalse(byb_widgets, msg='BYB Widget container still have market cards')

                self.assertTrue(byb_widgets, msg='BYB Widget is not present in Front End')
                byb_name_matched = False
                for byb_widget_name, byb_widget in byb_widgets.items():
                    byb_widget_name_v = byb_widget.name
                    if byb_name == byb_widget_name_v:
                        byb_name_matched = True
                        break
                self.assertEqual(expected_result, byb_name_matched,
                                 msg=f'expected result is: {expected_result} and byb names status in FE:{byb_name_matched} both are not same ')
        else:
            self.assertFalse(byb_container, msg="No Markets cards are available in BYB Widget but Container is Present in Front End")

    def test_000_preconditions(self):
        """
        Description: verifying existing Active Market cards in BYB Widget
        Expected:
        """
        byb_widget_active_market_cards = self.cms_config.get_byb_widget()
        byb_widget_datas = byb_widget_active_market_cards.get('data')
        byb_widget_card_locations = []
        byb_widget_cards_ids = []
        for byb_widget_data in byb_widget_datas:
            byb_widget_cards_ids.append(byb_widget_data['id'])
            byb_widget_card_locations.append(byb_widget_data.get('locations'))
        expected_locations = ['Sportbook Homepage']
        if len(byb_widget_card_locations) != 0:
            self.__class__.locations = []
            self.__class__.cms_market_id = None
            for byb_widget_data in byb_widget_datas:
                if self.cms_market_id:
                    break
                byb_widget_market_cards_ob = self.ss_req.ss_events_to_outcome_for_markets(
                    market_ids=[byb_widget_data['marketId']])
                for card_ob in byb_widget_market_cards_ob:
                    if card_ob['event']['isActive'] and card_ob['event']['eventStatusCode'] == 'A':
                        self.cms_config.update_market_cards(market_card_id=byb_widget_data['id'],
                                                            displayTo=self.date_to(minutes=2))
                        self.__class__.locations = byb_widget_data.get('locations')
                        self.__class__.cms_market_id = byb_widget_data['id']
                    if self.cms_market_id:
                        break

        else:
            self.cms_config.create_new_market_cards(title='Auto_BYB', event_id='',
                                                    market_id='', date_from=self.date_from(),
                                                    date_to=self.date_to(minutes=2), locations=expected_locations)
            self.__class__.locations = expected_locations

    def test_001_launch_the_cms_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the CMS and login with valid credentials
        EXPECTED: Able to launch CMS and login successfully
        """
        # verifying BYB widget is display or not
        for location in self.locations:
            if location == 'Sportbook Homepage':
                sport = "Homepage"
            else:
                sport = 'sport/football'
                state_name = 'Football'

            self.navigate_to_page(name=sport)
            self.site.wait_content_state(state_name=sport if sport == 'Homepage' else state_name, timeout=15)
            break
        # Verifying BYB Widget container in Front End
        byb_widget_containers = self.site.home.byb_widget.items_as_ordered_dict
        self.assertTrue(byb_widget_containers, msg='BYB Widget container is not present in Home Page')
        for byb_widget_container_name, byb_widget_container in byb_widget_containers.items():
            # Verifying BYB Widget accordions
            byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
            self.assertTrue(byb_widgets, msg='BYB Widget is not present in Front End')
            for byb_widget_name, byb_widget in byb_widgets.items():
                # verifying BYB widget cards
                self.__class__.byb_widget_name_v = byb_widget.name
                byb_sections = byb_widget.items_as_ordered_dict_inc_dup
                self.assertTrue(byb_sections, msg='BYB Widget cards is not present in Front End')
                break
        self.verify_BYB_widget_FE(expected_result=True, byb_name=self.byb_widget_name_v)
        # wait 1 mint
        wait_for_haul(120)
        # Verifying BYB widget container in Front End with expected false
        self.verify_BYB_widget_FE(expected_result=False, byb_name=self.byb_widget_name_v)

        # updating date in BYB widget expired market card
        self.cms_config.updated_byb_expired_market_cards(market_card_id=self.cms_market_id,
                                                         displayTo=self.date_to(minutes=40))
        wait_for_haul(5)
        # Verification BYB Widget is display in FE or not
        self.verify_BYB_widget_FE(expected_result=True, byb_name=self.byb_widget_name_v)

    def test_002_click_on_byb_main_section_and_navigate_to_the_byb_widget_sub_section(self):
        """
        DESCRIPTION: Click on BYB main section and navigate to the BYB widget sub section
        EXPECTED: User can able to navigate to the BYB widget sub section successfully
        """
        # Covered in above step

    def test_003_verify_the_display_of_expired_market_cards_table(self):
        """
        DESCRIPTION: Verify the Display of Expired Market Cards Table
        EXPECTED: User can able to see the Expired Market Cards Table
        """
        # covered in above step

    def test_004_verify_edit_icon_for_the_all_the_expired_records(self):
        """
        DESCRIPTION: Verify 'Edit Icon' for the all the expired records
        EXPECTED: Edit Icon' should be displayed for all the expired records
        """
        # Covered in above step
