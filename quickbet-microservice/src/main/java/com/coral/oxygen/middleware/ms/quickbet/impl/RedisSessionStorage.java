package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

/**
 * @author volodymyr.masliy
 */
@Component
@Profile("!UNIT")
public final class RedisSessionStorage implements SessionStorage<SessionDto> {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private long sessionTtl;

  private RedisTemplate<String, SessionDto> redisTemplate;

  @Autowired
  public RedisSessionStorage(
      RedisTemplate<String, SessionDto> redisTemplate,
      @Value("${session.ttl.minutes}") long sessionTtl) {
    this.redisTemplate = redisTemplate;
    this.sessionTtl = sessionTtl;
  }

  /**
   * Returns true if session's expiration time was successfully refreshed. Otherwise, returns false
   * (already expired or never existed)
   *
   * @param sessionId - session id
   */
  @Override
  public boolean refreshTtl(String sessionId) {
    ASYNC_LOGGER.debug("Refreshing {}", sessionId);
    Boolean refreshTtl =
        redisTemplate.boundValueOps(sessionId).expire(sessionTtl, TimeUnit.MINUTES);
    return refreshTtl != null ? refreshTtl : Boolean.FALSE;
  }

  @Override
  public Optional<SessionDto> find(String sessionId) {
    return Optional.ofNullable(redisTemplate.boundValueOps(sessionId).get());
  }

  @Override
  public List<SessionDto> findAll() {
    Set<String> keys = redisTemplate.keys("*");
    Set<String> keysData = CollectionUtils.isEmpty(keys) ? Collections.emptySet() : keys;
    return keysData.stream().map(key -> redisTemplate.boundValueOps(key).get()).toList();
  }

  @Override
  public void persist(SessionDto session) {
    String sessionId = session.getSessionId();
    ASYNC_LOGGER.info("Persisting {}:{}", sessionId, session);
    redisTemplate.boundValueOps(sessionId).set(session, sessionTtl, TimeUnit.MINUTES);
  }
}
