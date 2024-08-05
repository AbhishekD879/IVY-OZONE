from voltron.pages.shared.contents.base_content import ComponentContent
from voltron.utils.waiters import wait_for_result


class BuildInfoJSONPage(ComponentContent):
    _url_pattern = r'^http[s]?:\/\/.+\/buildInfo.json$'

    def _wait_active(self, timeout=2):
        self._we = self._find_myself()
        return wait_for_result(lambda: self.get_json_content(),
                               name='buildInfo.json to load',
                               timeout=timeout)

    def get_json_content(self):
        return self._get_webelement_text(we=self._we)
