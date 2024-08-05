from tests.Common import Common
from voltron.utils.waiters import wait_for_result


class BasePromotionTest(Common):

    def check_banner(self, page_name='Home', banner_name='Autotest Banner', timeout=10, is_present=True):
        self._logger.info('*** Verifying banner is present on %s' % page_name)
        banner_section = self.site.contents.banner_section
        banner_section.scroll_to_we()
        available_banners = banner_section.banners_names
        if is_present:
            self.assertTrue(banner_name in available_banners,
                            msg='%s is not in banners list %s, page %s' %
                                (banner_name, available_banners, self.site.content_state))
            timeout = timeout * len(available_banners)
            banner_presence = wait_for_result(lambda: banner_section.active_banner_name == banner_name,
                                              name='Active banner "%s" to become active, current "%s"' % (
                                                  banner_name,
                                                  banner_section.active_banner_name
                                              ),
                                              timeout=timeout,
                                              poll_interval=1.5)
            self.assertTrue(banner_presence,
                            msg='Expected banner "%s" is not active after %s sec. Available banners list: %s' %
                                (banner_name, timeout, available_banners))
        else:
            self.assertFalse(banner_name in available_banners,
                             msg='%s is in banners list' % banner_name)

    def check_banner_on_sport_page(self, name='football', banner_name='Autotest Banner', is_present=True):
        self.navigate_to_page(name=name)
        self.check_banner(page_name='Sport', banner_name=banner_name, is_present=is_present)
