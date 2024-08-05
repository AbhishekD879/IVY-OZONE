package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BrandMenuStructure;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandMenuStructureRepository;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class BrandMenuStructureService extends SortableService<BrandMenuStructure> {
  private final BrandMenuStructureRepository structureRepository;

  private static final List<String> ONLY_ADMIN_USER_MENUS = Collections.singletonList("/admin");

  @Autowired
  public BrandMenuStructureService(BrandMenuStructureRepository structureRepository) {
    super(structureRepository);
    this.structureRepository = structureRepository;
  }

  @Override
  public List<BrandMenuStructure> findByBrand(String brand) {

    List<BrandMenuStructure> menuStructures =
        structureRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);

    filterMenuItems(menuStructures);

    return menuStructures;
  }

  private void filterMenuItems(List<BrandMenuStructure> menuStructures) {

    Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
        .filter(Authentication::isAuthenticated)
        .map(Authentication::getPrincipal)
        .map(User.class::cast)
        .filter(user -> !user.isAdmin())
        .ifPresent(
            user ->
                menuStructures.stream()
                    .findFirst()
                    .ifPresent(
                        brandMenuStructure ->
                            brandMenuStructure
                                .getMenu()
                                .removeIf(
                                    menuItem ->
                                        ONLY_ADMIN_USER_MENUS.contains(menuItem.getPath()))));
  }
}
