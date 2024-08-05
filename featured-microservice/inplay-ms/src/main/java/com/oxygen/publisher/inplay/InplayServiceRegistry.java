package com.oxygen.publisher.inplay;

import com.corundumstudio.socketio.SocketIOServer;
import com.oxygen.health.api.AbstractServiceRegistry;
import com.oxygen.publisher.inplay.service.InplayConsumerApi;
import com.oxygen.publisher.inplay.service.InplayConsumerApiProvider;
import com.oxygen.publisher.inplay.service.InplayDataService;
import com.oxygen.publisher.inplay.service.InplayDataServiceImpl;
import com.oxygen.publisher.inplay.service.InplayKafkaRecordConsumer;
import com.oxygen.publisher.inplay.service.InplaySocketServerHealthService;
import com.oxygen.publisher.server.SocketIOConnector;
import com.oxygen.publisher.service.CallExecutorService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ConfigurableApplicationContext;

/** Created by Aliaksei Yarotski on 1/29/18. */
@Slf4j
public class InplayServiceRegistry extends AbstractServiceRegistry {

  public SocketIOServer getSocketIOServer() {
    return super.getServiceAndReloadFailed(SocketIOConnector.class).getServer();
  }

  public InplayConsumerApi getInplayConsumerApi() {
    return super.getServiceAndReloadFailed(InplayConsumerApiProvider.class).getInplayConsumerApi();
  }

  public InplayDataService getInplayDataService() {
    return super.getServiceAndReloadFailed(InplayDataServiceImpl.class);
  }

  public InplayServiceRegistry(ConfigurableApplicationContext appContext) {
    // order is important here
    super(
        appContext,
        new Class[] {
          InplayConsumerApiProvider.class,
          InplayDataServiceImpl.class,
          SocketIOConnector.class,
          CallExecutorService.class,
          InplayKafkaRecordConsumer.class,
          InplayHealthIndicator.class,
          InplaySocketServerHealthService.class,
        });
  }
}
