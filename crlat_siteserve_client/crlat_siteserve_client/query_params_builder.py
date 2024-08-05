
class SimpleFilterBuilder:
    def __init__(self, level, attribute, operator=None, value=None):
        self.level = level
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def build(self):
        query = f'{self.level}.{self.attribute}'
        query += f':{self.operator}' if self.operator else ''
        query += f':{self.value}' if self.value else ''
        return 'simpleFilter', query


class ExistsFilterBuilder:
    def __init__(self, level, filter_builder):
        self.level = level
        self.filter_builder = filter_builder

    def build(self):
        filter_name, filter_value = self.filter_builder.build()
        return 'existsFilter', f'{self.level}:{filter_name}:{filter_value}'


class ExternalKeysBuilder:
    def __init__(self, level):
        self.level = level

    def build(self):
        return 'externalKeys', self.level


class QueryBuilder:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_builder):
        self.filters.append(filter_builder.build())
        return self

    def build(self):
        return self.filters


class TranslationLangFilterBuilder:
    def __init__(self, lang: str='en'):
        self.lang = lang

    def build(self):
        return 'translationLang', self.lang


class ResponseFormatFilterBuilder:
    def __init__(self, r_format: str = 'json'):
        self.r_format = r_format

    def build(self):
        return 'responseFormat', self.r_format


class ChildCountFilterBuilder:
    def __init__(self, value: str='event'):
        self.value = value

    def build(self):
        return 'childCount', self.value


class RacingFormFilterBuilder:
    def __init__(self, level: str='event'):
        self.level = level

    def build(self):
        return 'racingForm', self.level


class PruneFilterBuilder:
    def __init__(self, level: str='event'):
        self.level = level

    def build(self):
        return 'prune', self.level


class PriceHistoryFilterBuilder:
    def __init__(self, value: str='true'):
        self.value = value

    def build(self):
        return 'priceHistory', self.value


class LimitRecordsFilterBuilder:
    def __init__(self, level: str, value: str):
        self.level = level
        self.value = value

    def build(self):
        return 'limitRecords', f'{self.level}:{self.value}'


class DebugFilterBuilder:
    def __init__(self, value: str='includeHiddenFields'):
        self.value = value

    def build(self):
        return 'debug', self.value
