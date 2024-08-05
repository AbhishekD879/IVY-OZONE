from crlat_ws_clients.abc_base.base_application import BaseApplication
from crlat_ws_clients.clients.vis_client_model.vis_client_domain import VisClientEntity
from crlat_ws_clients.clients.vis_client_model.vis_lt_listener import VisLoadTestTListenerEntity


class VisApp(BaseApplication):
    def __init__(
            self,
            success_hooks=None,
            failure_hooks=None,
            *args,
            **kwargs
    ):
        super().__init__(success_hooks=success_hooks, failure_hooks=failure_hooks, *args, **kwargs)
        self._domain = self._create_vis_client_entity()
        if success_hooks and failure_hooks:
            self._create_vis_lt_listener(
                success_hooks=success_hooks,
                failure_hooks=failure_hooks
            )

    def _create_vis_lt_listener(
            self,
            success_hooks=None,
            failure_hooks=None,
    ):
        event = VisLoadTestTListenerEntity.Created(
            application=self,
            success_hooks=success_hooks,
            failure_hooks=failure_hooks
        )
        vis_ltl = VisLoadTestTListenerEntity(event)
        return vis_ltl

    def _create_vis_client_entity(self) -> VisClientEntity:
        return VisClientEntity(VisClientEntity.Created(application=self))

    def connect_vis_srv(self, base_url='wss://vis-tst2-coral.symphony-solutions.eu/generic'):
        self._domain.fire_event(
            VisClientEntity.VisCliConnectServer,
            base_url=base_url
        )

    def unsubscribe_fb(
            self,
            openbet_id
    ):
        self._domain.fire_event(
            VisClientEntity.VisCliUnsubscribeFBMatch,
            openbet_id=openbet_id
        )

    def subscribe_fb(
            self,
            openbet_id
    ):
        self._domain.fire_event(
            VisClientEntity.VisCliSubscribeFBMatch,
            openbet_id=openbet_id
        )

    def unsubscribe_tennis(
            self,
            openbet_id
    ):
        self._domain.fire_event(
            VisClientEntity.VisCliUnsubscribeTennisMatch,
            openbet_id=openbet_id
        )

    def subscribe_tennis(
            self,
            openbet_id
    ):
        self._domain.fire_event(
            VisClientEntity.VisCliSubscribeTennisMatch,
            openbet_id=openbet_id
        )

    def disconnect_vis_srv(self):
        self._domain.fire_event(VisClientEntity.VisCliDisconnectServer)