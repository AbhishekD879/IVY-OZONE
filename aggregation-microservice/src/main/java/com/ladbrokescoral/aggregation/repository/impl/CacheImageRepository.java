package com.ladbrokescoral.aggregation.repository.impl;

import com.ladbrokescoral.aggregation.repository.AbstractCacheImageRepository;
import java.time.Duration;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class CacheImageRepository extends AbstractCacheImageRepository<String, byte[]> {

  @Autowired
  public CacheImageRepository(
      ReactiveRedisTemplate<String, byte[]> reactiveRedisImageTemplate,
      @Value("${general.image.cache.ttl}") Duration cacheTtl) {
    super(reactiveRedisImageTemplate, cacheTtl);
  }

  @Override
  protected String getKeyPrefix() {
    return "SILK_";
  }
}
