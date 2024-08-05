from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class VirtualEntryPointBanner(ComponentBase):
    _play_now_button = 'xpath=.//button[@class="btn"]'
    _image = 'xpath=.img'

    @property
    def image_url(self):
        we = self._find_element_by_selector(selector=self._image)
        if we:
            return we.get_attribute('src')
        return ''

    @property
    def play_now_button(self):
        return ButtonBase(selector=self._play_now_button, context=self._we)
