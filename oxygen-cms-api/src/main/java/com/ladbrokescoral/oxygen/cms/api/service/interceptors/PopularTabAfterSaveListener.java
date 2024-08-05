package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.PopularTab;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class PopularTabAfterSaveListener extends AbstractSportTabAfterSaveListener<PopularTab> {

  public PopularTabAfterSaveListener(
      final SportCategoryPublicService sportPublicService,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(sportPublicService, context, ladsCoralKafkaPublisher);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<PopularTab> event) {
    Integer sportId = event.getSource().getSportId();
    String brand = event.getSource().getBrand();
    uploadSportTabs(sportId, brand);
  }
}
