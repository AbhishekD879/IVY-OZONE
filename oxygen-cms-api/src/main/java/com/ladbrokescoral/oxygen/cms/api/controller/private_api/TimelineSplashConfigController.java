package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineSplashConfigService;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TimelineSplashConfigController extends AbstractCrudController<TimelineSplashConfig> {
  private final TimelineSplashConfigService timelineSplashConfigService;

  TimelineSplashConfigController(TimelineSplashConfigService timelineSplashConfigService) {
    super(timelineSplashConfigService);
    this.timelineSplashConfigService = timelineSplashConfigService;
  }

  @Override
  @PostMapping("/timeline/splash-config")
  public ResponseEntity<TimelineSplashConfig> create(
      @RequestBody @Valid TimelineSplashConfig entity) {
    return super.create(populateCreatorAndUpdater(entity.prepareModelBeforeSave()));
  }

  @Override
  @PutMapping("/timeline/splash-config/{id}")
  public TimelineSplashConfig update(
      @PathVariable String id, @RequestBody @Valid TimelineSplashConfig entity) {
    return super.update(id, populateCreatorAndUpdater(entity.prepareModelBeforeUpdate()));
  }

  @GetMapping("/timeline/splash-config/brand/{brand}")
  public TimelineSplashConfig readOneByBrand(@PathVariable String brand) {
    TimelineSplashConfig settings = timelineSplashConfigService.findOneByBrand(brand);

    return populateCreatorAndUpdater(settings);
  }
}
