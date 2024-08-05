package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationGroupService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@SuppressWarnings("java:S4684")
public class NavigationGroupController extends AbstractCrudController<NavigationGroup> {

  private final NavigationGroupService navigationGroupService;

  NavigationGroupController(NavigationGroupService navigationGroupService) {
    super(navigationGroupService);
    this.navigationGroupService = navigationGroupService;
  }

  @PostMapping("/navigation-group")
  @Override
  public ResponseEntity<NavigationGroup> create(@RequestBody @Valid NavigationGroup entity) {
    return super.create(entity);
  }

  @PutMapping("/navigation-group/{id}")
  @Override
  public NavigationGroup update(
      @PathVariable String id, @RequestBody @Valid NavigationGroup entity) {
    return super.update(id, entity);
  }

  @GetMapping("/navigation-group/brand/{brand}")
  public List<NavigationGroupDto> findAllNavigationGroup(@PathVariable String brand) {
    return navigationGroupService.findAllNavigationGroup(brand);
  }

  // This API is used in Promotion Page
  @GetMapping("/navigation-group/active/brand/{brand}")
  public List<NavigationGroupDto> findAllActiveNavigationGroup(@PathVariable String brand) {
    return navigationGroupService.findAllActiveNavigationGroup(brand);
  }

  @DeleteMapping("/navigation-group/{id}/{promotionIds}")
  public ResponseEntity<NavigationGroup> deleteByNavigationGroupId(
      @PathVariable String id, @PathVariable String promotionIds) {
    navigationGroupService.deleteNavItemsByNavGId(promotionIds, id);
    return super.delete(id);
  }

  @GetMapping("nav-item/navigation-groupId/{id}")
  public Optional<NavigationGroupDto> readAll(@PathVariable String id) {
    NavigationGroup navigationGroup = super.read(id);
    return navigationGroupService.findNavigationGroup(id, Optional.ofNullable(navigationGroup));
  }
}
