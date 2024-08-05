package com.oxygen.publisher.inplay.context;

import com.corundumstudio.socketio.SocketIOServer;
import com.oxygen.publisher.inplay.InplayServiceRegistry;
import com.oxygen.publisher.inplay.service.InplayDataService;
import com.oxygen.publisher.model.InplayCachedData;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 1/29/18. */
@Slf4j
public class InplayMiddlewareContext {

  @Getter @Setter private InplayServiceRegistry serviceRegistry;

  @Getter private InplayCachedData inplayCachedData;

  public InplayMiddlewareContext(InplayServiceRegistry serviceRegistry) {
    this.serviceRegistry = serviceRegistry;
    inplayCachedData = new InplayCachedData();
  }

  public InplayDataService inplayDataService() {
    return serviceRegistry.getInplayDataService();
  }

  public SocketIOServer socketIOServer() {
    return serviceRegistry.getSocketIOServer();
  }

  public void applyWorkingCache(InplayCachedData newInplayCachedData) {
    synchronized (newInplayCachedData.getEntityGUID().intern()) {
      if (this.inplayCachedData != null
          && newInplayCachedData.getEntityGUID().equals(this.inplayCachedData.getEntityGUID())) {
        log.info("[InplayMiddlewareContext:applyWorkingCache] lock released, no updates.");
        return;
      }
      this.inplayCachedData = newInplayCachedData;
      log.info(
          "[InplayMiddlewareContext:applyWorkingCache] {} New cache has been applied from chain.",
          inplayCachedData.getVersion());
    }
  }
}
