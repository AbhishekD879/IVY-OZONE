package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
public class InMemorySessionStorage implements SessionStorage<SessionDto> {

  private final Map<String, SessionDto> map;

  public InMemorySessionStorage() {
    map = new HashMap<>();
  }

  @Override
  public boolean refreshTtl(String sessionId) {
    return true;
  }

  @Override
  public Optional<SessionDto> find(String sessionId) {
    return Optional.ofNullable(map.get(sessionId));
  }

  @Override
  public List<SessionDto> findAll() {
    return new ArrayList<>(map.values());
  }

  @Override
  public void persist(SessionDto session) {
    map.put(session.getSessionId(), session);
  }
}
