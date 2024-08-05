import re
from time import sleep

from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result


class BaseAEMBannersTest(Common):

    @classmethod
    def custom_setUp(cls):
        dynamic_banners_config = cls.get_initial_data_system_configuration().get('DynamicBanners')
        if not dynamic_banners_config:
            dynamic_banners_config = cls.get_cms_config().get_system_configuration_item('DynamicBanners')
        if not dynamic_banners_config.get('enabled'):
            raise CmsClientException('AEM dynamic banners are turned OFF now')

    def get_offers_url(self):
        sleep(10)  # have to do this, when navigating thru site we need to wait some time before getting new performance
        # entries since the offers request might still not be performed
        data = self.site.get_performance_entries
        offers_url = next((item.get('name') for item in reversed(data) if re.findall(r'^https:\/\/(.*?)(offers.json)',
                                                                                     item.get('name'))), None)
        self._logger.debug(f'*** Offers URL is: "{offers_url}"')
        return offers_url

    def get_offers_response(self):
        """
        This method gets offers response based on offers call url
        :return: List of dictionaries with AEM banners info
        """
        self.site.contents.aem_banner_section.wait_for_banners()
        offers_call_url = self.get_offers_url()
        self.assertTrue(offers_call_url, msg='AEM banners offers call not found')
        self._logger.info('*** Doing request %s' % offers_call_url)
        content = do_request(method='GET', url=offers_call_url)
        self.assertIn('offers', content, msg='Network call with offers for AEM banners not found')
        contents = content['offers']
        if content.get('rg'):
            contents.append(content['rg'])
        if content.get('pinned'):
            for pinned_offer in content['pinned']:
                contents.append(content['pinned'][pinned_offer])
        return contents

    def wait_for_next_banner(self):
        cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners', {})
        if not cms_banners:
            cms_banners = self.cms_config.get_system_configuration_item('DynamicBanners')
        time_per_slide = cms_banners.get('timePerSlide')
        if time_per_slide is None:
            raise CmsClientException('timePerSlide value not configured in CMS')
        timeout = int(time_per_slide)

        current_page = self.site.contents
        start_active_banner_index = current_page.aem_banner_section.active_banner_index
        return wait_for_result(lambda: current_page.aem_banner_section.active_banner_index != start_active_banner_index,
                               name='Next AEM banner to load',
                               timeout=(timeout + timeout),
                               poll_interval=timeout / 2)
