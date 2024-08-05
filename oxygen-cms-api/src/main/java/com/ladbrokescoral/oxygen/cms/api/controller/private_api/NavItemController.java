package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.service.NavItemService;
import com.ladbrokescoral.oxygen.cms.api.service.PromoLeaderboardValidationService;
import java.util.ArrayList;
import java.util.Objects;
import java.util.Optional;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@SuppressWarnings("java:S4684")
@Slf4j
public class NavItemController extends AbstractSortableController<NavItem> {

  private final PromoLeaderboardValidationService validationService;

  NavItemController(
      NavItemService sortableService,
      PromoLeaderboardValidationService leaderboardValidationService) {
    super(sortableService);
    this.validationService = leaderboardValidationService;
  }

  @PostMapping("/nav-item")
  @Override
  public ResponseEntity<NavItem> create(@RequestBody @Valid NavItem entity) {
    log.info("NavItem Request entity while creating : {}", entity);
    validateMaxLeaderboard(entity);
    return super.create(entity);
  }

  private void validateMaxLeaderboard(NavItem entity) {
    if (validationService.isNavItemValidationRequired(
        entity.getNavType(), entity.getNavigationGroupId())) {
      validationService.validateMaxLeaderboard(
          entity.getBrand(),
          validationService.getLinkedPromotionsCount(entity.getNavigationGroupId()),
          new ArrayList<>());
    }
  }

  @PutMapping("/nav-item/{id}")
  @Override
  public NavItem update(@PathVariable String id, @RequestBody @Valid NavItem entity) {
    log.info("NavItem Request entity while updating: {}", entity);
    Optional<NavItem> maybeEntity = crudService.findOne(id);
    validateUpdateMaxLeaderboard(maybeEntity, entity);
    return super.update(id, entity);
  }

  private void validateUpdateMaxLeaderboard(Optional<NavItem> maybeEntity, NavItem updatedEntity) {
    if (validationService.isNavItemValidationRequired(
        updatedEntity.getNavType(), updatedEntity.getNavigationGroupId())) {
      maybeEntity.ifPresent(
          (NavItem existingEntity) -> {
            if (Objects.isNull(existingEntity.getLeaderboardId())
                && Objects.nonNull(updatedEntity.getLeaderboardId())) {
              validationService.validateMaxLeaderboard(
                  updatedEntity.getBrand(),
                  validationService.getLinkedPromotionsCount(updatedEntity.getNavigationGroupId()),
                  new ArrayList<>());
            }
          });
    }
  }

  @DeleteMapping("/nav-item/{id}")
  @Override
  public ResponseEntity<NavItem> delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("nav-item/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
