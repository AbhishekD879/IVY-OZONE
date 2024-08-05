package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.UserMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.UserMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.UserMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.UserMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.Collections;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class UserMenuPublicServiceTest {

  @Mock private UserMenuRepository repository;

  private UserMenuPublicService service;

  private String defaultTargetUri = "my-account";
  private String defaultUriMedium = "/images/uploads/right_menu/default/default-156x156.png";
  private String defaultUriSmall = "/images/uploads/right_menu/default/default-104x104.png";

  @Before
  public void init() {
    UserMenuService menuService =
        new UserMenuService(
            repository,
            null,
            null,
            ImagePath.builder()
                .smallSize(new ImageServiceImpl.Size("10x10"))
                .mediumSize(new ImageServiceImpl.Size("20x20"))
                .largeSize(new ImageServiceImpl.Size("30x30"))
                .build());
    service = new UserMenuPublicService(menuService);
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    String brand = "bma";

    UserMenu entity = new UserMenu();

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<UserMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    UserMenuDto dto = list.get(0);
    assertNull(dto.getSvg());
    assertNull(dto.getSvgId());
    assertEquals(defaultTargetUri, dto.getTargetUri());
    assertEquals(StringUtils.EMPTY, dto.getLinkTitle());
    assertEquals(defaultUriMedium, dto.getUriMedium());
    assertEquals(defaultUriSmall, dto.getUriSmall());
    assertNull(dto.getActiveIfLogout());
    assertNull(dto.getQa());
    assertNull(dto.getDisabled());
    assertNull(dto.getShowUserMenu());
  }

  @Test
  public void testFindByBrandEmptyEntity() {
    // arrange
    String brand = "rcomb";

    UserMenu entity = new UserMenu();
    entity.setSvg(StringUtils.EMPTY);
    entity.setSvgId(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setUriMedium(StringUtils.EMPTY);
    entity.setUriSmall(StringUtils.EMPTY);
    entity.setActiveIfLogout(Boolean.FALSE);
    entity.setQa(StringUtils.EMPTY);
    entity.setDisabled(Boolean.FALSE);
    entity.setShowUserMenu(StringUtils.EMPTY);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<UserMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    UserMenuDto dto = list.get(0);
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertEquals(defaultTargetUri, dto.getTargetUri());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(defaultUriMedium, dto.getUriMedium());
    assertEquals(defaultUriSmall, dto.getUriSmall());
    assertEquals(entity.getActiveIfLogout(), dto.getActiveIfLogout());
    assertEquals(entity.getQa(), dto.getQa());
    assertEquals(dto.getDisabled(), dto.getDisabled());
    assertEquals(entity.getShowUserMenu(), dto.getShowUserMenu());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "bma";

    UserMenu entity = new UserMenu();
    entity.setSvg("<svg/>");
    entity.setSvgId("#icon-live");
    entity.setTargetUri("/live-stream");
    entity.setLinkTitle("LIVE STREAMING");
    entity.setUriMedium("/medium.png");
    entity.setUriSmall("/small.png");
    entity.setActiveIfLogout(Boolean.TRUE);
    entity.setQa("QA");
    entity.setDisabled(Boolean.TRUE);
    entity.setShowUserMenu("both");

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<UserMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    UserMenuDto dto = list.get(0);
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getUriMedium(), dto.getUriMedium());
    assertEquals(entity.getUriSmall(), dto.getUriSmall());
    assertEquals(entity.getActiveIfLogout(), dto.getActiveIfLogout());
    assertEquals(entity.getQa(), dto.getQa());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getShowUserMenu(), dto.getShowUserMenu());
  }
}
