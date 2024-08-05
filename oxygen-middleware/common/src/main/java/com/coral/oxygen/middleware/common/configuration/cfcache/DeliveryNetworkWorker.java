package com.coral.oxygen.middleware.common.configuration.cfcache;

import com.coral.oxygen.middleware.pojos.model.cache.UploadItem;
import java.util.function.BiPredicate;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@RequiredArgsConstructor
@Component
public class DeliveryNetworkWorker {
  private final BrandCacheServiceProvider brandCacheServiceProvider;

  public void deliverItem(UploadItem item) {
    if (item != null) doUploadToCache(item);
  }

  private void doUploadToCache(UploadItem item) {
    try {
      forEachCacheService(item, (s, i) -> s.uploadJSON(i.getPath(), i.getFileName(), i.getJson()));
    } catch (Exception e) {
      log.error("Failed to upload item {} of brand {}", item.getFileName(), item.getBrand(), e);
    }
  }

  private void forEachCacheService(
      UploadItem item, BiPredicate<BrandCacheService, UploadItem> updateCacheWithItem) {
    brandCacheServiceProvider
        .getCacheService(item.getBrand())
        .forEach(
            (BrandCacheService cacheService) -> {
              if (updateCacheWithItem.test(cacheService, item)) {
                cacheService.purgeCache(item.getBrand(), item.getPath(), item.getFileName());
              }
            });
  }
}
