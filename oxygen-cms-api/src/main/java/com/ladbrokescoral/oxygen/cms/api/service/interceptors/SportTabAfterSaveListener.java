package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportTabAfterSaveListener extends AbstractSportTabAfterSaveListener<SportTab> {

  public SportTabAfterSaveListener(
      final SportCategoryPublicService sportPublicService,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(sportPublicService, context, ladsCoralKafkaPublisher);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SportTab> event) {
    Integer sportId = event.getSource().getSportId();
    String brand = event.getSource().getBrand();
    uploadSportTabs(sportId, brand);
  }

  @Override
  public void onAfterDelete(AfterDeleteEvent<SportTab> deleteEvent) {
    Integer sportId = deleteEvent.getSource().getInteger("sportId");
    String brand = deleteEvent.getSource().getString("brand");
    delete(brand, PATH_TEMPLATE, sportId.toString());
    delete(brand, CONFIGS_PATH_TEMPLATE, sportId.toString());
  }
}
