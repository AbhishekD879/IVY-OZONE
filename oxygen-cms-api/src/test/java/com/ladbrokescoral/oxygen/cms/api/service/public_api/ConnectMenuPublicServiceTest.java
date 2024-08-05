package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.ConnectMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.ConnectMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ConnectMenuService;
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
public class ConnectMenuPublicServiceTest {

  @Mock private ConnectMenuRepository repository;

  private ConnectMenuPublicService service;

  @Before
  public void init() {
    ConnectMenuService menuService = new ConnectMenuService(repository, null, null);
    service = new ConnectMenuPublicService(menuService);
  }

  @Test
  public void testFindAllByBrandUninitializedEntity() {
    // arrange
    String brand = "bma";

    ConnectMenu entity = new ConnectMenu();

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<ConnectMenuDto> list = service.findByBrand(brand);

    // assert
    assertEquals(1, list.size());

    ConnectMenuDto dto = list.iterator().next();
    assertNull(dto.getUpgradePopup());
    assertNull(dto.getSvg());
    assertNull(dto.getSvgId());
    assertNull(dto.getTargetUri());
    assertNull(dto.getLinkTitle());
    assertEquals(StringUtils.EMPTY, dto.getLinkSubtitle());
    assertNull(dto.getInApp());
    assertNull(dto.getShowItemFor());
    assertTrue(dto.getChildren().isEmpty());
  }

  @Test
  public void testFindAllByBrandEmptyEntity() {
    // arrange
    String brand = "retail";

    ConnectMenu entity = new ConnectMenu();
    entity.setUpgradePopup(Boolean.FALSE);
    entity.setSvg(StringUtils.EMPTY);
    entity.setSvgId(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setLinkSubtitle(StringUtils.EMPTY);
    entity.setInApp(Boolean.FALSE);
    entity.setShowItemFor(StringUtils.EMPTY);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<ConnectMenuDto> list = service.findByBrand(brand);

    // assert
    assertEquals(1, list.size());

    ConnectMenuDto dto = list.iterator().next();
    assertEquals(entity.getUpgradePopup(), dto.getUpgradePopup());
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getLinkSubtitle(), dto.getLinkSubtitle());
    assertEquals(entity.getInApp(), dto.getInApp());
    assertEquals(entity.getShowItemFor(), dto.getShowItemFor());
    assertTrue(dto.getChildren().isEmpty());
  }

  @Test
  public void testFindAllByBrand() {
    // arrange
    String brand = "connect";

    ConnectMenu parentEntity = new ConnectMenu();
    parentEntity.setId("PARENT_ID");
    parentEntity.setUpgradePopup(Boolean.TRUE);
    parentEntity.setSvg("<svg/>");
    parentEntity.setSvgId("#abc");
    parentEntity.setTargetUri("/shop-locator");
    parentEntity.setLinkTitle("Shop Locator");
    parentEntity.setLinkSubtitle("Find the Coral shops around you.");
    parentEntity.setInApp(Boolean.TRUE);
    parentEntity.setShowItemFor("both");

    ConnectMenu childEntity = new ConnectMenu();
    childEntity.setId("CHILD_ID");
    childEntity.setParent("PARENT_ID");
    childEntity.setUpgradePopup(Boolean.FALSE);
    childEntity.setSvg("<svg/>");
    childEntity.setSvgId("#xyz");
    childEntity.setTargetUri("/bet-filter");
    childEntity.setLinkTitle("Football Bet Filter");
    childEntity.setLinkSubtitle("Use the bet filters to find the perfect bet.");
    childEntity.setInApp(Boolean.TRUE);
    childEntity.setShowItemFor("existing");

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE))
        .thenReturn(Arrays.asList(parentEntity, childEntity));

    // act
    List<ConnectMenuDto> list = service.findByBrand(brand);

    // assert
    assertEquals(1, list.size());

    ConnectMenuDto parentDto = list.iterator().next();
    assertEquals(parentEntity.getUpgradePopup(), parentDto.getUpgradePopup());
    assertEquals(parentEntity.getSvg(), parentDto.getSvg());
    assertEquals(parentEntity.getSvgId(), parentDto.getSvgId());
    assertEquals(parentEntity.getTargetUri(), parentDto.getTargetUri());
    assertEquals(parentEntity.getLinkTitle(), parentDto.getLinkTitle());
    assertEquals(parentEntity.getLinkSubtitle(), parentDto.getLinkSubtitle());
    assertEquals(parentEntity.getInApp(), parentDto.getInApp());
    assertEquals(parentEntity.getShowItemFor(), parentDto.getShowItemFor());
    assertEquals(1, parentDto.getChildren().size());

    assertEquals(childEntity, parentDto.getChildren().get(0));
  }
}
