package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.DeviceType.MOBILE;

import com.ladbrokescoral.oxygen.cms.api.aop.LogExecutionTime;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.SegmentNamePattern;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Validated
public class InitialDataApi implements Public {
  private final InitialDataService service;

  public InitialDataApi(InitialDataService service) {
    this.service = service;
  }

  @Cacheable("initial-data")
  @LogExecutionTime
  @GetMapping("{brand}/initial-data/{deviceType}")
  public InitialDataDto getInitialData(
      @PathVariable String brand, @PathVariable String deviceType) {
    return service.fetchInitialData(brand, deviceType, SegmentConstants.UNIVERSAL);
  }

  @Cacheable(
      value = "initial-data",
      key = "{ #root.methodName, #brand, #segmentName}",
      unless = "#result == null")
  @LogExecutionTime
  @GetMapping("{brand}/initial-data/segment/{segmentName}/mobile")
  public InitialDataDto getSegmentedInitialData(
      @PathVariable("brand") @Brand String brand,
      @Validated @SegmentNamePattern @PathVariable("segmentName") String segmentName) {
    return service.fetchInitialData(brand, MOBILE.getValue(), segmentName);
  }
}
