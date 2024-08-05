package com.oxygen.publisher.inplay;

import static org.junit.Assert.assertEquals;
import static org.mockito.BDDMockito.given;

import com.oxygen.publisher.inplay.context.InplayMiddlewareContext;
import com.oxygen.publisher.inplay.service.InplayKafkaRecordConsumer;
import com.oxygen.publisher.inplay.service.InplaySocketServerHealthService;
import com.oxygen.publisher.model.InplayCachedData;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.Status;

@RunWith(MockitoJUnitRunner.class)
public class InplayHealthIndicatorTest {

  private InplayHealthIndicator testedEntity;
  @Mock private InplayMiddlewareContext inplayMiddlewareContext;
  @Mock private InplayServiceRegistry inplayServiceRegistry;
  @Mock private InplayCachedData inplayCachedData;
  @Mock private InplayKafkaRecordConsumer inplayKafkaRecordConsumer;
  @Mock private InplaySocketServerHealthService inplaySocketServerHealthService;

  @Before
  public void init() {
    testedEntity = new InplayHealthIndicator(inplayMiddlewareContext, inplayServiceRegistry);
    given(inplayMiddlewareContext.getInplayCachedData()).willReturn(inplayCachedData);
    given(inplayServiceRegistry.getService(InplayKafkaRecordConsumer.class))
        .willReturn(inplayKafkaRecordConsumer);
    given(inplayServiceRegistry.getService(InplaySocketServerHealthService.class))
        .willReturn(inplaySocketServerHealthService);
  }

  @Test
  public void upStatusCheckOk() {
    Health.Builder builder = new Health.Builder();
    given(inplayCachedData.isEmpty()).willReturn(false);
    given(inplayKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(true);
    given(inplaySocketServerHealthService.getHealthStatusForExternal()).willReturn(true);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.UP);
  }

  @Test
  public void statusEmptyData() {
    Health.Builder builder = new Health.Builder();
    given(inplayCachedData.isEmpty()).willReturn(true);
    given(inplayKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(true);
    given(inplaySocketServerHealthService.getHealthStatusForExternal()).willReturn(true);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void statusCheckIfServiceDown0() {
    Health.Builder builder = new Health.Builder();
    given(inplayCachedData.isEmpty()).willReturn(false);

    given(inplayKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(true);
    given(inplaySocketServerHealthService.getHealthStatusForExternal()).willReturn(false);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void statusCheckIfServiceDown1() {
    Health.Builder builder = new Health.Builder();
    given(inplayCachedData.isEmpty()).willReturn(false);

    given(inplayKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(false);
    given(inplaySocketServerHealthService.getHealthStatusForExternal()).willReturn(true);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void statusCheckNotReady() {
    Health.Builder builder = new Health.Builder();
    given(inplayCachedData.isEmpty()).willReturn(true);

    given(inplayKafkaRecordConsumer.getHealthStatusForExternal()).willReturn(false);
    given(inplaySocketServerHealthService.getHealthStatusForExternal()).willReturn(false);

    testedEntity.doHealthCheck(builder);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }
}
