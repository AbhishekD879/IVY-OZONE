package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.coral.oxygen.middleware.ms.quickbet.BaseSession;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.SessionNotFoundException;
import com.coral.oxygen.middleware.ms.quickbet.component.SessionRefresherComponent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.stream.Collectors;
import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class SessionManager {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private ConcurrentMap<UUID, Session> sessionMap;
  private SessionStorage<SessionDto> sessionStorage;
  private SessionRefresherComponent sessionRefresherComponent;

  @Autowired
  public SessionManager(
      SessionStorage<SessionDto> sessionStorage,
      SessionRefresherComponent sessionRefresherComponent) {
    this.sessionMap = new ConcurrentHashMap<>();
    this.sessionStorage = sessionStorage;
    this.sessionRefresherComponent = sessionRefresherComponent;
  }

  public Session loadPersistedSession(String sessionId) throws SessionNotFoundException {
    BaseSession session = new BaseSession(sessionId, sessionStorage);
    if (session.fetch()) {
      sessionRefresherComponent.registerSession(session.sessionId());
      return session;
    } else {
      throw new SessionNotFoundException("ID: " + sessionId);
    }
  }

  public Session getAttachedSession(UUID clientId) {
    return this.sessionMap.get(clientId);
  }

  public void attachSession(UUID clientId, Session session) {
    this.sessionMap.put(clientId, session);
  }

  public Session createAndAttachNewSession(UUID clientId) {
    final BaseSession session = new BaseSession(UUID.randomUUID().toString(), sessionStorage);
    session.save();
    attachSession(clientId, session);
    sessionRefresherComponent.registerSession(session.sessionId());
    return session;
  }

  public void detachSession(UUID clientId) {
    if (clientId == null || !sessionMap.containsKey(clientId)) {
      ASYNC_LOGGER.log(Level.WARN, "Did not find clientId {0} in session map", clientId);
      return;
    }

    String sessionId = sessionMap.get(clientId).sessionId();
    sessionRefresherComponent.unregisterSession(sessionId);
    Session session = sessionMap.remove(clientId);
    session.finishTasks();
  }

  public Map<UUID, SessionDto> getAllAttachedSessions() {
    return this.sessionMap.entrySet().stream()
        .collect(
            Collectors.toMap(Map.Entry::getKey, e -> ((BaseSession) e.getValue()).sessionDto()));
  }
}
