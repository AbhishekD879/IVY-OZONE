package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderContactMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderContactMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.HeaderContactMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.HeaderContactMenuService;
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
public class HeaderContactMenuPublicServiceTest {

  @Mock private HeaderContactMenuRepository repository;

  private HeaderContactMenuPublicService service;

  @Before
  public void init() {
    HeaderContactMenuService menuService = new HeaderContactMenuService(repository);
    service = new HeaderContactMenuPublicService(menuService);
  }

  @Test
  public void testFindUninitializedEntity() {
    // arrange
    String brand = "connect";

    HeaderContactMenu entity = new HeaderContactMenu();

    when(repository.findAllByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderContactMenuDto> list = service.find(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderContactMenuDto dto = list.get(0);
    assertNull(dto.getId());
    assertNull(dto.getAuthRequired());
    assertNull(dto.getDisabled());
    assertNull(dto.getInApp());
    assertNull(dto.getSystemID());
    assertNull(dto.getLinkTitle());
    assertNull(dto.getLabel());
    assertNull(dto.getTargetUri());
  }

  @Test
  public void testFindEmptyEntity() {
    // arrange
    String brand = "ladbrokes";

    HeaderContactMenu entity = new HeaderContactMenu();
    entity.setId(StringUtils.EMPTY);
    entity.setAuthRequired(Boolean.FALSE);
    entity.setDisabled(Boolean.FALSE);
    entity.setInApp(Boolean.FALSE);
    entity.setSystemID(0);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setLabel(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);

    when(repository.findAllByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderContactMenuDto> list = service.find(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderContactMenuDto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getAuthRequired(), dto.getAuthRequired());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getInApp(), dto.getInApp());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getLabel(), dto.getLabel());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
  }

  @Test
  public void testFind() {
    // arrange
    String brand = "bma";

    HeaderContactMenu entity = new HeaderContactMenu();
    entity.setId("ID");
    entity.setAuthRequired(Boolean.TRUE);
    entity.setDisabled(Boolean.TRUE);
    entity.setInApp(Boolean.TRUE);
    entity.setSystemID(1);
    entity.setLinkTitle("Contact Us Link");
    entity.setLabel("Contact US");
    entity.setTargetUri("http://test.com/help");

    when(repository.findAllByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<HeaderContactMenuDto> list = service.find(brand);

    // arrange
    assertEquals(1, list.size());

    HeaderContactMenuDto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getAuthRequired(), dto.getAuthRequired());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(entity.getInApp(), dto.getInApp());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getLabel(), dto.getLabel());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
  }
}
