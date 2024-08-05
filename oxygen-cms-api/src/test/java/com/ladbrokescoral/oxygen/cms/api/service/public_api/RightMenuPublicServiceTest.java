package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.*;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.RightMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.RightMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.RightMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
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
public class RightMenuPublicServiceTest {

  @Mock private RightMenuExtendedRepository repository;

  private RightMenuPublicService service;

  @Before
  public void init() {
    RightMenuService menuService =
        new RightMenuService(
            null,
            repository,
            null,
            null,
            ImagePath.builder()
                .smallSize(new ImageServiceImpl.Size("10x10"))
                .mediumSize(new ImageServiceImpl.Size("20x20"))
                .largeSize(new ImageServiceImpl.Size("30x30"))
                .build());
    service = new RightMenuPublicService(menuService);
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    RightMenu entity = new RightMenu();

    when(repository.findRightMenus("connect")).thenReturn(Collections.singletonList(entity));

    // act
    List<RightMenuDto> list =
        service.findByBrand("retail"); // retail 'brand' is mapped to 'connect'

    // arrange
    assertEquals(1, list.size());

    RightMenuDto dto = list.get(0);
    assertNull(dto.getId());
    assertNull(dto.getSvg());
    assertNull(dto.getSvgId());
    assertEquals(StringUtils.EMPTY, dto.getUriLarge());
    assertEquals(StringUtils.EMPTY, dto.getUriMedium());
    assertEquals(StringUtils.EMPTY, dto.getUriSmall());
    assertNull(dto.getSection());
    assertNull(dto.getType());
    assertNull(dto.getShowItemFor());
    assertTrue(dto.getShowOnlyOnOS().isEmpty());
    assertNull(dto.getQa());
    assertNull(dto.getIconAlignment());
    assertNull(dto.getAuthRequired());
    assertNull(dto.getSystemID());
    assertEquals(StringUtils.EMPTY, dto.getButtonClass());
    assertNull(dto.getStartUrl());
    assertNull(dto.getSubHeader());
    assertEquals(StringUtils.EMPTY, dto.getLinkTitle());
    assertNull(dto.getTargetUri());
    assertNull(dto.getDisabled());
  }

  @Test
  public void testFindByBrandEmptyEntity() {
    // arrange
    String brand = "connect";

    RightMenu entity = new RightMenu();
    entity.setId(StringUtils.EMPTY);
    entity.setSvg(StringUtils.EMPTY);
    entity.setSvgId(StringUtils.EMPTY);
    entity.setUriLarge(StringUtils.EMPTY);
    entity.setUriMedium(StringUtils.EMPTY);
    entity.setUriSmall(StringUtils.EMPTY);
    entity.setSection(StringUtils.EMPTY);
    entity.setType(StringUtils.EMPTY);
    entity.setShowItemFor(StringUtils.EMPTY);
    entity.setQa(StringUtils.EMPTY);
    entity.setIconAligment(StringUtils.EMPTY);
    entity.setAuthRequired(Boolean.FALSE);
    entity.setSystemID(0);
    entity.setStartUrl(StringUtils.EMPTY);
    entity.setSubHeader(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setDisabled(Boolean.FALSE);
    entity.setInApp(Boolean.FALSE);
    entity.setShowOnlyOnIOS(Boolean.FALSE);
    entity.setShowOnlyOnAndroid(Boolean.FALSE);

    when(repository.findRightMenus(brand)).thenReturn(Collections.singletonList(entity));

    // act
    List<RightMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    RightMenuDto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertEquals(entity.getUriLarge(), dto.getUriLarge());
    assertEquals(entity.getUriMedium(), dto.getUriMedium());
    assertEquals(entity.getUriSmall(), dto.getUriSmall());
    assertEquals(entity.getSection(), dto.getSection());
    assertEquals(entity.getType(), dto.getType());
    assertEquals(entity.getShowItemFor(), dto.getShowItemFor());
    assertEquals(entity.getQa(), dto.getQa());
    assertEquals(entity.getIconAligment(), dto.getIconAlignment());
    assertEquals(entity.getAuthRequired(), dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertEquals(StringUtils.EMPTY, dto.getButtonClass());
    assertEquals(entity.getStartUrl(), dto.getStartUrl());
    assertEquals(entity.getSubHeader(), dto.getSubHeader());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertTrue(dto.getShowOnlyOnOS().isEmpty());
  }

  @Test
  public void testFindByBrandShowOnlyOnOSCases() {
    // arrange
    String brand = "ladbrokes";

    RightMenu entity1 = new RightMenu();
    entity1.setShowOnlyOnIOS(Boolean.TRUE);
    entity1.setShowOnlyOnAndroid(Boolean.FALSE);

    RightMenu entity2 = new RightMenu();
    entity2.setShowOnlyOnIOS(Boolean.FALSE);
    entity2.setShowOnlyOnAndroid(Boolean.TRUE);

    RightMenu entity3 = new RightMenu();
    entity3.setShowOnlyOnIOS(Boolean.TRUE);
    entity3.setShowOnlyOnAndroid(Boolean.TRUE);

    when(repository.findRightMenus(brand)).thenReturn(Arrays.asList(entity1, entity2, entity3));

    // act
    List<RightMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(3, list.size());

    RightMenuDto dto1 = list.get(0);
    assertEquals(1, dto1.getShowOnlyOnOS().size());
    assertEquals("ios", dto1.getShowOnlyOnOS().get(0));

    RightMenuDto dto2 = list.get(1);
    assertEquals(1, dto2.getShowOnlyOnOS().size());
    assertEquals("android", dto2.getShowOnlyOnOS().get(0));

    RightMenuDto dto3 = list.get(2);
    assertEquals(2, dto3.getShowOnlyOnOS().size());
    assertArrayEquals(new String[] {"ios", "android"}, dto3.getShowOnlyOnOS().toArray());
  }

  @Test
  public void testFindByBrandUpdateRightMenuCases() {
    // arrange
    String brand = "secondscreen";

    RightMenu entity1 = new RightMenu();
    entity1.setType("link");

    RightMenu entity2 = new RightMenu();
    entity2.setType("link");
    entity2.setTargetUri("/settings");

    RightMenu entity3 = new RightMenu();
    entity3.setTargetUri("/login");

    RightMenu entity4 = new RightMenu();
    entity4.setType("icon");

    RightMenu entity5 = new RightMenu();
    entity5.setType("icon");
    entity5.setTargetUri("/contact");

    when(repository.findRightMenus(brand))
        .thenReturn(Arrays.asList(entity1, entity2, entity3, entity4, entity5));

    // act
    List<RightMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(5, list.size());

    RightMenuDto dto1 = list.get(0);
    assertEquals(StringUtils.EMPTY, dto1.getTargetUri());
    assertNull(dto1.getButtonClass());

    RightMenuDto dto2 = list.get(1);
    assertEquals(entity2.getTargetUri(), dto2.getTargetUri());
    assertNull(dto2.getButtonClass());

    RightMenuDto dto3 = list.get(2);
    assertEquals(entity3.getTargetUri(), dto3.getTargetUri());
    assertEquals(entity3.getTargetUri(), dto3.getButtonClass());

    RightMenuDto dto4 = list.get(3);
    assertEquals(entity4.getTargetUri(), dto4.getTargetUri());
    assertEquals(StringUtils.EMPTY, dto4.getButtonClass());

    RightMenuDto dto5 = list.get(4);
    assertEquals(entity5.getTargetUri(), dto5.getTargetUri());
    assertEquals(entity5.getTargetUri(), dto5.getButtonClass());
  }

  @Test
  public void testFindByBrandLinkTitleCases() {
    // arrange
    String brand = "rcomb";

    RightMenu entity1 = new RightMenu();
    entity1.setMenuItemView("icon");

    RightMenu entity2 = new RightMenu();
    entity2.setMenuItemView("icon");
    entity2.setLinkTitle("Settings");

    RightMenu entity3 = new RightMenu();
    entity3.setMenuItemView("link");

    RightMenu entity4 = new RightMenu();
    entity4.setMenuItemView("link");
    entity4.setLinkTitle("Features");

    when(repository.findRightMenus(brand))
        .thenReturn(Arrays.asList(entity1, entity2, entity3, entity4));

    // act
    List<RightMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(4, list.size());

    RightMenuDto dto1 = list.get(0);
    assertEquals(StringUtils.EMPTY, dto1.getLinkTitle());

    RightMenuDto dto2 = list.get(1);
    assertEquals(StringUtils.EMPTY, dto2.getLinkTitle());

    RightMenuDto dto3 = list.get(2);
    assertEquals(StringUtils.EMPTY, dto3.getLinkTitle());

    RightMenuDto dto4 = list.get(3);
    assertEquals(entity4.getLinkTitle(), dto4.getLinkTitle());
  }

  @Test
  public void testFindByBrandImageUriCases() {
    // arrange
    String brand = "bma";

    RightMenu entity1 = new RightMenu();
    entity1.setUriLarge("/large.png");
    entity1.setUriMedium("/medium.png");
    entity1.setUriSmall("/small.png");

    RightMenu entity2 = new RightMenu();
    entity2.setMenuItemView("description");
    entity2.setUriLarge("/large.png");
    entity2.setUriMedium("/medium.png");
    entity2.setUriSmall("/small.png");

    RightMenu entity3 = new RightMenu();
    entity3.setMenuItemView("link");

    RightMenu entity4 = new RightMenu();
    entity4.setMenuItemView("link");
    entity4.setUriLarge("public-large.png");
    entity4.setUriMedium("public-medium.png");
    entity4.setUriSmall("public-small.png");

    when(repository.findRightMenus(brand))
        .thenReturn(Arrays.asList(entity1, entity2, entity3, entity4));

    // act
    List<RightMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(4, list.size());

    RightMenuDto dto1 = list.get(0);
    assertEquals(StringUtils.EMPTY, dto1.getUriLarge());
    assertEquals(StringUtils.EMPTY, dto1.getUriMedium());
    assertEquals(StringUtils.EMPTY, dto1.getUriSmall());

    RightMenuDto dto2 = list.get(1);
    assertEquals(StringUtils.EMPTY, dto2.getUriLarge());
    assertEquals(StringUtils.EMPTY, dto2.getUriMedium());
    assertEquals(StringUtils.EMPTY, dto2.getUriSmall());

    RightMenuDto dto3 = list.get(2);
    assertEquals("/images/uploads/right_menu/default/default-156x156.png", dto3.getUriLarge());
    assertEquals("/images/uploads/right_menu/default/default-156x156.png", dto3.getUriMedium());
    assertEquals("/images/uploads/right_menu/default/default-104x104.png", dto3.getUriSmall());

    RightMenuDto dto4 = list.get(3);
    assertEquals("-large.png", dto4.getUriLarge());
    assertEquals("-medium.png", dto4.getUriMedium());
    assertEquals("-small.png", dto4.getUriSmall());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "partner";

    RightMenu entity = new RightMenu();
    entity.setId("ID1");
    entity.setSvg("<svg1/>");
    entity.setSvgId("#icon-log-in");
    entity.setMenuItemView("item");
    entity.setUriLarge("/large.png");
    entity.setUriMedium("/medium.png");
    entity.setUriSmall("/small.png");
    entity.setSection("top");
    entity.setType("link");
    entity.setShowItemFor("loggedOut");
    entity.setQa("QA1");
    entity.setIconAligment("left");
    entity.setAuthRequired(Boolean.TRUE);
    entity.setSystemID(1);
    entity.setStartUrl("http://test.com/start");
    entity.setSubHeader("log in");
    entity.setLinkTitle("Log in");
    entity.setTargetUri("log-in");
    entity.setDisabled(Boolean.TRUE);
    entity.setInApp(Boolean.TRUE);
    entity.setShowOnlyOnIOS(Boolean.TRUE);
    entity.setShowOnlyOnAndroid(Boolean.TRUE);

    when(repository.findRightMenus(brand)).thenReturn(Collections.singletonList(entity));

    // act
    List<RightMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    RightMenuDto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertEquals(entity.getUriLarge(), dto.getUriLarge());
    assertEquals(entity.getUriMedium(), dto.getUriMedium());
    assertEquals(entity.getUriSmall(), dto.getUriSmall());
    assertEquals(entity.getSection(), dto.getSection());
    assertEquals(entity.getType(), dto.getType());
    assertEquals(entity.getShowItemFor(), dto.getShowItemFor());
    assertEquals(entity.getQa(), dto.getQa());
    assertEquals(entity.getIconAligment(), dto.getIconAlignment());
    assertEquals(entity.getAuthRequired(), dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertNull(dto.getButtonClass());
    assertEquals(entity.getStartUrl(), dto.getStartUrl());
    assertEquals(entity.getSubHeader(), dto.getSubHeader());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getDisabled(), dto.getDisabled());
    assertEquals(2, dto.getShowOnlyOnOS().size());
    assertArrayEquals(new String[] {"ios", "android"}, dto.getShowOnlyOnOS().toArray());
  }
}
