package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsSorting;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class InplayStatsSortingAfterSaveListener
    extends BasicInitialDataAfterSaveListener<InplayStatsSorting> {
  public InplayStatsSortingAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<InplayStatsSorting> event) {
    log.info(
        "InplayStatsSortingAfterSaveListener::on AfterSave Event for the collection::{}",
        event.getCollectionName());
    super.upload(event);
  }
}
