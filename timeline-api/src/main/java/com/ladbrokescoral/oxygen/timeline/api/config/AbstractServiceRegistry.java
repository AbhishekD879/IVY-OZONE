package com.ladbrokescoral.oxygen.timeline.api.config;

import com.ladbrokescoral.oxygen.timeline.api.registrators.ReloadableService;
import java.util.Arrays;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ConfigurableApplicationContext;

/** Created by Aliaksei Yarotski on 1/30/18. */
@Slf4j
public abstract class AbstractServiceRegistry {

  private final ConfigurableApplicationContext appContext;
  private Map<Class<? extends ReloadableService>, ReloadableService> registry =
      new ConcurrentHashMap<>();
  private final Class<? extends ReloadableService>[] services;

  protected AbstractServiceRegistry(
      ConfigurableApplicationContext appContext, Class<? extends ReloadableService>[] services) {
    this.appContext = appContext;
    this.services = services;
  }

  public void load() {
    try {
      Arrays.stream(services)
          .forEach(
              (Class<? extends ReloadableService> clazz) -> {
                ReloadableService service = appContext.getBean(clazz);
                if (!service.isHealthy()) {
                  service.start();
                }
                registry.put(clazz, service);
              });
    } catch (Exception e) {
      log.error(
          "Services failed to load. Check services order in AbstractServiceRegistry implementation.",
          e);
      throw e;
    }
  }

  public void stop() {
    registry.values().forEach(service -> service.evict());
  }

  public <T extends ReloadableService> T getService(Class<T> clazz) {
    return (T)
        Optional.ofNullable(registry.get(clazz))
            .orElseThrow(
                () ->
                    new IllegalStateException(
                        String.format(
                            "Service %s isn't present in register. "
                                + "Check services order declaration in AbstractServiceRegistry implementation.",
                            clazz.getSimpleName())));
  }

  public <T extends ReloadableService> T getServiceAndReloadFailed(Class<T> clazz) {
    ReloadableService service = getService(clazz);
    if (!service.isHealthy()) {
      return pushReload(clazz);
    }
    return (T) registry.get(clazz);
  }

  public synchronized <T extends ReloadableService> T pushReload(Class<T> clazz) {
    if (null != registry.get(clazz)) {
      if (registry.get(clazz).isHealthy()) {
        return (T) registry.get(clazz);
      }
      registry.get(clazz).evict();
    } else {
      log.error(
          String.format(
              "Service %s failed to evict for {}. Can't find it in service registry.",
              clazz.getSimpleName()));
    }
    T result = appContext.getBean(clazz);
    result.start();
    registry.put(clazz, result);
    log.info("[AbstractServiceRegistry:pushReload] {} started.", clazz.getSimpleName());
    return result;
  }
}
