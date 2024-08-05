package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.BankingMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.BankingMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BankingMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl.Size;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BankingMenuPublicServiceTest {

  @Mock private BankingMenuExtendedRepository repository;

  private BankingMenuPublicService service;

  @Before
  public void init() {

    BankingMenuService menuService =
        new BankingMenuService(
            null,
            repository,
            null,
            null,
            ImagePath.builder()
                .smallSize(new Size("10x10"))
                .mediumSize(new Size("20x20"))
                .largeSize(new Size("30x30"))
                .build());
    service = new BankingMenuPublicService(menuService);
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    BankingMenu entity = new BankingMenu();

    when(repository.findMenus("connect")).thenReturn(Collections.singletonList(entity));

    // act
    List<BankingMenuDto> list =
        service.findByBrand("retail"); // retail 'brand' is mapped to 'connect'

    // arrange
    assertEquals(1, list.size());

    BankingMenuDto dto = list.iterator().next();
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

    BankingMenu entity = new BankingMenu();
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

    when(repository.findMenus(brand)).thenReturn(Collections.singletonList(entity));

    // act
    List<BankingMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    BankingMenuDto dto = list.iterator().next();
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

    BankingMenu entity1 = new BankingMenu();
    entity1.setShowOnlyOnIOS(Boolean.TRUE);
    entity1.setShowOnlyOnAndroid(Boolean.FALSE);

    BankingMenu entity2 = new BankingMenu();
    entity2.setShowOnlyOnIOS(Boolean.FALSE);
    entity2.setShowOnlyOnAndroid(Boolean.TRUE);

    BankingMenu entity3 = new BankingMenu();
    entity3.setShowOnlyOnIOS(Boolean.TRUE);
    entity3.setShowOnlyOnAndroid(Boolean.TRUE);

    when(repository.findMenus(brand)).thenReturn(Arrays.asList(entity1, entity2, entity3));

    // act
    List<BankingMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(3, list.size());

    Iterator<BankingMenuDto> iterator = list.iterator();

    BankingMenuDto dto1 = iterator.next();
    assertEquals(1, dto1.getShowOnlyOnOS().size());
    assertEquals("ios", dto1.getShowOnlyOnOS().get(0));

    BankingMenuDto dto2 = iterator.next();
    assertEquals(1, dto2.getShowOnlyOnOS().size());
    assertEquals("android", dto2.getShowOnlyOnOS().get(0));

    BankingMenuDto dto3 = iterator.next();
    assertEquals(2, dto3.getShowOnlyOnOS().size());
    assertArrayEquals(new String[] {"ios", "android"}, dto3.getShowOnlyOnOS().toArray());
  }

  @Test
  public void testFindByBrandUpdateBankingMenuCases() {
    // arrange
    String brand = "secondscreen";

    BankingMenu entity1 = new BankingMenu();
    entity1.setType("link");

    BankingMenu entity2 = new BankingMenu();
    entity2.setType("link");
    entity2.setTargetUri("/settings");

    BankingMenu entity3 = new BankingMenu();
    entity3.setTargetUri("/login");

    BankingMenu entity4 = new BankingMenu();
    entity4.setType("icon");

    BankingMenu entity5 = new BankingMenu();
    entity5.setType("icon");
    entity5.setTargetUri("/contact");

    when(repository.findMenus(brand))
        .thenReturn(Arrays.asList(entity1, entity2, entity3, entity4, entity5));

    // act
    List<BankingMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(5, list.size());

    Iterator<BankingMenuDto> iterator = list.iterator();

    BankingMenuDto dto1 = iterator.next();
    assertEquals(StringUtils.EMPTY, dto1.getTargetUri());
    assertNull(dto1.getButtonClass());

    BankingMenuDto dto2 = iterator.next();
    assertEquals(entity2.getTargetUri(), dto2.getTargetUri());
    assertNull(dto2.getButtonClass());

    BankingMenuDto dto3 = iterator.next();
    assertEquals(entity3.getTargetUri(), dto3.getTargetUri());
    assertEquals(entity3.getTargetUri(), dto3.getButtonClass());

    BankingMenuDto dto4 = iterator.next();
    assertEquals(entity4.getTargetUri(), dto4.getTargetUri());
    assertEquals(StringUtils.EMPTY, dto4.getButtonClass());

    BankingMenuDto dto5 = iterator.next();
    assertEquals(entity5.getTargetUri(), dto5.getTargetUri());
    assertEquals(entity5.getTargetUri(), dto5.getButtonClass());
  }

  @Test
  public void testFindByBrandLinkTitleCases() {
    // arrange
    String brand = "rcomb";

    BankingMenu entity1 = new BankingMenu();
    entity1.setMenuItemView("icon");

    BankingMenu entity2 = new BankingMenu();
    entity2.setMenuItemView("icon");
    entity2.setLinkTitle("Settings");

    BankingMenu entity3 = new BankingMenu();
    entity3.setMenuItemView("link");

    BankingMenu entity4 = new BankingMenu();
    entity4.setMenuItemView("link");
    entity4.setLinkTitle("Features");

    when(repository.findMenus(brand)).thenReturn(Arrays.asList(entity1, entity2, entity3, entity4));

    // act
    List<BankingMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(4, list.size());

    Iterator<BankingMenuDto> iterator = list.iterator();

    BankingMenuDto dto1 = iterator.next();
    assertEquals(StringUtils.EMPTY, dto1.getLinkTitle());

    BankingMenuDto dto2 = iterator.next();
    assertEquals(StringUtils.EMPTY, dto2.getLinkTitle());

    BankingMenuDto dto3 = iterator.next();
    assertEquals(StringUtils.EMPTY, dto3.getLinkTitle());

    BankingMenuDto dto4 = iterator.next();
    assertEquals(entity4.getLinkTitle(), dto4.getLinkTitle());
  }

  @Test
  public void testFindByBrandImageUriCases() {
    // arrange
    String brand = "bma";

    BankingMenu entity1 = new BankingMenu();
    entity1.setUriLarge("/large.png");
    entity1.setUriMedium("/medium.png");
    entity1.setUriSmall("/small.png");

    BankingMenu entity2 = new BankingMenu();
    entity2.setMenuItemView("description");
    entity2.setUriLarge("/large.png");
    entity2.setUriMedium("/medium.png");
    entity2.setUriSmall("/small.png");

    BankingMenu entity3 = new BankingMenu();
    entity3.setMenuItemView("link");

    BankingMenu entity4 = new BankingMenu();
    entity4.setMenuItemView("link");
    entity4.setUriLarge("public-large.png");
    entity4.setUriMedium("public-medium.png");
    entity4.setUriSmall("public-small.png");

    when(repository.findMenus(brand)).thenReturn(Arrays.asList(entity1, entity2, entity3, entity4));

    // act
    List<BankingMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(4, list.size());

    Iterator<BankingMenuDto> iterator = list.iterator();

    BankingMenuDto dto1 = iterator.next();
    assertEquals(StringUtils.EMPTY, dto1.getUriLarge());
    assertEquals(StringUtils.EMPTY, dto1.getUriMedium());
    assertEquals(StringUtils.EMPTY, dto1.getUriSmall());

    BankingMenuDto dto2 = iterator.next();
    assertEquals(StringUtils.EMPTY, dto2.getUriLarge());
    assertEquals(StringUtils.EMPTY, dto2.getUriMedium());
    assertEquals(StringUtils.EMPTY, dto2.getUriSmall());

    BankingMenuDto dto3 = iterator.next();
    assertEquals("/images/uploads/right_menu/default/default-156x156.png", dto3.getUriLarge());
    assertEquals("/images/uploads/right_menu/default/default-156x156.png", dto3.getUriMedium());
    assertEquals("/images/uploads/right_menu/default/default-104x104.png", dto3.getUriSmall());

    BankingMenuDto dto4 = iterator.next();
    assertEquals("-large.png", dto4.getUriLarge());
    assertEquals("-medium.png", dto4.getUriMedium());
    assertEquals("-small.png", dto4.getUriSmall());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "partner";

    BankingMenu entity = new BankingMenu();
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

    when(repository.findMenus(brand)).thenReturn(Collections.singletonList(entity));

    // act
    List<BankingMenuDto> list = service.findByBrand(brand);

    // arrange
    assertEquals(1, list.size());

    BankingMenuDto dto = list.iterator().next();
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
