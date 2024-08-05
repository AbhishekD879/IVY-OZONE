package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.FooterMenuArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentedModule;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentedModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl.Size;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.data.domain.PageRequest;

@RunWith(MockitoJUnitRunner.class)
public class FooterMenuServiceTest {

  @Mock private FooterMenuRepository repository;

  @Mock private FooterMenuArchivalRepository footerMenuArchivalRepository;

  @Mock private ModelMapper modelMapper;
  @Mock private SegmentRepository segmentRepository;
  @Mock private SegmentArchivalRepository segmentArchivalRepository;

  private SegmentedModuleSerive segmentedModuleSerive;

  private FooterMenuService footerMenuService;

  @Mock private SegmentedModuleRepository segmentedModuleRepository;

  private SegmentService segmentService;

  @Before
  public void setUp() throws Exception {
    segmentedModuleSerive = new SegmentedModuleSerive(segmentedModuleRepository);
    segmentService = new SegmentService(segmentRepository, segmentArchivalRepository, modelMapper);
    footerMenuService =
        new FooterMenuService(
            repository,
            null,
            null,
            ImagePath.builder()
                .smallSize(new Size("4x4"))
                .mediumSize(new Size("4x4"))
                .largeSize(new Size("4x4"))
                .build(),
            modelMapper,
            footerMenuArchivalRepository,
            segmentService,
            segmentedModuleSerive);
  }

  @Test
  public void testFindAllByBrandAndDeviceTypeWithDefaultDeviceType() {
    footerMenuService.findAllByBrandAndDeviceType("bma", "unknownDeviceType");
    verify(repository)
        .findUniversalRecordsByBrand(
            "bma", "mobile", true, PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
  }

  @Test
  public void testFindAllByBrandAndDeviceTypeLimitForRcombBrand() {
    footerMenuService.findAllByBrandAndDeviceType("rcomb", "tablet");
    verify(repository)
        .findUniversalRecordsByBrand(
            "rcomb", "tablet", true, PageRequest.of(0, 6, SortableService.SORT_BY_SORT_ORDER_ASC));
  }

  @Test
  public void testFindAllByBrandAndDeviceTypeLimitForConnectBrand() {
    footerMenuService.findAllByBrandAndDeviceType("connect", "tablet");
    verify(repository)
        .findUniversalRecordsByBrand(
            "connect",
            "tablet",
            true,
            PageRequest.of(0, 6, SortableService.SORT_BY_SORT_ORDER_ASC));
  }

  @Test
  public void testFindAllByBrandAndDeviceTypeLimitForDesktopBrand() {
    footerMenuService.findAllByBrandAndDeviceType("desktop", "desktop");
    verify(repository)
        .findUniversalRecordsByBrand(
            "desktop",
            "desktop",
            true,
            PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC));
  }

  @Test
  public void testFindAllByBrandAndDeviceTypeLimitForBmaBrand() {
    footerMenuService.findAllByBrandAndDeviceType("bma", "tablet");
    verify(repository)
        .findUniversalRecordsByBrand(
            "bma", "tablet", true, PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
  }

  @Test
  public void testgetUniversalwithoutDevice() {

    footerMenuService.findByBrandAndSegmentNameAndDeviceTypeAndIsDisableFalse(
        "bma",
        "Universal",
        Optional.ofNullable(null),
        false,
        PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
    verify(repository, times(1))
        .findUniversalRecordsByBrand(
            "bma", false, PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
  }

  @Test
  public void testgetUniversalwithDeviceType() {

    footerMenuService.findByBrandAndSegmentNameAndDeviceTypeAndIsDisableFalse(
        "bma",
        "Universal",
        Optional.of("mobile"),
        false,
        PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
    verify(repository, times(1))
        .findUniversalRecordsByBrand(
            "bma", "mobile", false, PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
  }

  @Test
  public void testgetSegmentAndUniversalwithoutDevice() {

    footerMenuService.findByBrandAndSegmentNameAndDeviceTypeAndIsDisableFalse(
        "bma",
        "s1",
        Optional.ofNullable(null),
        false,
        PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
    verify(repository, times(1)).findAllByBrandAndSegmentName("bma", Arrays.asList("s1"), false);
  }

  @Test
  public void testgetSegmentAndUniversalwithDeviceType() {

    footerMenuService.findByBrandAndSegmentNameAndDeviceTypeAndIsDisableFalse(
        "bma",
        "s1",
        Optional.of("mobile"),
        false,
        PageRequest.of(0, 5, SortableService.SORT_BY_SORT_ORDER_ASC));
    verify(repository, times(1))
        .findAllByBrandAndSegmentNameAndDeviceType("bma", Arrays.asList("s1"), "mobile", false);
  }

  @Test
  public void testfindAllActiveByBrand() {
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    when(repository.findAllActiveRecordsByBrand("bma", pageRequest))
        .thenReturn(getFooterMenuList());
    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    footerMenuService.findAllActiveByBrand("bma");
    verify(repository, times(1)).findAllActiveRecordsByBrand("bma", pageRequest);
  }

  @Test
  public void testFindAllUniversalByBrandAndDeviceType() {

    List<FooterMenu> footerMenus =
        footerMenuService.findAllByBrandAndDeviceType("bma", "mobile", "Universal");
    Assertions.assertNotNull(footerMenus);
  }

  @Test
  public void testFindAllUniversalByBrand() {
    PageRequest pageRequest =
        PageRequest.of(
            0, getQueryLimit("bma", DeviceType.MOBILE), SortableService.SORT_BY_SORT_ORDER_ASC);

    when(repository.findUniversalRecordsByBrand("bma", "mobile", true, pageRequest))
        .thenReturn(getFooterMenuList());

    footerMenuService.findAllByBrandAndDeviceType("bma", "Universal");

    verify(repository, times(1)).findUniversalRecordsByBrand("bma", "mobile", true, pageRequest);
  }

  @Test
  public void testFindAllSegmentAndUniversalByBrandAndDeviceTypewithSegmentModulefalse() {

    PageRequest pageRequest =
        PageRequest.of(
            0, getQueryLimit("bma", DeviceType.MOBILE), SortableService.SORT_BY_SORT_ORDER_ASC);
    when(segmentedModuleRepository.findByModuleNameAndChannelAndBrand(
            Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(null);
    when(repository.findUniversalRecordsByBrand("bma", "mobile", false, pageRequest))
        .thenReturn(getFooterMenuList());
    footerMenuService.findAllByBrandAndDeviceType("bma", "mobile", "s1");

    verify(repository, times(1)).findUniversalRecordsByBrand("bma", "mobile", false, pageRequest);
  }

  @Test
  public void testfindAllSegmentAndUniversalByBrandAndDeviceTypewithSegmentModuleTrue() {
    when(segmentedModuleRepository.findByModuleNameAndChannelAndBrand(
            Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(getSegmentModuleView());
    when(repository.findAllByBrandAndSegmentNameAndDeviceType(
            "bma", Arrays.asList("s1"), "mobile", false))
        .thenReturn(getSegmentFooterMenuList());
    footerMenuService.findAllByBrandAndDeviceType("bma", "mobile", "s1");

    verify(repository, times(1))
        .findAllByBrandAndSegmentNameAndDeviceType("bma", Arrays.asList("s1"), "mobile", false);
  }

  @Test
  public void testFindFiveSegmentAndUniversalByBrandAndDeviceTypewithSegmentModuleTrue() {
    when(segmentedModuleRepository.findByModuleNameAndChannelAndBrand(
            Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(getSegmentModuleView());
    when(repository.findAllByBrandAndSegmentNameAndDeviceType(
            "bma", Arrays.asList("s1"), "mobile", false))
        .thenReturn(getFiveSegmentFooterMenuList());
    footerMenuService.findAllByBrandAndDeviceType("bma", "mobile", "s1");

    verify(repository, times(1))
        .findAllByBrandAndSegmentNameAndDeviceType("bma", Arrays.asList("s1"), "mobile", false);
  }

  private List<SegmentedModule> getSegmentModuleView() {
    List<SegmentedModule> listModule = new ArrayList<>();
    SegmentedModule module = new SegmentedModule();
    listModule.add(module);
    return listModule;
  }

  private List<Segment> getSegments() {
    List<Segment> segList = new ArrayList<>();
    segList.add(Segment.builder().segmentName("s1").brand("bma").build());
    segList.add(Segment.builder().segmentName("s2").brand("bma").build());
    segList.add(Segment.builder().segmentName("s3").brand("bma").build());
    segList.add(Segment.builder().segmentName("s4").brand("bma").build());
    segList.add(Segment.builder().segmentName("Universal").brand("bma").build());

    return segList;
  }

  public static FooterMenu createFooterMenu(String id, boolean value, String segmentName) {
    FooterMenu footerMenu = new FooterMenu();
    footerMenu.setId(id);
    footerMenu.setWidgetName("football");
    footerMenu.setUniversalSegment(value);
    footerMenu.setSegmentReferences(getSegmentReference(segmentName));
    footerMenu.setBrand("coral");
    footerMenu.setSortOrder(5 + Math.random());
    footerMenu.setLinkTitleBrand("coral");
    footerMenu.setLinkTitle("image1");

    return footerMenu;
  }

  public static List<SegmentReference> getSegmentReference(String segmentName) {
    List<SegmentReference> segmentReferences = new ArrayList<>();
    segmentReferences.add(getSegmentReference(segmentName, "10", 1 + Math.random()));
    segmentReferences.add(getSegmentReference(segmentName, "10", 2 + Math.random()));
    return segmentReferences;
  }

  private static SegmentReference getSegmentReference(
      String segmentName, String pageRefId, double sortOrder) {
    return SegmentReference.builder()
        .segmentName(segmentName)
        .id("1")
        .sortOrder(sortOrder)
        .pageRefId(pageRefId)
        .build();
  }

  private static List<FooterMenu> getFooterMenuList() {
    List<FooterMenu> FooterMenuList = new ArrayList<>();
    FooterMenuList.add(createFooterMenu("1", true, "universal"));
    return FooterMenuList;
  }

  private static List<FooterMenu> getSegmentFooterMenuList() {
    List<FooterMenu> FooterMenuList = new ArrayList<>();
    FooterMenuList.add(createFooterMenu("1", false, "s1"));
    return FooterMenuList;
  }

  private static List<FooterMenu> getFiveSegmentFooterMenuList() {
    List<FooterMenu> FooterMenuList = new ArrayList<>();
    FooterMenuList.add(createFooterMenu("1", false, "s1"));
    FooterMenuList.add(createFooterMenu("2", false, "s1"));
    FooterMenuList.add(createFooterMenu("3", false, "s1"));
    FooterMenuList.add(createFooterMenu("4", false, "s1"));
    FooterMenuList.add(createFooterMenu("5", false, "s1"));
    FooterMenuList.add(createFooterMenu("6", false, "s1"));

    return FooterMenuList;
  }

  private static final int DEFAULT_QUERY_LIMIT = 5;
  private static final int RCOMB_CONNECT_QUERY_LIMIT = 6;

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
