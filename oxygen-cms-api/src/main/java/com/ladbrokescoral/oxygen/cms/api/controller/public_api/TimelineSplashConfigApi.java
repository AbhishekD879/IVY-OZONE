package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TimelineSplashConfigDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.TimelineConfigPublicService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class TimelineSplashConfigApi implements Public {
  private final TimelineConfigPublicService timelineSplashConfigService;

  @GetMapping("{brand}/timeline-splash-config")
  public ResponseEntity<TimelineSplashConfigDto> findTimelineSplashConfigByBrand(
      @PathVariable String brand) {
    return timelineSplashConfigService
        .findSplashConfigByBrand(brand)
        .map(ResponseEntity::ok)
        .orElse(new ResponseEntity<>(HttpStatus.NO_CONTENT));
  }
}
