package com.coral.oxygen.middleware.common.configuration.cfcache;

public interface BrandCacheService extends CachePurgeService {

  boolean uploadJSON(String relativePath, String fileName, String json);
}
