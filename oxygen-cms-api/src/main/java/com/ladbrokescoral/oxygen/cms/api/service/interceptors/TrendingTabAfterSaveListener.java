package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class TrendingTabAfterSaveListener extends AbstractSportTabAfterSaveListener<TrendingTab> {

  public TrendingTabAfterSaveListener(
      final SportCategoryPublicService sportPublicService,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(sportPublicService, context, ladsCoralKafkaPublisher);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<TrendingTab> event) {
    Integer sportId = event.getSource().getSportId();
    String brand = event.getSource().getBrand();
    uploadSportTabs(sportId, brand);
  }
}
