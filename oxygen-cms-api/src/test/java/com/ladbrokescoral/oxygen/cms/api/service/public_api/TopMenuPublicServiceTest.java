package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.TopMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TopMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.TopMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TopMenuService;
import java.util.Collections;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TopMenuPublicServiceTest {

  @Mock private TopMenuRepository repository;

  private TopMenuPublicService service;

  @Before
  public void init() {
    TopMenuService menuService = new TopMenuService(repository);
    service = new TopMenuPublicService(menuService);
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    String brand = "bma";

    TopMenu entity = new TopMenu();

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<TopMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    TopMenuDto dto = list.get(0);
    assertNull(dto.getLinkTitle());
    assertNull(dto.getTargetUri());
    assertNull(dto.getDisabled());
  }

  @Test
  public void testFindByBrandEmptyEntity() {
    // arrange
    String brand = "connect";

    TopMenu entity = new TopMenu();
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setDisabled(Boolean.FALSE);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<TopMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    TopMenuDto dto = list.get(0);
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "retail";

    TopMenu entity = new TopMenu();
    entity.setLinkTitle("Football");
    entity.setTargetUri("/football");
    entity.setDisabled(Boolean.TRUE);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<TopMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    TopMenuDto dto = list.get(0);
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
  }
}
