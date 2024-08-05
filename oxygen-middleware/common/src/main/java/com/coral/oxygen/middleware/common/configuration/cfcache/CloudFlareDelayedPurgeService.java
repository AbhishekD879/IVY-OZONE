package com.coral.oxygen.middleware.common.configuration.cfcache;

import static java.util.stream.Collectors.toSet;

import java.util.List;
import java.util.Optional;
import java.util.Set;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class CloudFlareDelayedPurgeService extends AbstractDelayedPurgeService {

  private final CloudFlareClient cloudFlareClient;
  private final String cloudFlareZoneId;
  private final String[] purgeUrls;

  public CloudFlareDelayedPurgeService(
      CloudFlareClient cloudFlareClient,
      Integer queueCapacity,
      Integer initialDelay,
      Integer fixedDelay,
      Integer purgeItemsMaxLimit,
      String cloudFlareZoneId,
      String[] purgeUrls) {
    super(queueCapacity, initialDelay, fixedDelay, purgeItemsMaxLimit);
    this.cloudFlareClient = cloudFlareClient;
    this.cloudFlareZoneId = cloudFlareZoneId;
    this.purgeUrls = purgeUrls;
  }

  @Override
  public void purgeCache(String brand, String path, String fileName) {
    for (String uri : purgeUrls) {
      delayPurge(
          CCUItem.builder()
              .brand(brand)
              .path(PathUtil.concatUri(uri, path, fileName))
              .name(fileName)
              .build());
    }
  }

  @Override
  public String getRootUrl() {
    return purgeUrls.length > 0 ? purgeUrls[0] : null;
  }

  @Override
  protected List<Optional<InvalidateCacheResult>> doPurgeItems(List<CCUItem> purgeItems) {
    Set<String> purgePaths = purgeItems.stream().map(CCUItem::getPath).collect(toSet());
    Optional<InvalidateCacheResult> purgePathsResult =
        cloudFlareClient.invalidate(cloudFlareZoneId, purgePaths);
    return List.of(purgePathsResult, Optional.empty());
  }
}
