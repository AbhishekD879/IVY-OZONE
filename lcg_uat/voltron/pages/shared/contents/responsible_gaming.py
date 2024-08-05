from voltron.pages.shared.contents.responsible_gambling import ResponsibleGambling


class ResponsibleGaming(ResponsibleGambling):
    _url_pattern = r'^http[s]?:\/\/.+\/safer-gambling'
    _header_line = 'xpath=.//*[contains(@class,"pc-h header")] | .//*[contains(@class,"header-ctrl d-flex")]'

    @property
    def header_title(self):
        return self._get_webelement_text(selector=self._header_line, context=self._we)
