from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import tests
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from collections import OrderedDict


class BaseCouponsTest(BaseSportTest):

    def basic_active_events_filter(self):
        """
        Default filter for view list of all coupons
        """
        return self.ss_query_builder.add_filter(
            exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN,
                                                       self.start_date_minus)))

    def find_coupon_and_open_it(self, coupon_name: str, **kwargs):
        """
        Opens coupon details page of 'coupon_name' coupon
        :param coupon_section: One of coupon categories
        :param coupon_name: Name of coupon which belongs to coupon_section
        """
        coupon_section = kwargs.get('coupon_section')
        if coupon_section:
            coupons_list = self.get_coupons_list_in_coupons_section(coupon_section)
        else:
            coupon_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(coupon_categories, msg='Can not find any coupon category')
            coupons_list = OrderedDict([])
            for coupon_group_name, coupon_group in coupon_categories.items():
                coupons = coupon_group.items_as_ordered_dict
                self.assertTrue(coupons, msg=f'No coupons found in {coupon_group_name} group')
                coupons_list.update(coupons)

        self.assertIn(coupon_name, coupons_list.keys(),
                      msg=f'"{coupon_name}" is not found in list of coupons "{coupons_list.keys()}"')
        coupons_list.get(coupon_name).click()
        self.site.wait_content_state('CouponPage')

    def get_coupons_list_in_coupons_section(self, coupon_section: str) -> OrderedDict:
        """
        :param coupon_section: One of coupon categories
        :return: All coupons which belongs to provided coupon_section
        """
        coupon_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupon_categories, msg='Can not find any coupon category')

        coupon_section = coupon_categories.get(coupon_section, None)
        self.assertTrue(coupon_section, msg=f'Can not find: "{coupon_section}" coupon')
        coupons_list = coupon_section.items_as_ordered_dict
        self.assertTrue(coupons_list, msg='Can not find any coupon')

        return coupons_list

    def get_active_coupons_list(self):
        coupon_resp = self.get_active_coupons_response()
        return [x['coupon']['name'] for x in coupon_resp]

    def get_active_coupons_response(self):
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   category_id=self.ob_config.backend.ti.football.category_id,
                                   brand=self.brand)

        self.ss_query_builder.add_filter(
            exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN,
                                                       self.start_date_minus)))
        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'

        active_coupons_query = self.basic_active_events_filter() \
            .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME,
                                                                   OPERATORS.GREATER_THAN_OR_EQUAL, start_date))) \
            .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED,
                                                                   OPERATORS.IS_FALSE))) \
            .add_filter(simple_filter(LEVELS.COUPON, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID,
                                                                   OPERATORS.INTERSECTS,
                                                                   self.ob_config.backend.ti.football.category_id)))
        coupon_resp = ss_req.ss_coupon(query_builder=active_coupons_query)
        return coupon_resp
