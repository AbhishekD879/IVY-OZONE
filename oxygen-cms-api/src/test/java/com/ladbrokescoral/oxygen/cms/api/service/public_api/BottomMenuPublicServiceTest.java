package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.BottomMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BottomMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.BottomMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BottomMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.util.Collections;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BottomMenuPublicServiceTest {

  @Mock private BottomMenuRepository repository;

  private BottomMenuPublicService service;

  @Before
  public void init() {
    BottomMenuService menuService = new BottomMenuService(repository);
    service = new BottomMenuPublicService(menuService);
  }

  @Test
  public void testFindUninitializedEntity() {
    // arrange
    String brand = "bma";

    BottomMenu entity = new BottomMenu();

    when(repository.findAllByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BottomMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    BottomMenuDto dto = list.iterator().next();
    assertNull(dto.getId());
    assertNull(dto.getAuthRequired());
    assertNull(dto.getSystemID());
    assertNull(dto.getStartUrl());
    assertNull(dto.getLinkTitle());
    assertNull(dto.getTargetUri());
    assertNull(dto.getDisabled());
    assertNull(dto.getInApp());
  }

  @Test
  public void testFindEmptyEntity() {
    // arrange
    String brand = "connect";

    BottomMenu entity = new BottomMenu();
    entity.setId(StringUtils.EMPTY);
    entity.setAuthRequired(Boolean.FALSE);
    entity.setSystemID(0);
    entity.setStartUrl(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setDisabled(Boolean.FALSE);
    entity.setInApp(Boolean.FALSE);

    when(repository.findAllByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BottomMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    BottomMenuDto dto = list.iterator().next();
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getAuthRequired(), dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertEquals(entity.getStartUrl(), dto.getStartUrl());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getInApp(), dto.getInApp());
  }

  @Test
  public void testFind() {
    // arrange
    String brand = "retail";

    BottomMenu entity = new BottomMenu();
    entity.setId("ID");
    entity.setAuthRequired(Boolean.TRUE);
    entity.setSystemID(1);
    entity.setStartUrl("/about");
    entity.setLinkTitle("About us");
    entity.setTargetUri("http://test.com/app/about");
    entity.setDisabled(Boolean.TRUE);
    entity.setInApp(Boolean.TRUE);

    when(repository.findAllByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BottomMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    BottomMenuDto dto = list.iterator().next();
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getAuthRequired(), dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertEquals(entity.getStartUrl(), dto.getStartUrl());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getInApp(), dto.getInApp());
  }
}
