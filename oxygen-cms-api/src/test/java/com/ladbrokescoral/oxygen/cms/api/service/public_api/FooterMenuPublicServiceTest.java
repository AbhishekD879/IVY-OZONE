package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.FooterMenuArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV3Dto;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FooterMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.data.domain.PageRequest;

@RunWith(MockitoJUnitRunner.class)
public class FooterMenuPublicServiceTest {

  @Mock private FooterMenuRepository repository;

  @Mock private FooterMenuArchivalRepository footerMenuArchivalRepository;

  @Mock private ModelMapper modelMapper;

  @Mock private SegmentedModuleSerive segmentedModuleSerive;

  private static final int DEFAULT_QUERY_LIMIT = 5;
  private static final int RCOMB_CONNECT_QUERY_LIMIT = 6;

  PageRequest pageRequest = PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC);

  private FooterMenuPublicService service;
  @Mock SegmentService segmentService;

  @Before
  public void init() {
    FooterMenuService footerMenuService =
        new FooterMenuService(
            repository,
            null,
            null,
            ImagePath.builder()
                .smallSize(new ImageServiceImpl.Size("10x10"))
                .mediumSize(new ImageServiceImpl.Size("20x20"))
                .largeSize(new ImageServiceImpl.Size("30x30"))
                .build(),
            modelMapper,
            footerMenuArchivalRepository,
            segmentService,
            segmentedModuleSerive);
    service = new FooterMenuPublicService(footerMenuService);
  }

  /** FooterMenuPublicService.find(String brand) test cases */
  @Test
  public void testFindByBrandReturnsEmptyListIfNoDeviceSet() {
    // arrange
    String brand = "bma";
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);

    FooterMenu entity = new FooterMenu();
    when(repository.findUniversalRecordsByBrand(brand, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<FooterMenuV3Dto> list = service.find(brand);

    // assert
    assertEquals(0, list.size());
  }

  @Test
  public void testFindByBrandUninitializedEntity() {
    // arrange
    String brand = "connect";

    FooterMenu entity = new FooterMenu();
    entity.setMobile(Boolean.TRUE);
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    when(repository.findUniversalRecordsByBrand(brand, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<FooterMenuV3Dto> list = service.find(brand);

    // assert
    assertEquals(1, list.size());

    FooterMenuV3Dto dto = list.get(0);
    assertNull(dto.getId());
    assertEquals(StringUtils.EMPTY, dto.getTarget());
    assertEquals(StringUtils.EMPTY, dto.getTitle());
    assertEquals(StringUtils.EMPTY, dto.getImage());
    assertEquals(StringUtils.EMPTY, dto.getImageLarge());
    assertNull(dto.getInApp());
    assertNull(dto.getShowItemFor());
    assertNull(dto.getWidget());
    assertNull(dto.getSvg());
    assertNull(dto.getSvgId());
    assertFalse(dto.getAuthRequired());
    assertNull(dto.getSystemID());
    assertEquals(1, dto.getDevice().size());
    assertEquals("m", dto.getDevice().get(0));
  }

  @Test
  public void testFindByBrandEmptyEntity() {
    // arrange
    String brand = "retail";

    FooterMenu entity = new FooterMenu();
    entity.setId(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setUriSmall(StringUtils.EMPTY);
    entity.setUriLarge(StringUtils.EMPTY);
    entity.setInApp(Boolean.FALSE);
    entity.setShowItemFor(StringUtils.EMPTY);
    entity.setWidgetName(StringUtils.EMPTY);
    entity.setSvg(StringUtils.EMPTY);
    entity.setSvgId(StringUtils.EMPTY);
    entity.setAuthRequired(Boolean.FALSE);
    entity.setSystemID(1);
    entity.setDesktop(Boolean.TRUE);
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);

    when(repository.findUniversalRecordsByBrand(brand, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<FooterMenuV3Dto> list = service.find(brand);

    // assert
    assertEquals(1, list.size());

    FooterMenuV3Dto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getTargetUri(), dto.getTarget()); // Empty if entity.getItemType() != "link"
    assertEquals(entity.getLinkTitle(), dto.getTitle());
    assertEquals(entity.getUriSmall(), dto.getImage());
    assertEquals(entity.getUriLarge(), dto.getImageLarge());
    assertNull(dto.getInApp()); // Null if entity.getItemType() != "link"
    assertNull(dto.getWidget()); // Null if entity.getItemType() != "widget"
    assertNull(dto.getSvg()); // Null if entity.getSvg() null or empty
    assertNull(dto.getSvgId()); // Null if entity.getSvgId() null or empty
    assertFalse(dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertEquals(1, dto.getDevice().size());
    assertEquals("d", dto.getDevice().get(0));
  }

  @Test
  public void testFindByBrandMapperCases() {
    // arrange
    String brand = "secondscreen";

    FooterMenu linkEntity = new FooterMenu();
    linkEntity.setItemType("link");
    linkEntity.setTargetUri("home");
    linkEntity.setInApp(Boolean.FALSE);
    linkEntity.setSvg("<svg/>");
    linkEntity.setSvgId("#icon");
    linkEntity.setTablet(Boolean.TRUE);

    FooterMenu widgetEntity = new FooterMenu();
    widgetEntity.setItemType("widget");
    widgetEntity.setWidgetName("clock");
    widgetEntity.setTablet(Boolean.TRUE);
    widgetEntity.setMobile(Boolean.TRUE);
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    when(repository.findUniversalRecordsByBrand(brand, false, pageRequest))
        .thenReturn(Arrays.asList(linkEntity, widgetEntity));

    // act
    List<FooterMenuV3Dto> list = service.find(brand);

    // assert
    assertEquals(2, list.size());

    FooterMenuV3Dto linkDto = list.get(0);
    assertEquals(linkEntity.getTargetUri(), linkDto.getTarget());
    assertFalse(linkDto.getInApp());
    assertNull(linkDto.getWidget());
    assertEquals(linkEntity.getSvg(), linkDto.getSvg());
    assertEquals(linkEntity.getSvgId(), linkDto.getSvgId());
    assertEquals(1, linkDto.getDevice().size());
    assertEquals("t", linkDto.getDevice().get(0));

    FooterMenuV3Dto widgetDto = list.get(1);
    assertEquals(widgetEntity.getWidgetName(), widgetDto.getWidget());
    assertEquals(2, widgetDto.getDevice().size());
    assertArrayEquals(new String[] {"m", "t"}, widgetDto.getDevice().toArray());
  }

  @Test
  public void testFindByBrandReturnsMaxFifteenDistinctMenuItems() {
    // arrange
    String brand = "rcomb";
    long maxDistinctFooterMenuItems = 15;
    int entitiesPerDevice = 10;
    String[] deviceTypes = {"m", "t", "d"};

    ArrayList<FooterMenu> entityList = new ArrayList<>();

    for (int i = 0; i < entitiesPerDevice; i++) {
      FooterMenu mobileEntity = new FooterMenu();
      mobileEntity.setId(String.format("Mobile-%d", i));
      mobileEntity.setMobile(Boolean.TRUE);

      FooterMenu tabletEntity = new FooterMenu();
      tabletEntity.setId(String.format("Tablet-%d", i));
      tabletEntity.setTablet(Boolean.TRUE);

      FooterMenu desktopEntity = new FooterMenu();
      desktopEntity.setId(String.format("Desktop-%d", i));
      desktopEntity.setDesktop(Boolean.TRUE);

      entityList.add(mobileEntity);
      entityList.add(tabletEntity);
      entityList.add(desktopEntity);
    }

    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);

    when(repository.findUniversalRecordsByBrand(brand, false, pageRequest)).thenReturn(entityList);

    // act
    List<FooterMenuV3Dto> list = service.find(brand);

    // assert
    assertEquals(entitiesPerDevice * deviceTypes.length, entityList.size());
    assertEquals(maxDistinctFooterMenuItems, list.size());

    for (int i = 0; i < maxDistinctFooterMenuItems; i++) {
      FooterMenuV3Dto dto = list.get(i);

      assertEquals(entityList.get(i).getId(), dto.getId());
      assertEquals(1, dto.getDevice().size());
      assertEquals(deviceTypes[i % deviceTypes.length], dto.getDevice().get(0));
    }
  }

  @Test
  public void testFindByBrandReturnsMaxFiveAggregatedMenuItems() {
    // arrange
    String brand = "retail";
    long maxAggregatedFooterMenuItems = 5;
    int entitiesCount = 10;

    ArrayList<FooterMenu> entityList = new ArrayList<>();

    for (int i = 0; i < entitiesCount; i++) {
      FooterMenu entity = new FooterMenu();
      entity.setId(String.format("Entity-%d", i));
      entity.setMobile(Boolean.TRUE);
      entity.setTablet(Boolean.TRUE);
      entity.setDesktop(Boolean.TRUE);

      entityList.add(entity);
    }
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    when(repository.findUniversalRecordsByBrand(brand, false, pageRequest)).thenReturn(entityList);

    // act
    List<FooterMenuV3Dto> list = service.find(brand);

    // assert
    assertEquals(entitiesCount, entityList.size());
    assertEquals(maxAggregatedFooterMenuItems, list.size());

    for (int i = 0; i < maxAggregatedFooterMenuItems; i++) {
      FooterMenuV3Dto dto = list.get(i);

      assertEquals(entityList.get(i).getId(), dto.getId());
      assertEquals(3, dto.getDevice().size());
      assertArrayEquals(new String[] {"m", "t", "d"}, dto.getDevice().toArray());
    }
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "ladbrokes";

    FooterMenu entity = new FooterMenu();
    entity.setId("ID");
    entity.setItemType("link");
    entity.setTargetUri("home");
    entity.setLinkTitle("Home");
    entity.setUriSmall("/small.png");
    entity.setUriLarge("/large.png");
    entity.setInApp(Boolean.TRUE);
    entity.setShowItemFor("both");
    entity.setSvg("<symbol></symbol>");
    entity.setSvgId("#icon-home");
    entity.setAuthRequired(Boolean.TRUE);
    entity.setSystemID(1);
    entity.setMobile(Boolean.TRUE);
    entity.setTablet(Boolean.TRUE);
    entity.setDesktop(Boolean.TRUE);
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    when(repository.findUniversalRecordsByBrand(brand, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<FooterMenuV3Dto> list = service.find(brand);

    // assert
    assertEquals(1, list.size());

    FooterMenuV3Dto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getTargetUri(), dto.getTarget());
    assertEquals(entity.getLinkTitle(), dto.getTitle());
    assertEquals(entity.getUriSmall(), dto.getImage());
    assertEquals(entity.getUriLarge(), dto.getImageLarge());
    assertTrue(dto.getInApp());
    assertNull(dto.getWidget());
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertTrue(dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
    assertEquals(3, dto.getDevice().size());
    assertArrayEquals(new String[] {"m", "t", "d"}, dto.getDevice().toArray());
  }

  /** FooterMenuPublicService.find(String brand, String deviceType) test cases */
  @Test
  public void testFindByBrandAndDeviceUninitializedEntity() {
    // arrange
    String brand = "bma";

    FooterMenu entity = new FooterMenu();

    // TODO :not passing the pageable.need to check

    when(repository.findUniversalRecordsByBrand(brand, "mobile", false, pageRequest))
        .thenReturn(Collections.singletonList(entity));

    // act
    DeviceType queryDeviceType = DeviceType.MOBILE;

    int limit = getQueryLimit(brand, queryDeviceType);
    // Check for Segmentation at Device level, if the module is not segmented at
    // device level then
    // need to send Universal records only
    PageRequest pageRequest =
        PageRequest.of(
            0, getQueryLimit(brand, queryDeviceType), SortableService.SORT_BY_SORT_ORDER_ASC);
    List<FooterMenuV2Dto> list =
        service.find(brand, "unknown_device"); // Unknown devices fallback to "mobile"

    // assert
    assertEquals(1, list.size());

    FooterMenuV2Dto dto = list.get(0);
    assertNull(dto.getId());
    assertEquals(StringUtils.EMPTY, dto.getTargetUri());
    assertEquals(StringUtils.EMPTY, dto.getLinkTitle());
    assertEquals(StringUtils.EMPTY, dto.getUriSmall());
    assertNull(dto.getUriMedium());
    assertEquals(StringUtils.EMPTY, dto.getUriLarge());
    assertFalse(dto.getInApp());
    assertNull(dto.getShowItemFor());
    assertFalse(dto.getDisabled());
    assertNull(dto.getSvg());
    assertNull(dto.getSvgId());
    assertFalse(dto.getAuthRequired());
    assertNull(dto.getSystemID());
  }

  @Test
  public void testFindByBrandAndDeviceEmptyEntity() {
    // arrange
    String brand = "retail";
    String deviceType = "desktop";
    PageRequest pageRequest =
        PageRequest.of(
            0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC); // Size Int.Max - for
    // desktop device

    FooterMenu entity = new FooterMenu();
    entity.setId(StringUtils.EMPTY);
    entity.setTargetUri(StringUtils.EMPTY);
    entity.setLinkTitle(StringUtils.EMPTY);
    entity.setUriSmall(StringUtils.EMPTY);
    entity.setUriMedium(StringUtils.EMPTY);
    entity.setUriLarge(StringUtils.EMPTY);
    entity.setInApp(Boolean.FALSE);
    entity.setShowItemFor(StringUtils.EMPTY);
    entity.setDisabled(Boolean.FALSE);
    entity.setSvg(StringUtils.EMPTY);
    entity.setSvgId(StringUtils.EMPTY);
    entity.setAuthRequired(Boolean.FALSE);
    entity.setSystemID(0);

    when(repository.findUniversalRecordsByBrand(brand, deviceType, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<FooterMenuV2Dto> list = service.find(brand, deviceType);

    // assert
    assertEquals(1, list.size());

    FooterMenuV2Dto dto = list.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getUriSmall(), dto.getUriSmall());
    assertEquals(entity.getUriMedium(), dto.getUriMedium());
    assertEquals(entity.getUriLarge(), dto.getUriLarge());
    assertFalse(dto.getInApp());
    assertEquals(entity.getShowItemFor(), dto.getShowItemFor());
    assertFalse(dto.getDisabled());
    assertNull(dto.getSvg()); // Null if entity.getSvg() null or empty
    assertNull(dto.getSvgId()); // Null if entity.getSvgId() null or empty
    assertFalse(dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
  }

  @Test
  public void testFindByBrandAndDevice() {
    // arrange
    String rcombBrand = "rcomb";
    String connectBrand = "connect";
    String deviceType = "mobile";
    PageRequest pageRequest =
        PageRequest.of(
            0, 6, SortableService.SORT_BY_SORT_ORDER_ASC); // Size 6 - for "rcomb" and "connect"
    // brands

    FooterMenu entity = new FooterMenu();
    entity.setId("ID");
    entity.setTargetUri("news");
    entity.setLinkTitle("News");
    entity.setUriSmall("/small.png");
    entity.setUriMedium("/medium.png");
    entity.setUriLarge("/large.png");
    entity.setInApp(Boolean.TRUE);
    entity.setShowItemFor("both");
    entity.setDisabled(Boolean.TRUE);
    entity.setSvg("<svg/>");
    entity.setSvgId("#icon-news");
    entity.setAuthRequired(Boolean.TRUE);
    entity.setSystemID(1);

    // TODO :not passing the pageable.need to check

    when(repository.findUniversalRecordsByBrand(rcombBrand, deviceType, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));
    when(repository.findUniversalRecordsByBrand(connectBrand, deviceType, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<FooterMenuV2Dto> rcombMenuList = service.find(rcombBrand, deviceType);
    List<FooterMenuV2Dto> connectMenuList = service.find(connectBrand, deviceType);

    // assert
    assertEquals(1, rcombMenuList.size());
    assertEquals(1, connectMenuList.size());

    assertEquals(rcombMenuList.get(0), connectMenuList.get(0));

    FooterMenuV2Dto dto = rcombMenuList.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getUriSmall(), dto.getUriSmall());
    assertEquals(entity.getUriMedium(), dto.getUriMedium());
    assertEquals(entity.getUriLarge(), dto.getUriLarge());
    assertTrue(dto.getInApp());
    assertEquals(entity.getShowItemFor(), dto.getShowItemFor());
    assertTrue(dto.getDisabled());
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertTrue(dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
  }

  @Test
  public void testFindByBrandAndDeviceAndUniversal() {
    // arrange
    String brand = "bma";
    String deviceType = "mobile";
    DeviceType queryDeviceType = DeviceType.fromString(deviceType).orElse(DeviceType.MOBILE);
    PageRequest pageRequest =
        PageRequest.of(
            0,
            getQueryLimit(brand, queryDeviceType),
            SortableService.SORT_BY_SORT_ORDER_ASC); // Size 6 - for "rcomb" and "connect"

    FooterMenu entity = new FooterMenu();
    entity.setId("ID");
    entity.setTargetUri("news");
    entity.setLinkTitle("News");
    entity.setUriSmall("/small.png");
    entity.setUriMedium("/medium.png");
    entity.setUriLarge("/large.png");
    entity.setInApp(Boolean.TRUE);
    entity.setShowItemFor("both");
    entity.setDisabled(Boolean.TRUE);
    entity.setSvg("<svg/>");
    entity.setSvgId("#icon-news");
    entity.setAuthRequired(Boolean.TRUE);
    entity.setSystemID(1);

    when(repository.findUniversalRecordsByBrand(brand, deviceType, false, pageRequest))
        .thenReturn(Collections.singletonList(entity));
    // act
    List<FooterMenuV2Dto> menuList = service.find(brand, deviceType);

    // assert
    assertEquals(1, menuList.size());

    FooterMenuV2Dto dto = menuList.get(0);
    assertEquals(entity.getId(), dto.getId());
    assertEquals(entity.getTargetUri(), dto.getTargetUri());
    assertEquals(entity.getLinkTitle(), dto.getLinkTitle());
    assertEquals(entity.getUriSmall(), dto.getUriSmall());
    assertEquals(entity.getUriMedium(), dto.getUriMedium());
    assertEquals(entity.getUriLarge(), dto.getUriLarge());
    assertTrue(dto.getInApp());
    assertEquals(entity.getShowItemFor(), dto.getShowItemFor());
    assertTrue(dto.getDisabled());
    assertEquals(entity.getSvg(), dto.getSvg());
    assertEquals(entity.getSvgId(), dto.getSvgId());
    assertTrue(dto.getAuthRequired());
    assertEquals(entity.getSystemID(), dto.getSystemID());
  }

  private int getQueryLimit(String brand, DeviceType deviceType) {
    int limit = DEFAULT_QUERY_LIMIT;
    if (brand.equals("rcomb") || brand.equals("connect")) {
      limit = RCOMB_CONNECT_QUERY_LIMIT;
    }
    if (deviceType.equals(DeviceType.DESKTOP)) {
      limit = Integer.MAX_VALUE; // return all elements for desktop device
    }
    return limit;
  }
}
