package com.coral.oxygen.middleware.common.configuration.cfcache;

public interface CachePurgeService {

  void purgeCache(String brand, String path, String fileName);

  String getRootUrl();

  void shutdown();
}
