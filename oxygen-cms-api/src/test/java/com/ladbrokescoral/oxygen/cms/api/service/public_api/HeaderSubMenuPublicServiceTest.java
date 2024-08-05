package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.*;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderSubMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderSubMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.HeaderSubMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderSubMenuService;
import java.util.Collections;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HeaderSubMenuPublicServiceTest {

  @Mock private HeaderSubMenuRepository repository;

  private HeaderSubMenuPublicService service;

  @Before
  public void init() {
    HeaderSubMenuService menuService = new HeaderSubMenuService(repository);
    service = new HeaderSubMenuPublicService(menuService);
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    String brand = "ladbrokes";

    HeaderSubMenu entity = new HeaderSubMenu();

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderSubMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderSubMenuDto dto = list.get(0);
    assertNull(dto.getId());
    assertNull(dto.getLinkTitle());
    assertNull(dto.getTargetUri());
    assertNull(dto.getDisabled());
    assertTrue(dto.getInApp());
  }

  @Test
  public void testFindByBrandEmptyEntity() {
    // arrange
    String brand = "secondscreen";

    HeaderSubMenu entity = new HeaderSubMenu();
    entity.setId(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setDisabled(Boolean.FALSE);
    entity.setInApp(Boolean.FALSE);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderSubMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderSubMenuDto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getInApp(), dto.getInApp());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "bma";

    HeaderSubMenu entity = new HeaderSubMenu();
    entity.setId("ID");
    entity.setLinkTitle("In-Play");
    entity.setTargetUri("in-play");
    entity.setDisabled(Boolean.TRUE);
    entity.setInApp(Boolean.TRUE);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderSubMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderSubMenuDto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getInApp(), dto.getInApp());
  }
}
