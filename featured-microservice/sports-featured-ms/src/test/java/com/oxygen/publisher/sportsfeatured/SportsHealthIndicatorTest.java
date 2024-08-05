package com.oxygen.publisher.sportsfeatured;

import static org.junit.Assert.assertEquals;
import static org.mockito.BDDMockito.given;

import com.oxygen.publisher.sportsfeatured.configuration.FeaturedKafkaRecordConsumer;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.service.FeaturedIoServerHealthIndicatorService;
import com.oxygen.publisher.sportsfeatured.service.FeaturedServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.Status;

@RunWith(MockitoJUnitRunner.class)
public class SportsHealthIndicatorTest {

  private SportsHealthIndicator testedEntity;
  @Mock private SportsServiceRegistry featuredServiceRegistry;
  @Mock private SportsMiddlewareContext featuredMiddlewareContext;
  @Mock SportsCachedData sportsCachedData;
  @Mock private FeaturedServiceImpl featuredService;
  @Mock private FeaturedKafkaRecordConsumer featuredKafkaRecordConsumer;
  @Mock private FeaturedIoServerHealthIndicatorService ioHealthIndicator;

  @Before
  public void init() {
    testedEntity = new SportsHealthIndicator(featuredServiceRegistry, featuredMiddlewareContext);
    given(featuredMiddlewareContext.getFeaturedCachedData()).willReturn(sportsCachedData);
    given(featuredServiceRegistry.getService(FeaturedServiceImpl.class))
        .willReturn(featuredService);
    given(featuredServiceRegistry.getService(FeaturedKafkaRecordConsumer.class))
        .willReturn(featuredKafkaRecordConsumer);
    given(featuredServiceRegistry.getService(FeaturedIoServerHealthIndicatorService.class))
        .willReturn(ioHealthIndicator);
  }

  @Test
  public void upStatusCheckOk() {
    Health.Builder builder = new Health.Builder();
    given(sportsCachedData.isEmpty()).willReturn(false);
    given(featuredService.getHealthStatusForExternal()).willReturn(true);
    given(featuredKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(true);
    given(ioHealthIndicator.getHealthStatusForExternal()).willReturn(true);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.UP);
  }

  @Test
  public void statusEmptyData() {
    Health.Builder builder = new Health.Builder();
    given(sportsCachedData.isEmpty()).willReturn(true);
    given(featuredService.getHealthStatusForExternal()).willReturn(true);
    given(featuredKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(true);
    given(ioHealthIndicator.getHealthStatusForExternal()).willReturn(true);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void statusCheckIfServiceDown0() {
    Health.Builder builder = new Health.Builder();
    given(sportsCachedData.isEmpty()).willReturn(false);

    given(featuredService.getHealthStatusForExternal()).willReturn(false);
    given(featuredKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(true);
    given(ioHealthIndicator.getHealthStatusForExternal()).willReturn(true);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void statusCheckIfServiceDown1() {
    Health.Builder builder = new Health.Builder();
    given(sportsCachedData.isEmpty()).willReturn(false);

    given(featuredService.getHealthStatusForExternal()).willReturn(true);
    given(featuredKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(false);
    given(ioHealthIndicator.getHealthStatusForExternal()).willReturn(true);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void statusCheckIfServiceDown2() {
    Health.Builder builder = new Health.Builder();
    given(sportsCachedData.isEmpty()).willReturn(false);

    given(featuredService.getHealthStatusForExternal()).willReturn(true);
    given(featuredKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(true);
    given(ioHealthIndicator.getHealthStatusForExternal()).willReturn(false);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }
}
