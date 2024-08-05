package com.ladbrokescoral.aggregation.repository.impl;

import com.ladbrokescoral.aggregation.repository.AbstractCacheImageRepository;
import java.time.Duration;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class CachePathRepository extends AbstractCacheImageRepository<String, byte[]> {

  @Autowired
  public CachePathRepository(
      ReactiveRedisTemplate<String, byte[]> reactiveRedisTemplate,
      @Value("${general.path.cache.ttl}") Duration cacheTtl) {
    super(reactiveRedisTemplate, cacheTtl);
  }

  @Override
  protected String getKeyPrefix() {
    return "PATH_";
  }
}
