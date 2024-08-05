package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.*;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.BaseMenuDto;
import com.ladbrokescoral.oxygen.cms.api.dto.HeaderMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.HeaderMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderMenuService;
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
public class HeaderMenuPublicServiceTest {

  @Mock private HeaderMenuRepository repository;

  private HeaderMenuPublicService service;

  @Before
  public void init() {
    HeaderMenuService menuService = new HeaderMenuService(repository);
    service = new HeaderMenuPublicService(menuService);
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    String brand = "rcomb";

    HeaderMenu entity = new HeaderMenu();

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderMenuDto dto = list.get(0);
    assertNull(dto.getId());
    assertNull(dto.getLinkTitle());
    assertNull(dto.getTargetUri());
    assertNull(dto.getDisabled());
    assertTrue(dto.getInApp());
    assertTrue(dto.getChildren().isEmpty());
  }

  @Test
  public void testFindByBrandEmptyEntity() {
    // arrange
    String brand = "ladbrokes";

    HeaderMenu entity = new HeaderMenu();
    entity.setId(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setDisabled(Boolean.FALSE);
    entity.setInApp(Boolean.FALSE);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderMenuDto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getInApp(), dto.getInApp());
    assertTrue(dto.getChildren().isEmpty());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "secondscreen";

    HeaderMenu parentEntity = new HeaderMenu();
    parentEntity.setId("PARENT_ID");
    parentEntity.setLinkTitle("Top");
    parentEntity.setTargetUri("/top");
    parentEntity.setDisabled(Boolean.TRUE);
    parentEntity.setInApp(Boolean.TRUE);

    HeaderMenu childEntity = new HeaderMenu();
    childEntity.setId("CHILD_ID");
    childEntity.setParent(parentEntity.getId());
    childEntity.setLinkTitle("Sub");
    childEntity.setTargetUri("/top/sub");
    childEntity.setDisabled(Boolean.TRUE);
    childEntity.setInApp(Boolean.TRUE);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Arrays.asList(parentEntity, childEntity));

    // act
    List<HeaderMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderMenuDto parentDto = list.get(0);
    assertEquals(parentEntity.getId(), parentDto.getId());
    assertEquals(parentEntity.getLinkTitle(), parentDto.getLinkTitle());
    assertEquals(parentEntity.getTargetUri(), parentDto.getTargetUri());
    assertEquals(parentEntity.getDisabled(), parentDto.getDisabled());
    assertEquals(parentEntity.getInApp(), parentDto.getInApp());
    assertEquals(1, parentDto.getChildren().size());

    BaseMenuDto childDto = parentDto.getChildren().get(0);
    assertEquals(childEntity.getId(), childDto.getId());
    assertEquals(childEntity.getLinkTitle(), childDto.getLinkTitle());
    assertEquals(childEntity.getTargetUri(), childDto.getTargetUri());
    assertEquals(childEntity.getDisabled(), childDto.getDisabled());
    assertEquals(childEntity.getInApp(), childDto.getInApp());
  }
}
