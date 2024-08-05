package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ArcProfilePublicService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.DependsOn;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@DependsOn("arcProfilePublicService")
public class ArcProfileSaveListener extends BasicMongoEventListener<ArcProfile> {
  private static final String PATH_TEMPLATE_PREFIX = "api/{0}/arc-profile/";
  private final ArcProfilePublicService service;

  protected ArcProfileSaveListener(
      final DeliveryNetworkService context, final ArcProfilePublicService service) {
    super(context);
    this.service = service;
  }

  /** Method that captures After save event and upload that collection to s3 bucket. */
  @Override
  public void onAfterSave(AfterSaveEvent<ArcProfile> event) {
    String brand = event.getSource().getBrand();
    Integer modelRiskLevel = event.getSource().getModelRiskLevel();
    Integer reasonCode = event.getSource().getReasonCode();
    StringBuilder pathTemplateSB = new StringBuilder(PATH_TEMPLATE_PREFIX);
    String pathTemplate = pathTemplateSB.append(modelRiskLevel).toString();
    String fileName = reasonCode.toString();
    ArcProfileDto arcProfile =
        service.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            brand, modelRiskLevel, reasonCode);
    log.info("ArcProfileSaveListener :: saved file path :" + brand + pathTemplate + fileName);
    uploadOptional(brand, pathTemplate, fileName, Optional.of(arcProfile));
  }

  @Override
  public void onAfterDelete(AfterDeleteEvent<ArcProfile> deleteEvent) {
    String brand = deleteEvent.getSource().getString("brand");
    Integer modelRiskLevel = deleteEvent.getSource().getInteger("modelRiskLevel");
    Integer reasonCode = deleteEvent.getSource().getInteger("reasonCode");
    StringBuilder pathTemplateSB = new StringBuilder(PATH_TEMPLATE_PREFIX);
    String pathTemplate = pathTemplateSB.append(modelRiskLevel).toString();
    String fileName = reasonCode.toString();
    log.info("ArcProfileSaveListener :: deleted file path :" + brand + pathTemplate + fileName);
    delete(brand, pathTemplate, fileName);
  }
}
