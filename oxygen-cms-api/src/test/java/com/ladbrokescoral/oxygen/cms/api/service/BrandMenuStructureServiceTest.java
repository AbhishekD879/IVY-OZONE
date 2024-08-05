package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BrandMenuStructure;
import com.ladbrokescoral.oxygen.cms.api.entity.Name;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.UserStatus;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandMenuStructureRepository;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

@RunWith(MockitoJUnitRunner.class)
public class BrandMenuStructureServiceTest extends BDDMockito {

  @Mock private UserService userService;
  @Mock private BrandMenuStructureRepository repository;

  private BrandMenuStructureService service;

  private static final String ADMIN_PATH = "/admin";

  @Before
  public void init() {
    service = new BrandMenuStructureService(repository);
  }

  @Test
  public void adminUserTest() {
    mockContext();
    when(repository.findByBrand(anyString(), any())).thenReturn(menuStructureCollection());
    when(SecurityContextHolder.getContext().getAuthentication().isAuthenticated()).thenReturn(true);
    when(SecurityContextHolder.getContext().getAuthentication().getPrincipal())
        .thenReturn(
            User.builder()
                .admin(true)
                .password("pass")
                .email("mail")
                .status(UserStatus.ACTIVE)
                .name(new Name("first", "second"))
                .brandCode("code")
                .build());

    List<BrandMenuStructure> brandMenuStructures = service.findByBrand("brand");
    Optional<BrandMenuStructure> brandMenuStructureOpt = brandMenuStructures.stream().findFirst();
    Assert.assertTrue(brandMenuStructureOpt.isPresent());
    brandMenuStructureOpt.ifPresent(
        brandMenuStructure -> {
          Assert.assertEquals(2, brandMenuStructure.getMenu().size());
          Assert.assertTrue(
              brandMenuStructure.getMenu().stream()
                  .anyMatch(menuItem -> ADMIN_PATH.equals(menuItem.getPath())));
        });
  }

  @Test
  public void notAdminTest() {
    mockContext();
    when(repository.findByBrand(anyString(), any())).thenReturn(menuStructureCollection());
    when(SecurityContextHolder.getContext().getAuthentication().isAuthenticated()).thenReturn(true);
    when(SecurityContextHolder.getContext().getAuthentication().getPrincipal())
        .thenReturn(
            User.builder()
                .admin(false)
                .password("pass")
                .email("mail")
                .status(UserStatus.ACTIVE)
                .name(new Name("first", "second"))
                .brandCode("code")
                .build());

    List<BrandMenuStructure> brandMenuStructures = service.findByBrand("brand");
    Optional<BrandMenuStructure> brandMenuStructureOpt = brandMenuStructures.stream().findFirst();
    Assert.assertTrue(brandMenuStructureOpt.isPresent());
    brandMenuStructureOpt.ifPresent(
        brandMenuStructure -> {
          Assert.assertEquals(1, brandMenuStructure.getMenu().size());
          Assert.assertFalse(
              brandMenuStructure.getMenu().stream()
                  .anyMatch(menuItem -> ADMIN_PATH.equals(menuItem.getPath())));
        });
  }

  private List<BrandMenuStructure> menuStructureCollection() {
    List<BrandMenuItemDto> menuItems = new ArrayList<>();

    menuItems.add(
        BrandMenuItemDto.builder()
            .id("id1")
            .label("label")
            .path("/menu")
            .active(true)
            .displayOrder(0)
            .build());
    menuItems.add(
        BrandMenuItemDto.builder()
            .id("id2")
            .label("label")
            .path(ADMIN_PATH)
            .active(true)
            .displayOrder(1)
            .build());

    BrandMenuStructure brandMenuStructure = new BrandMenuStructure();
    brandMenuStructure.setMenu(menuItems);
    return Collections.singletonList(brandMenuStructure);
  }

  private void mockContext() {
    SecurityContext securityContext = mock(SecurityContext.class);
    Authentication authentication = mock(Authentication.class);
    SecurityContextHolder.setContext(securityContext);

    when(securityContext.getAuthentication()).thenReturn(authentication);
  }
}
