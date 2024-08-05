package com.oxygen.publisher.sportsfeatured;

import com.oxygen.health.api.AbstractPublisherHealthIndicator;
import com.oxygen.health.api.AbstractServiceRegistry;
import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.sportsfeatured.configuration.FeaturedKafkaRecordConsumer;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.service.FeaturedIoServerHealthIndicatorService;
import com.oxygen.publisher.sportsfeatured.service.FeaturedServiceImpl;
import java.util.Arrays;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.health.Health;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportsHealthIndicator extends AbstractPublisherHealthIndicator {

  private List<Class<? extends ReloadableService>> servicesToCheck =
      Arrays.asList(
          FeaturedServiceImpl.class,
          FeaturedKafkaRecordConsumer.class,
          FeaturedIoServerHealthIndicatorService.class);
  private AbstractServiceRegistry featuredServiceRegistry;
  private SportsMiddlewareContext featuredMiddlewareContext;

  @Value("${skip.health.check:false}")
  private boolean skipHealthCheck;

  @Autowired
  public SportsHealthIndicator(
      AbstractServiceRegistry featuredServiceRegistry,
      SportsMiddlewareContext featuredMiddlewareContext) {
    this.featuredServiceRegistry = featuredServiceRegistry;
    this.featuredMiddlewareContext = featuredMiddlewareContext;
  }

  @Override
  protected void doHealthCheck(Health.Builder builder) {
    builder.up();
    if (skipHealthCheck) {
      return;
    }
    summarize(builder, !featuredMiddlewareContext.getFeaturedCachedData().isEmpty());
    summarize(builder, checkServicesStatus());
  }

  @Override
  public List<Class<? extends ReloadableService>> getServicesToCheck() {
    return servicesToCheck;
  }

  @Override
  public AbstractServiceRegistry getServiceRegistry() {
    return featuredServiceRegistry;
  }
}
