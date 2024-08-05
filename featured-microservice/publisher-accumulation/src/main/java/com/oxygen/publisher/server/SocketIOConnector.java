package com.oxygen.publisher.server;

import com.corundumstudio.socketio.SocketIOServer;
import com.newrelic.api.agent.NewRelic;
import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.context.AbstractSessionContext;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RequiredArgsConstructor
public class SocketIOConnector implements ReloadableService {

  @Getter protected final SocketIOServer server;
  protected final AbstractSessionContext sessionContext;
  protected AtomicBoolean onService = new AtomicBoolean();

  @Override
  public void start() {
    sessionContext.registerListeners(server);
    server.addConnectListener(sessionContext::onConnect);
    server.addDisconnectListener(sessionContext::onDisconnect);
    sessionContext.getHealthCheckListener(server).registerListener(server);
    onService.set(true);
  }

  @Override
  public void evict() {
    onService.set(false);
  }

  @Override
  public boolean isHealthy() {
    return onService.get();
  }

  @Override
  public void onFail(Exception ex) {
    onService.set(false);
    log.error("SocketIOConnector server exception. ", ex);
    NewRelic.noticeError(ex);
  }
}
