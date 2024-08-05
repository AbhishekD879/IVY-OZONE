package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineCampaignService;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.PositiveOrZero;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TimelineCampaignController extends AbstractCrudController<Campaign> {
  private final TimelineCampaignService service;

  TimelineCampaignController(TimelineCampaignService service) {
    super(service);
    this.service = service;
  }

  @GetMapping({"/timeline/campaign", "/timeline/campaign/{pageNumber}/{pageSize}"})
  public List<Campaign> getAll(
      @PathVariable(value = "pageNumber", required = false) @PositiveOrZero Integer pageNumber,
      @PathVariable(value = "pageSize", required = false) @PositiveOrZero Integer pageSize,
      Sort sort) {
    return service.findOrdered(sort);
  }

  // E.G. /campaign/brand/bma/1/10?sort=name,asc
  @GetMapping({
    "/timeline/campaign/brand/{brand}",
    "/timeline/campaign/brand/{brand}/{pageNumber}/{pageSize}", // by default sorted by updatedAt
  })
  public List<Campaign> getByBrand(
      @PathVariable("brand") String brand,
      @PathVariable(value = "pageNumber", required = false) @PositiveOrZero Integer pageNumber,
      @PathVariable(value = "pageSize", required = false) @PositiveOrZero Integer pageSize,
      Sort sort) {
    return service.findByBrandOrdered(brand, sort);
  }

  @PostMapping("/timeline/campaign")
  public Campaign save(@RequestBody @Valid Campaign entity) {
    return service.save(populateCreatorAndUpdater(entity.prepareModelBeforeSave()));
  }

  @Override
  @PutMapping("/timeline/campaign/{id}")
  public Campaign update(@PathVariable("id") String id, @RequestBody @Valid Campaign updateEntity) {
    return super.update(id, populateCreatorAndUpdater(updateEntity.prepareModelBeforeUpdate()));
  }

  @GetMapping("/timeline/campaign/{id}")
  public Campaign getCampaignById(@PathVariable("id") String id) {
    return this.service.findOne(id).orElse(null);
  }

  @Override
  @DeleteMapping("/timeline/campaign/{id}") // we also need to remove all posts of this campaign
  public ResponseEntity delete(@PathVariable("id") String id) {
    return super.delete(id);
  }
}
