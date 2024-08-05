package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.AccaInsuranceMessage;
import com.ladbrokescoral.oxygen.cms.api.repository.AccaInsuranceMessageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class AccaInsuranceMessagesAfterSaveListener
    extends BasicMongoEventListener<AccaInsuranceMessage> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "acca-insurance";
  private final AccaInsuranceMessageRepository repository;

  public AccaInsuranceMessagesAfterSaveListener(
      final AccaInsuranceMessageRepository repository, final DeliveryNetworkService context) {
    super(context);
    this.repository = repository;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<AccaInsuranceMessage> event) {
    String brand = event.getSource().getBrand();
    Optional<AccaInsuranceMessage> accaInsuranceMessage = repository.findOneByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, accaInsuranceMessage);
  }
}
