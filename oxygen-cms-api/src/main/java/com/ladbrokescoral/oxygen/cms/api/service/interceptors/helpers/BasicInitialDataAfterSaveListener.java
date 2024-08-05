package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.BasicMongoEventListener;
import com.ladbrokescoral.oxygen.cms.util.CustomExecutors;
import java.util.Arrays;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.util.ObjectUtils;

@Slf4j
public abstract class BasicInitialDataAfterSaveListener<T extends HasBrand>
    extends BasicMongoEventListener<T> {

  private final InitialDataService service;
  // "api/{0}/initial-data".
  protected static final String PATH_TEMPLATE = "api/{0}/initial-data";
  protected static final String CF_PATH_TEMPLATE = "api/{0}/cf/initial-data";

  // FIXME: should be private. un-testable for Spock
  @Autowired protected CustomExecutors customExecutors;

  public BasicInitialDataAfterSaveListener(
      final InitialDataService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  protected void upload(AfterSaveEvent<T> event) {
    String brand = event.getSource().getBrand();
    if (ObjectUtils.isEmpty(brand)) {
      log.error("Ignore upload. Event must contains brand {} ", event);
    } else {
      customExecutors.getSingleThreadLastTaskExecutor(brand).execute(() -> doUpload(event));
    }
  }

  private void doUpload(AfterSaveEvent<T> event) {
    log.info("Preparing initial-data update to Akamai after event {}", event.getCollectionName());
    Arrays.asList("mobile", "tablet", "desktop")
        .forEach(
            deviceType -> {
              InitialDataDto content =
                  service.fetchInitialData(
                      event.getSource().getBrand(), deviceType, SegmentConstants.UNIVERSAL);
              uploadOptional(
                  event.getSource().getBrand(), PATH_TEMPLATE, deviceType, Optional.of(content));

              if ("mobile".equals(deviceType)) {
                content = service.fetchCFInitialData(event.getSource().getBrand(), deviceType);

                uploadCFContent(
                    event.getSource().getBrand(),
                    CF_PATH_TEMPLATE,
                    deviceType,
                    Optional.of(content));
              }
            });
    log.info("Sent initial-data for update to Akamai after event {}", event.getCollectionName());
  }
}
