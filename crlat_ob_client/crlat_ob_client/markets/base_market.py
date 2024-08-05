"""
This module contains Base Market Templates for Multiple Market creation
"""
from abc import ABC, abstractmethod

from crlat_ob_client.utils.exceptions import OBException


class BaseMarketEntity(ABC):

    def __init__(self, **kwargs):
        self.event_id = kwargs.get('eventID')
        self.market_name = kwargs.get('market_name')
        self.market_template_id = kwargs.get('market_template_id')
        self.market_disporder = kwargs.get('market_disporder')
        self.market_display_sort_code = None

    @abstractmethod
    def _generate_params(self):
        return OBException('This method should be implemented in child classes')

    def build_params(self):
        return self._generate_params()
