package com.oxygen.publisher.sportsfeatured;

import com.corundumstudio.socketio.SocketIOServer;
import com.oxygen.health.api.AbstractServiceRegistry;
import com.oxygen.publisher.server.SocketIOConnector;
import com.oxygen.publisher.service.CallExecutorService;
import com.oxygen.publisher.sportsfeatured.configuration.FeaturedApiProvider;
import com.oxygen.publisher.sportsfeatured.configuration.FeaturedKafkaRecordConsumer;
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi;
import com.oxygen.publisher.sportsfeatured.service.FeaturedIoServerHealthIndicatorService;
import com.oxygen.publisher.sportsfeatured.service.FeaturedService;
import com.oxygen.publisher.sportsfeatured.service.FeaturedServiceImpl;
import com.oxygen.publisher.sportsfeatured.service.SportsPageIdRegistration;
import lombok.ToString;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ConfigurableApplicationContext;

/** Created by Aliaksei Yarotski on 1/11/18. */
@ToString
@Slf4j
public class SportsServiceRegistry extends AbstractServiceRegistry {

  public FeaturedService getFeaturedService() {
    return super.getServiceAndReloadFailed(FeaturedServiceImpl.class);
  }

  public SocketIOServer getSocketIOServer() {
    return super.getServiceAndReloadFailed(SocketIOConnector.class).getServer();
  }

  public SportsPageIdRegistration getSportsPageIdRegistration() {
    return super.getServiceAndReloadFailed(SportsPageIdRegistration.class);
  }

  public FeaturedApi getFeaturedApi() {
    return super.getServiceAndReloadFailed(FeaturedApiProvider.class).featuredApi();
  }

  public FeaturedApiProvider getFeaturedApiProvider() {
    return super.getServiceAndReloadFailed(FeaturedApiProvider.class);
  }

  public SportsServiceRegistry(ConfigurableApplicationContext appContext) {
    // order is important here
    super(
        appContext,
        new Class[] {
          FeaturedApiProvider.class,
          FeaturedServiceImpl.class,
          CallExecutorService.class,
          SportsPageIdRegistration.class,
          SocketIOConnector.class,
          SportsHealthIndicator.class,
          FeaturedKafkaRecordConsumer.class,
          FeaturedIoServerHealthIndicatorService.class,
        });
  }
}
