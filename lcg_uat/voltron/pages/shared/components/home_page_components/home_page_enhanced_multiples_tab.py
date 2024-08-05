from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent


class EnhancedMultiplesTabContent(TabContent):
    _accordions_list = 'xpath=..//*[contains(@data-crlat, "tab.showEnhancedMultiples")]'
    _verify_spinner = True
