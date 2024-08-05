package com.oxygen.health.api;

import com.newrelic.api.agent.NewRelic;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.actuate.health.AbstractHealthIndicator;
import org.springframework.boot.actuate.health.Health.Builder;
import org.springframework.boot.actuate.health.Status;

/**
 * A custom Spring Boot health indicator of this service. Checks whether SocketIOConnector is
 * started and
 *
 * @author tvuyiv
 */
@RequiredArgsConstructor
@Slf4j
public abstract class AbstractPublisherHealthIndicator extends AbstractHealthIndicator
    implements ReloadableService {

  private Status applicationStatus = Status.UP;

  protected boolean checkServicesStatus() {
    StringBuilder errorMessage = new StringBuilder();
    try {
      for (Class<? extends ReloadableService> service : getServicesToCheck()) {
        if (!getServiceRegistry().getService(service).getHealthStatusForExternal()) {
          errorMessage.append(service.getSimpleName()).append(" is down. ");
        }
      }
    } catch (IllegalArgumentException e) {
      log.error("Failed to check health status.", e);
      NewRelic.noticeError(e);
      return false;
    }
    if (errorMessage.length() > 0) {
      String msg = errorMessage.toString();
      log.warn(msg);
      NewRelic.noticeError(msg);
      return false;
    } else {
      return true;
    }
  }

  /**
   * This approach is summarizing the status of the health check.
   *
   * @param builder health status Spring representation.
   */
  protected final void summarize(Builder builder, Status status) {
    if (status == null) {
      builder.down();
    } else if (Status.UP.equals(builder.build().getStatus())) {
      builder.status(status);
    }
  }

  /**
   * This approach is summarizing the status of the health check.
   *
   * @param builder health status Spring representation.
   */
  protected final void summarize(Builder builder, boolean isHealthy) {
    if (isHealthy) {
      summarize(builder, Status.UP);
    } else {
      summarize(builder, Status.DOWN);
    }
  }

  @Override
  public void start() {
    applicationStatus = Status.UP;
  }

  @Override
  public void evict() {}

  @Override
  public boolean isHealthy() {
    return applicationStatus.equals(Status.UP);
  }

  @Override
  public void onFail(Exception ex) {}

  public abstract List<Class<? extends ReloadableService>> getServicesToCheck();

  public abstract AbstractServiceRegistry getServiceRegistry();
}
