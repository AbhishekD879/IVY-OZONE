package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class LuckyDipMappingAfterSaveListener extends BasicMongoEventListener<LuckyDipMapping> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "lucky-dip-mapping";
  private final LuckyDipMappingPublicService service;

  public LuckyDipMappingAfterSaveListener(
      final LuckyDipMappingPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<LuckyDipMapping> event) {
    String brand = event.getSource().getBrand();
    List<LuckyDipMappingPublicDto> activeLuckyDipMappingsByBrand =
        service.findAllActiveLuckyDipMappingsByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, activeLuckyDipMappingsByBrand);
  }
}
