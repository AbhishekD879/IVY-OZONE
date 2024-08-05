package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.NetworkIndicatorConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.NetworkIndicatorRepository;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class NetworkIndicatorAfterSaveListener
    extends BasicMongoEventListener<NetworkIndicatorConfig> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "network-indicator";

  private NetworkIndicatorRepository networkIndicatorRepository;

  protected NetworkIndicatorAfterSaveListener(
      DeliveryNetworkService context, NetworkIndicatorRepository networkIndicatorRepository) {
    super(context);
    this.networkIndicatorRepository = networkIndicatorRepository;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<NetworkIndicatorConfig> event) {
    String brand = event.getSource().getBrand();
    Optional<NetworkIndicatorConfig> networkIndicatorConfig =
        networkIndicatorRepository.findOneByBrand(brand);
    log.info("networkIndicatorConfig:{}", networkIndicatorConfig);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, networkIndicatorConfig);
  }
}
