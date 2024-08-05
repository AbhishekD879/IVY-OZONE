package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.CCUItem;
import com.ladbrokescoral.oxygen.cms.api.service.DashboardService;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class AkamaiDelayedPurgeService extends AbstractDelayedPurgeService {

  private final AkamaiPurgeClient akamaiPurgeClient;
  private final String[] purgeUrls;

  public AkamaiDelayedPurgeService(
      DashboardService service,
      AkamaiPurgeClient akamaiPurgeClient,
      Integer queueCapacity,
      Integer initialDelay,
      Integer fixedDelay,
      String[] purgeUrls) {
    super(service, queueCapacity, initialDelay, fixedDelay);
    this.akamaiPurgeClient = akamaiPurgeClient;
    this.purgeUrls = purgeUrls;
  }

  @Override
  public void purgeCache(String brand, String path, String fileName) {
    purgeAll(brand, purgeUrls, path, fileName);
  }

  @Override
  public String getRootUrl() {
    return purgeUrls.length > 0 ? purgeUrls[0] : null;
  }

  @Override
  protected List<Optional<InvalidateCacheResult>> doPurgeItems(List<CCUItem> purgeItems) {
    log.trace("Invalidating {} items", purgeItems.size());
    return akamaiPurgeClient.invalidateAll();
  }

  private void purgeAll(
      String brand, String[] akamaiUrls, String relatedDirectory, String fileName) {
    for (String uri : akamaiUrls) {
      delayPurge(
          CCUItem.builder()
              .brand(brand)
              .path(PathUtil.concatUri(uri, relatedDirectory, fileName))
              .name(fileName)
              .build());
    }
  }
}
