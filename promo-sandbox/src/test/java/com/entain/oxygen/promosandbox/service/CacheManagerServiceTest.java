package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
class CacheManagerServiceTest {

  @Mock private CacheManager cacheManager;

  @InjectMocks private CacheManagerService cacheManagerService;

  @Test
  void clearCacheTest() {
    List<String> cachesName = new ArrayList<>();
    cachesName.add("topXCache");
    Mockito.when(cacheManager.getCacheNames()).thenReturn(cachesName);
    assertNotNull(cacheManager);
    Cache cache = Mockito.mock(Cache.class);
    Mockito.when(cacheManager.getCache(Mockito.anyString())).thenReturn(cache);
    cacheManagerService.clearCache();
  }
}
