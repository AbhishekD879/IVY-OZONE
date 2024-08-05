package com.ladbrokescoral.oxygen.timeline.api.registrators;

import com.ladbrokescoral.oxygen.timeline.api.config.AbstractServiceRegistry;
import java.lang.reflect.Field;
import java.util.Map;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.util.ReflectionUtils;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@DirtiesContext
public class TimelineServiceRegistryTest {
  @Autowired TimelineServiceRegistry serviceRegistry;
  @Autowired ConfigurableApplicationContext context;

  @Before
  public void setUp() {
    serviceRegistry = new TimelineServiceRegistry(context);
  }

  @Test
  public void testLoad() {
    StepVerifier.create(Mono.fromRunnable(() -> serviceRegistry.load())).verifyComplete();
  }

  @Test
  public void testLoadCase2() {
    StepVerifier.create(Mono.fromRunnable(() -> serviceRegistry.load())).verifyComplete();
  }

  @Test
  public void testLoadForException() {
    serviceRegistry = new TimelineServiceRegistry(null);
    StepVerifier.create(Mono.fromRunnable(() -> serviceRegistry.load())).expectError().verify();
  }

  @Test(expected = IllegalStateException.class)
  public void testgetService() {
    serviceRegistry.getService(PagePublisherChannelRegistrator.class);
  }

  @Test
  public void testgetServiceAndReloadFailed() {
    serviceRegistry.load();
    StepVerifier.create(
            Mono.fromRunnable(
                () ->
                    serviceRegistry.getServiceAndReloadFailed(
                        PagePublisherChannelRegistrator.class)))
        .verifyComplete();
  }

  @Test
  public void testgetServiceAndReloadFailedForUnHealthy() throws IllegalAccessException {
    PagePublisherChannelRegistrator page = Mockito.mock(PagePublisherChannelRegistrator.class);
    Field field = ReflectionUtils.findField(AbstractServiceRegistry.class, "registry");
    field.setAccessible(true);
    Map<Class<? extends ReloadableService>, ReloadableService> map =
        (Map<Class<? extends ReloadableService>, ReloadableService>) field.get(serviceRegistry);
    map.put(PagePublisherChannelRegistrator.class, page);

    Mockito.when(page.isHealthy()).thenReturn(false);

    // serviceRegistry.load();
    StepVerifier.create(
            Mono.fromRunnable(
                () ->
                    serviceRegistry.getServiceAndReloadFailed(
                        PagePublisherChannelRegistrator.class)))
        .verifyComplete();
  }

  @Test
  public void testpushReload() {
    serviceRegistry.load();
    StepVerifier.create(
            Mono.fromRunnable(
                () -> serviceRegistry.pushReload(PagePublisherChannelRegistrator.class)))
        .verifyComplete();
  }

  @Test
  public void testpushReloadException() throws IllegalAccessException {
    PagePublisherChannelRegistrator page = Mockito.mock(PagePublisherChannelRegistrator.class);
    Field field = ReflectionUtils.findField(AbstractServiceRegistry.class, "registry");
    field.setAccessible(true);
    Map<Class<? extends ReloadableService>, ReloadableService> map =
        (Map<Class<? extends ReloadableService>, ReloadableService>) field.get(serviceRegistry);
    map.put(PagePublisherChannelRegistrator.class, page);

    Mockito.when(page.isHealthy()).thenReturn(false);

    // serviceRegistry.load();
    StepVerifier.create(
            Mono.fromRunnable(
                () -> serviceRegistry.pushReload(PagePublisherChannelRegistrator.class)))
        .verifyComplete();
  }

  @Test
  public void testpushReloadExceptionNull() {
    // serviceRegistry.load();
    StepVerifier.create(
            Mono.fromRunnable(
                () -> serviceRegistry.pushReload(PagePublisherChannelRegistrator.class)))
        .verifyComplete();
  }

  @Test
  public void testStop() {
    StepVerifier.create(Mono.fromRunnable(() -> serviceRegistry.stop())).verifyComplete();
  }

  @Test
  public void testgetPagePublisherChannelRegistrator() {
    serviceRegistry.load();
    StepVerifier.create(
            Mono.fromRunnable(() -> serviceRegistry.getPagePublisherChannelRegistrator()))
        .verifyComplete();
  }
}
