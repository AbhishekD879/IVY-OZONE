package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineConfigService;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TimelineConfigController extends AbstractCrudController<Config> {
  private final TimelineConfigService timelineConfigService;

  TimelineConfigController(TimelineConfigService timelineConfigService) {
    super(timelineConfigService);
    this.timelineConfigService = timelineConfigService;
  }

  @Override
  @PostMapping("/timeline/system-config")
  public ResponseEntity<Config> create(@RequestBody @Valid Config entity) {
    return super.create(populateCreatorAndUpdater(entity.prepareModelBeforeSave()));
  }

  @Override
  @PutMapping("/timeline/system-config/{id}")
  public Config update(@PathVariable String id, @RequestBody @Valid Config entity) {
    return super.update(id, populateCreatorAndUpdater(entity.prepareModelBeforeUpdate()));
  }

  @GetMapping("/timeline/system-config/brand/{brand}")
  public Config readOneByBrand(@PathVariable String brand) {
    Config settings = timelineConfigService.findOneByBrand(brand);

    return populateCreatorAndUpdater(settings);
  }
}
