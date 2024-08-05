package com.coral.oxygen.cms.api.impl;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.google.common.cache.CacheBuilder;
import com.google.common.cache.CacheLoader;
import com.google.common.cache.LoadingCache;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

/** Created by azayats on 09.11.17. */
public class CachedSystemConfigProvider implements SystemConfigProvider {

  private static final String SYSTEM_CONFIG_KEY = "SYSTEM_CONFIG_KEY";

  private final CmsService cmsService;

  private final LoadingCache<String, CmsSystemConfig> cache;

  public CachedSystemConfigProvider(CmsService cmsService, long cacheTimeSec) {
    this.cmsService = cmsService;
    this.cache =
        CacheBuilder.newBuilder()
            .expireAfterWrite(cacheTimeSec, TimeUnit.SECONDS)
            .build(
                new CacheLoader<String, CmsSystemConfig>() {
                  @Override
                  public CmsSystemConfig load(String key) throws Exception {
                    return cmsService.requestSystemConfig();
                  }
                });
  }

  @Override
  public CmsSystemConfig systemConfig() {
    try {
      return cache.get(SYSTEM_CONFIG_KEY);
    } catch (ExecutionException e) {
      return cmsService.requestSystemConfig();
    }
  }
}
