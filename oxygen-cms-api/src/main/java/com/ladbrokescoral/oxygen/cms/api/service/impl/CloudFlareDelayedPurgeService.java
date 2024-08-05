package com.ladbrokescoral.oxygen.cms.api.service.impl;

import static java.util.stream.Collectors.toSet;

import com.ladbrokescoral.oxygen.cms.api.entity.CCUItem;
import com.ladbrokescoral.oxygen.cms.api.service.DashboardService;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class CloudFlareDelayedPurgeService extends AbstractDelayedPurgeService {

  private final CloudFlareClient cloudFlareClient;
  private final String cloudFlareZoneId;
  private final String[] purgeUrls;

  public CloudFlareDelayedPurgeService(
      DashboardService service,
      CloudFlareClient cloudFlareClient,
      Integer queueCapacity,
      Integer initialDelay,
      Integer fixedDelay,
      String cloudFlareZoneId,
      String[] purgeUrls) {
    super(service, queueCapacity, initialDelay, fixedDelay);
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
  public void purgeCache(String brand, String path, String fileName, String cacheTag) {
    for (String uri : purgeUrls) {
      delayPurge(
          CCUItem.builder()
              .brand(brand)
              .path(PathUtil.concatUri(uri, path, fileName))
              .name(fileName)
              .cacheTag(cacheTag)
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
    Set<String> purgeTags =
        purgeItems.stream()
            .filter(ccuItem -> ccuItem.getCacheTag() != null)
            .map(CCUItem::getCacheTag)
            .collect(toSet());
    Optional<InvalidateCacheResult> purgePathsResult =
        cloudFlareClient.invalidate(cloudFlareZoneId, purgePaths);
    Optional<InvalidateCacheResult> purgeTagsResult =
        purgeTags.isEmpty()
            ? Optional.empty()
            : cloudFlareClient.invalidateCacheTags(cloudFlareZoneId, purgeTags);

    return Stream.of(purgePathsResult, purgeTagsResult).collect(Collectors.toList());
  }
}
