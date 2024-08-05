package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsDisplay;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class InplayStatsDisplayAfterSaveListener
    extends BasicInitialDataAfterSaveListener<InplayStatsDisplay> {

  public InplayStatsDisplayAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<InplayStatsDisplay> event) {
    log.info(
        "InplayStatsDisplayAfterSaveListener::on AfterSave Event for the collection::{}",
        event.getCollectionName());
    super.upload(event);
  }
}
