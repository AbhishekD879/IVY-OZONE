package com.ladbrokescoral.oxygen.timeline.api.registrators;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.junit.MockitoJUnitRunner;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@RunWith(MockitoJUnitRunner.class)
public class PagePublisherChannelRegistratorTest {
  @InjectMocks private PagePublisherChannelRegistrator registrator;

  @Test
  public void testStart() {
    StepVerifier.create(Mono.fromRunnable(() -> registrator.start())).verifyComplete();
    assertTrue(registrator.isHealthy());
  }

  @Test
  public void testEvict() {
    registrator.evict();
    assertFalse(registrator.isHealthy());
  }

  @Test
  public void testEvictForExternal() {
    registrator.evict();
    assertFalse(registrator.getHealthStatusForExternal());
  }

  @Test
  public void testFail() {
    RuntimeException exception = new RuntimeException();
    registrator.onFail(exception);
    assertFalse(registrator.isHealthy());
  }
}
