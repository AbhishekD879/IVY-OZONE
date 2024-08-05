package com.coral.oxygen.middleware.common.configuration.cfcache;

import java.util.List;

public interface BrandCacheServiceProvider {

  List<BrandCacheService> getCacheService(String brand);
}
