package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostMessage;
import com.ladbrokescoral.oxygen.cms.api.repository.OddsBoostMessageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class OddsBoostMessagesAfterSaveListener extends BasicMongoEventListener<OddsBoostMessage> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "odds-boost";
  private final OddsBoostMessageRepository repository;

  public OddsBoostMessagesAfterSaveListener(
      final OddsBoostMessageRepository repository, final DeliveryNetworkService context) {
    super(context);
    this.repository = repository;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<OddsBoostMessage> event) {
    String brand = event.getSource().getBrand();
    Optional<OddsBoostMessage> oddsBoostMessage = repository.findOneByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, oddsBoostMessage);
  }
}
