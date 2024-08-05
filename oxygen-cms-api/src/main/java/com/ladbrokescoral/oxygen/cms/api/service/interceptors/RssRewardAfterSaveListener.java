package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import com.ladbrokescoral.oxygen.cms.api.service.RssRewardService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class RssRewardAfterSaveListener extends BasicMongoEventListener<RssReward> {
  private final RssRewardService service;
  private static final String RSS_REWARD = "rss-reward";
  private static final String PATH_TEMPLATE = "api/{0}/rss-reward";

  public RssRewardAfterSaveListener(
      final RssRewardService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<RssReward> event) {
    String brand = event.getSource().getBrand();
    RssReward rssReward = service.getRssReward(brand);
    log.info("RssRewardAfterSaveListener rss entity uploaded {}", rssReward);
    uploadCollection(
        brand, PATH_TEMPLATE, RSS_REWARD, Stream.of(rssReward).collect(Collectors.toList()));
  }
}
