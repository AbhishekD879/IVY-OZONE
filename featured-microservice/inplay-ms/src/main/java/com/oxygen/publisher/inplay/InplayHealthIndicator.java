package com.oxygen.publisher.inplay;

import com.oxygen.health.api.AbstractPublisherHealthIndicator;
import com.oxygen.health.api.AbstractServiceRegistry;
import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext;
import com.oxygen.publisher.inplay.service.InplayKafkaRecordConsumer;
import com.oxygen.publisher.inplay.service.InplaySocketServerHealthService;
import java.util.Arrays;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.actuate.health.Health;
import org.springframework.stereotype.Component;

/**
 * Health indicator should report that application is up only when it's ready to return data to
 * client. Otherwise client may get null structures in the response (BMA-30091)
 */
@Slf4j
@Component
public class InplayHealthIndicator extends AbstractPublisherHealthIndicator {

  private List<Class<? extends ReloadableService>> servicesToCheck =
      Arrays.asList(InplayKafkaRecordConsumer.class, InplaySocketServerHealthService.class);
  private InplayMiddlewareContext inplayMiddlewareContext;
  private AbstractServiceRegistry inplayServiceRegistry;

  public InplayHealthIndicator(
      InplayMiddlewareContext inplayMiddlewareContext, AbstractServiceRegistry serviceRegistry) {
    this.inplayMiddlewareContext = inplayMiddlewareContext;
    this.inplayServiceRegistry = serviceRegistry;
  }

  @Override
  protected void doHealthCheck(Health.Builder builder) {
    builder.up();
    summarize(builder, !inplayMiddlewareContext.getInplayCachedData().isEmpty());
    summarize(builder, checkServicesStatus());
  }

  @Override
  public List<Class<? extends ReloadableService>> getServicesToCheck() {
    return servicesToCheck;
  }

  @Override
  public AbstractServiceRegistry getServiceRegistry() {
    return inplayServiceRegistry;
  }
}
