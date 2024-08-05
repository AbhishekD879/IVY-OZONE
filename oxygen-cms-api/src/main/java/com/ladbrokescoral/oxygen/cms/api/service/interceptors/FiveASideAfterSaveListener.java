package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FiveASideFormation;
import com.ladbrokescoral.oxygen.cms.api.service.FiveASideFormationService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.ArrayList;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FiveASideAfterSaveListener extends BasicMongoEventListener<FiveASideFormation> {

  private final FiveASideFormationService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "five-a-side-formations";

  public FiveASideAfterSaveListener(
      FiveASideFormationService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FiveASideFormation> event) {
    String brand = event.getSource().getBrand();
    List<FiveASideFormation> formations = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, new ArrayList(formations));
  }
}
