package com.ladbrokescoral.oxygen.cms.api.service.impl;

public interface CachePurgeService {

  void purgeCache(String brand, String path, String fileName);

  default void purgeCache(String brand, String path, String fileName, String cacheTag) {
    purgeCache(brand, path, fileName);
  }

  String getRootUrl();

  void shutdown();
}
