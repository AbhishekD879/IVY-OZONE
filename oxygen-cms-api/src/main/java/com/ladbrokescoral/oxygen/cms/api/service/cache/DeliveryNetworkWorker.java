package com.ladbrokescoral.oxygen.cms.api.service.cache;

import static com.ladbrokescoral.oxygen.cms.api.entity.UploadItem.Action.DELETE;
import static com.ladbrokescoral.oxygen.cms.util.PathUtil.concatPath;

import com.ladbrokescoral.oxygen.cms.api.entity.UploadItem;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheServiceProvider;
import java.util.Objects;
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
    if (Objects.nonNull(item)) {
      if (DELETE == item.getAction()) {
        doDeleteFromCache(item);
      } else {
        doUploadToCache(item);
      }
    }
  }

  private void doUploadToCache(UploadItem item) {
    try {
      forEachCacheService(item, (s, i) -> s.uploadJSON(i.getPath(), i.getFileName(), i.getJson()));
    } catch (Exception e) {
      log.error("Failed to upload item {} of brand {}", item.getFileName(), item.getBrand(), e);
    }
  }

  private void doDeleteFromCache(UploadItem item) {
    try {
      forEachCacheService(item, (s, i) -> s.deleteFile(concatPath(i.getPath(), i.getFileName())));
    } catch (Exception e) {
      log.error("Failed to delete item {} of brand {}", item.getFileName(), item.getBrand(), e);
    }
  }

  private void forEachCacheService(
      UploadItem item, BiPredicate<BrandCacheService, UploadItem> updateCacheWithItem) {
    brandCacheServiceProvider
        .getCacheService(item.getBrand())
        .forEach(
            (BrandCacheService cacheService) -> {
              if (updateCacheWithItem.test(cacheService, item)) {
                cacheService.purgeCache(
                    item.getBrand(), item.getPath(), item.getFileName(), item.getCacheTag());
              }
            });
  }
}
