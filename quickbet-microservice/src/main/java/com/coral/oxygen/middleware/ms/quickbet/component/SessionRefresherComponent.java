package com.coral.oxygen.middleware.ms.quickbet.component;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionRefresher;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;

/**
 * @author volodymyr.masliy
 */
@Component
public final class SessionRefresherComponent {
  private SessionRefresher<String> sessionRefresher;
  private ConcurrentMap<String, ScheduledFuture> scheduledRefreshments;

  @Autowired
  public SessionRefresherComponent(
      SessionStorage<SessionDto> sessionStorage, @Value("${session.ttl.minutes}") Long sessionTtl) {
    this.sessionRefresher =
        new SessionRefresher<>(
            sessionStorage::refreshTtl,
            new SessionRefresher.TimeAmount(sessionTtl, TimeUnit.MINUTES));
    this.scheduledRefreshments = new ConcurrentHashMap<>();
  }

  public void registerSession(String sessionId) {
    Assert.notNull(sessionId, "sessionId cannot be null");
    if (scheduledRefreshments.containsKey(sessionId)) {
      unregisterSession(sessionId);
    }

    scheduledRefreshments.put(sessionId, sessionRefresher.registerSession(sessionId));
  }

  public void unregisterSession(String sessionId) {
    Assert.notNull(sessionId, "sessionId cannot be null");
    if (scheduledRefreshments.containsKey(sessionId)) {
      ScheduledFuture scheduledRefresh = scheduledRefreshments.get(sessionId);
      scheduledRefresh.cancel(true);
      scheduledRefreshments.remove(sessionId);
    }
  }
}
