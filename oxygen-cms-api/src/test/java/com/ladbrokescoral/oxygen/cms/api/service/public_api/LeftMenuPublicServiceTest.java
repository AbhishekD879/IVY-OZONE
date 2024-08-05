package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.*;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.BaseMenuDto;
import com.ladbrokescoral.oxygen.cms.api.dto.LeftMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LeftMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.LeftMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.LeftMenuService;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class LeftMenuPublicServiceTest {

  @Mock private LeftMenuRepository repository;

  private LeftMenuPublicService service;

  @Before
  public void init() {
    LeftMenuService menuService = new LeftMenuService(repository);
    service = new LeftMenuPublicService(menuService);
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    String brand = "bma";

    LeftMenu entity = new LeftMenu();

    when(repository.findAllByBrandOrderBySortOrderAsc(brand))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<LeftMenuDto> list = service.findByBrand(brand);

    // assert
    assertEquals(1, list.size());

    LeftMenuDto dto = list.get(0);
    assertNull(dto.getTargetUri());
    assertNull(dto.getLinkTitle());
    assertNull(dto.getInApp());
    assertNull(dto.getShowItemFor());
    assertTrue(dto.getChildren().isEmpty());
  }

  @Test
  public void testFindByBrandEmptyEntity() {
    // arrange
    String brand = "connect";

    LeftMenu entity = new LeftMenu();
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setInApp(Boolean.FALSE);
    entity.setShowItemFor(StringUtils.EMPTY);

    when(repository.findAllByBrandOrderBySortOrderAsc(brand))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<LeftMenuDto> list = service.findByBrand(brand);

    // assert
    assertEquals(1, list.size());

    LeftMenuDto dto = list.get(0);
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getInApp(), dto.getInApp());
    assertEquals(entity.getShowItemFor(), dto.getShowItemFor());
    assertTrue(dto.getChildren().isEmpty());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "retail";

    LeftMenu parentEntity = new LeftMenu();
    parentEntity.setId("PARENT_ID");
    parentEntity.setTargetUri("/connect");
    parentEntity.setLinkTitle("Home");
    parentEntity.setInApp(Boolean.TRUE);
    parentEntity.setShowItemFor("both");

    LeftMenu childEntity = new LeftMenu();
    childEntity.setId("CHILD_ID");
    childEntity.setParent(parentEntity.getId());
    childEntity.setTargetUri("/connect/offers");
    childEntity.setLinkTitle("Offers");
    childEntity.setDisabled(Boolean.TRUE);
    childEntity.setInApp(Boolean.TRUE);
    childEntity.setShowItemFor("both");

    when(repository.findAllByBrandOrderBySortOrderAsc(brand))
        .thenReturn(Arrays.asList(parentEntity, childEntity));

    // act
    List<LeftMenuDto> list = service.findByBrand(brand);

    // assert
    assertEquals(1, list.size());

    LeftMenuDto parentDto = list.get(0);
    assertEquals(parentEntity.getTargetUri(), parentDto.getTargetUri());
    assertEquals(parentEntity.getLinkTitle(), parentDto.getLinkTitle());
    assertEquals(parentEntity.getInApp(), parentDto.getInApp());
    assertEquals(parentEntity.getShowItemFor(), parentDto.getShowItemFor());
    assertEquals(1, parentDto.getChildren().size());

    BaseMenuDto childDto = (BaseMenuDto) parentDto.getChildren().get(0);
    assertNull(childDto.getId());
    assertEquals(childEntity.getTargetUri(), childDto.getTargetUri());
    assertEquals(childEntity.getLinkTitle(), childDto.getLinkTitle());
    assertEquals(childEntity.getDisabled(), childDto.getDisabled());
    assertEquals(childEntity.getInApp(), childDto.getInApp());
  }
}
