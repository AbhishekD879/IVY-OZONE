package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.NavigationPointArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.NavigationPointArchive;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.PageRequest;

@RunWith(MockitoJUnitRunner.class)
@Import(ModelMapperConfig.class)
public class NavigationPointServiceTest {
  @Mock NavigationPointRepository repository;
  @Spy private ModelMapper modelMapper;
  NavigationPointService navigationPointService;
  @Mock private SegmentedModuleSerive segmentedModuleSerive;

  NavigationPointArchivalRepository navigationPointArchivalRepository;
  @Mock SegmentService segmentService;

  @Mock AutomaticUpdateService automaticUpdateService;

  @Before
  public void setUp() throws Exception {
    navigationPointService =
        new NavigationPointService(
            repository,
            navigationPointArchivalRepository,
            modelMapper,
            segmentService,
            segmentedModuleSerive,
            automaticUpdateService);
  }

  @Test
  public void testGetNavigationPointByBrandEnabled() throws Exception {
    when(repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/private_api/navigation-point-db-data.json", NavigationPoint.class));
    List<NavigationPointDto> bma = navigationPointService.getNavigationPointByBrandEnabled("bma");
    List<NavigationPointDto> expected =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/navigationPointsPublic.json", NavigationPointDto.class);
    Assert.assertEquals(
        "Error during processing navigation points",
        TestUtil.serializeWithJackson(expected),
        TestUtil.serializeWithJackson(bma));
  }

  @Test
  public void testGetNavigationPointByBrandEnabledAndDeviceTypeNull() throws Exception {
    when(repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/private_api/navigation-point-db-data.json", NavigationPoint.class));
    List<NavigationPointDto> bma =
        navigationPointService.getNavigationPointByBrandEnabled(
            "bma", SegmentConstants.UNIVERSAL, null);
    List<NavigationPointDto> expected =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/navigationPointsPublic.json", NavigationPointDto.class);
    Assert.assertEquals(
        "Error during processing navigation points",
        TestUtil.serializeWithJackson(expected),
        TestUtil.serializeWithJackson(bma));
  }

  @Test
  public void testGetNavigationPointByBrandEnabledAndDeviceTypeAndUniversalSegment()
      throws Exception {
    when(repository.findUniversalRecordsByBrand(
            "bma", AbstractSegmentService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/private_api/navigation-point-db-data.json", NavigationPoint.class));

    List<NavigationPointDto> bma =
        navigationPointService.getNavigationPointByBrandEnabled(
            "bma", SegmentConstants.UNIVERSAL, DeviceType.MOBILE);
    List<NavigationPointDto> expected =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/navigationPointsPublic.json", NavigationPointDto.class);
    Assert.assertEquals(
        "Error during processing navigation points",
        TestUtil.serializeWithJackson(expected),
        TestUtil.serializeWithJackson(bma));
  }

  @Test
  public void testFindAllActiveByBrand() throws Exception {
    String brand = "bma";
    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    NavigationPoint navigationPoint = new NavigationPoint();
    navigationPoint.setBrand(brand);
    navigationPoint.setTargetUri("/abc.png");
    navigationPoint.setDescription(brand);
    navigationPoint.setTitle(brand);
    navigationPoint.setId("12345");
    navigationPoint.setEnabled(Boolean.TRUE);
    navigationPoint.setUpdatedByUserName("abcd");
    navigationPoint.setUniversalSegment(Boolean.TRUE);
    navigationPoint.setArchivalId("12345");
    when(repository.findAllActiveRecordsByBrand(brand, pageRequest))
        .thenReturn(Collections.singletonList(navigationPoint));
    List<NavigationPointSegmentedDto> list = navigationPointService.findAllActiveByBrand(brand);
    assertEquals(1, list.size());
    NavigationPointSegmentedDto dto = list.get(0);
    assertEquals(navigationPoint.getId(), dto.getId());
    assertEquals(navigationPoint.getBrand(), dto.getBrand());
    assertEquals(navigationPoint.getTargetUri(), dto.getTargetUri());
    assertEquals(navigationPoint.getDescription(), dto.getDescription());
    assertEquals(navigationPoint.getTitle(), dto.getTitle());
  }

  @Test
  public void testPrepareArchivalEntity() throws Exception {
    NavigationPoint navigationPoint = new NavigationPoint();
    String brand = "bma";
    navigationPoint.setBrand(brand);
    navigationPoint.setTargetUri("/abc.png");
    navigationPoint.setDescription(brand);
    navigationPoint.setTitle(brand);
    navigationPoint.setId("12345");
    navigationPoint.setEnabled(Boolean.TRUE);
    navigationPoint.setUpdatedByUserName("abcd");
    navigationPoint.setUniversalSegment(Boolean.TRUE);
    navigationPoint.setArchivalId("12345");
    NavigationPointService navigationPointService =
        new NavigationPointService(
            repository,
            navigationPointArchivalRepository,
            new ModelMapper(),
            segmentService,
            segmentedModuleSerive,
            automaticUpdateService);
    NavigationPointArchive navigationPointArchive =
        navigationPointService.prepareArchivalEntity(navigationPoint);
    Assert.assertNotNull(navigationPointArchive);
  }

  @Test
  public void testGetNavigationPointByBrandEnabledAndDeviceTypeAndSegment() throws Exception {
    when(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/private_api/navigation-point-segmented-db-data.json",
                NavigationPoint.class));
    when(repository.findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
            "bma",
            Arrays.asList("segment1"),
            Arrays.asList("5ae1ac12964c3859291eee6b"),
            AbstractSegmentService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.emptyList());
    when(segmentedModuleSerive.isSegmentedModule(
            NavigationPoint.class.getSimpleName(), DeviceType.MOBILE, "bma"))
        .thenReturn(true);
    List<NavigationPointDto> bma =
        navigationPointService.getNavigationPointByBrandEnabled(
            "bma", "segment1", DeviceType.MOBILE);
    List<NavigationPointDto> expected =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/navigationPointsPublic-with-segment.json",
            NavigationPointDto.class);
    Assert.assertEquals(
        "Error during processing navigation points",
        TestUtil.serializeWithJackson(expected),
        TestUtil.serializeWithJackson(bma));
  }

  @Test
  public void testGetNavigationPointByBrandEnabledAndDeviceTypeAndSegmentAndSegmentModuleFalse()
      throws Exception {
    when(segmentedModuleSerive.isSegmentedModule(
            NavigationPoint.class.getSimpleName(), DeviceType.MOBILE, "bma"))
        .thenReturn(false);
    List<NavigationPointDto> navigationPoints =
        navigationPointService.getNavigationPointByBrandEnabled(
            "bma", "segment1", DeviceType.MOBILE);
    assertNotNull(navigationPoints);
  }
}
