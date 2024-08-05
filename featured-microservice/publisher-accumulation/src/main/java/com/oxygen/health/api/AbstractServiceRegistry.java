package com.oxygen.health.api;

import com.newrelic.api.agent.NewRelic;
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
  private Map<Class, ReloadableService> registry = new ConcurrentHashMap<>();
  private final Class<? extends ReloadableService>[] services;

  public AbstractServiceRegistry(
      ConfigurableApplicationContext appContext, Class<? extends ReloadableService>[] services) {
    this.appContext = appContext;
    this.services = services;
  }

  public void load() {
    try {
      Arrays.stream(services)
          .forEach(
              clazz -> {
                ReloadableService service = appContext.getBean(clazz);
                if (!service.isHealthy()) {
                  service.start();
                }
                registry.put(clazz, service);
              });
    } catch (Exception e) {
      NewRelic.noticeError(e);
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
      NewRelic.noticeError(
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

  public boolean isOnService() {
    boolean isOnService = true;
    for (ReloadableService service : registry.values()) {
      try {
        log.info(
            "[AbstractServiceRegistry:isOnService] {} - {}",
            service.getClass().getSimpleName(),
            service.isHealthy());
        if (!service.isHealthy()) {
          isOnService = false;
        }
      } catch (Exception e) {
        log.error(
            "[AbstractServiceRegistry:isOnService] {} - ERROR", service.getClass().getSimpleName());
        isOnService = false;
      }
    }
    return isOnService;
  }
}
