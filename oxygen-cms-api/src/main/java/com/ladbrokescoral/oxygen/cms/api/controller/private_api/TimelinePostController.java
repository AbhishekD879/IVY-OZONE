package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelinePostService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.Optional;
import javax.validation.constraints.PositiveOrZero;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("v1/api/timeline/post")
public class TimelinePostController extends AbstractCrudController<TimelinePost> {
  private final TimelinePostService service;

  private CrudService<User> userService;

  public TimelinePostController(TimelinePostService crudService, CrudService<User> userService) {
    super(crudService);
    this.service = crudService;
    this.userService = userService;
  }

  @PostMapping
  public ResponseEntity<TimelinePost> save(@RequestBody TimelinePost entity) {
    return super.create(populateCreatorAndUpdater(entity.prepareModelBeforeSave()));
  }

  @GetMapping("/{id}")
  public TimelinePost getPostById(@PathVariable("id") String id) {
    return this.populateCreatorAndUpdater(super.read(id));
  }

  @Override
  @PutMapping("/{id}")
  public TimelinePost update(
      @PathVariable("id") String id, @RequestBody TimelinePost updateEntity) {
    return super.update(id, populateCreatorAndUpdater(updateEntity.prepareModelBeforeUpdate()));
  }

  @Override
  @DeleteMapping("/{id}")
  public ResponseEntity<TimelinePost> delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @GetMapping({
    "/brand/{brand}/{campaignId}",
    "/brand/{brand}/{campaignId}/{pageNumber}/{pageSize}",
  })
  public List<TimelinePost> getByBrand(
      @PathVariable("brand") String brand,
      @PathVariable("campaignId") String campaignID,
      @PathVariable(value = "pageNumber", required = false) @PositiveOrZero Integer pageNumber,
      @PathVariable(value = "pageSize", required = false) @PositiveOrZero Integer pageSize,
      Sort sort) {
    List<TimelinePost> posts;
    if (pageNumber != null && pageSize != null) {
      Pageable pageable = PageRequest.of(pageNumber, pageSize, sort);
      posts = service.findPageByBrandAndCampaignId(brand, campaignID, pageable);
    } else {
      posts = service.findByBrandAndCampaignId(brand, campaignID, sort);
    }
    posts.forEach(this::populateCreatorAndUpdater);

    return posts;
  }

  @GetMapping({"/brand/{brand}/{campaignId}/count"})
  public int getCountByBrand(
      @PathVariable("brand") String brand, @PathVariable("campaignId") String campaignID) {
    return service.getCountByBrandAndCampaignId(brand, campaignID);
  }

  @PutMapping("republish/{campaignId}")
  public void republish(@PathVariable("campaignId") String campaignId) {
    service.republishByCampaignId(campaignId);
  }

  TimelinePost populateCreatorAndUpdater(TimelinePost entity) {
    Optional.ofNullable(entity.getCreatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userService::findOne)
        .ifPresent(user -> entity.setCreatedByUserName(user.getEmail()));

    Optional.ofNullable(entity.getUpdatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userService::findOne)
        .ifPresent(user -> entity.setUpdatedByUserName(user.getEmail()));

    if (entity.getTemplate() != null) {
      Optional.ofNullable(entity.getTemplate().getCreatedBy())
          .filter(Util::isValidObjectIdString)
          .flatMap(userService::findOne)
          .ifPresent(user -> entity.getTemplate().setCreatedByUserName(user.getEmail()));

      Optional.ofNullable(entity.getTemplate().getUpdatedBy())
          .filter(Util::isValidObjectIdString)
          .flatMap(userService::findOne)
          .ifPresent(user -> entity.getTemplate().setUpdatedByUserName(user.getEmail()));
    }

    return entity;
  }
}
