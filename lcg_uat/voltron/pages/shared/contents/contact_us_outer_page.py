from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.waiters import wait_for_result


class ContactUsOuterPage(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/Contact-Us'
    _profile_icon = 'xpath=.//img[contains(@class, "profileIcon")]'
    _user_name = 'xpath=.//span[contains(@class, "profileName")]'

    def is_profile_icon_shown(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._profile_icon, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Profile icon shown status to be {expected_result}')

    @property
    def user_name(self):
        return self._get_webelement_text(selector=self._user_name, timeout=5)
