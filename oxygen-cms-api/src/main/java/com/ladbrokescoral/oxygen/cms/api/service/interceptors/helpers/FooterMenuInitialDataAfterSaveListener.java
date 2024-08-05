package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.util.CustomEvent;
import lombok.extern.slf4j.Slf4j;
import org.bson.Document;
import org.springframework.context.event.EventListener;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class FooterMenuInitialDataAfterSaveListener
    extends BasicInitialDataAfterSaveListener<FooterMenu> {
  private static final String COLLECTION_NAME = "footermenus";

  public FooterMenuInitialDataAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FooterMenu> event) {
    if (COLLECTION_NAME.equals(event.getCollectionName())) {
      upload(event);
    }
  }

  @EventListener
  public void listen(CustomEvent<FooterMenu> event) {
    log.info("received event++++++++++==");
    FooterMenu entity = (FooterMenu) event.getSource();
    entity.setBrand(event.getBrand());
    onAfterSave(new AfterSaveEvent<>(entity, new Document(), event.getCollectionName()));
  }
}
