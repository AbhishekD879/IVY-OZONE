package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.NavigationPointArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentedModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.io.IOException;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

@RunWith(MockitoJUnitRunner.class)
public class NavigationPointServiceCacheableTest {

  @Mock private NavigationPointRepository navigationPointRepository;

  @Mock private NavigationPointArchivalRepository navigationPointArchivalRepository;

  @Mock private SegmentRepository segmentRepository;
  @Mock private SegmentArchivalRepository segmentArchivalRepository;

  @Mock private SegmentedModuleRepository segmentedModuleRepository;

  private NavigationPointServiceCacheable navigationPointServiceCacheable;

  @Mock private AutomaticUpdateService automaticUpdateService;

  @Before
  public void init() throws IOException {
    NavigationPointService service =
        new NavigationPointService(
            navigationPointRepository,
            navigationPointArchivalRepository,
            new ModelMapper(),
            new SegmentService(segmentRepository, segmentArchivalRepository, new ModelMapper()),
            new SegmentedModuleSerive(segmentedModuleRepository),
            automaticUpdateService);
    navigationPointServiceCacheable = new NavigationPointServiceCacheable(service);

    when(navigationPointRepository.findUniversalRecordsByBrand(
            "bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/private_api/navigation-point-db-data.json", NavigationPoint.class));

    when(navigationPointRepository.save(Mockito.any(NavigationPoint.class)))
        .thenReturn(getNavigationPoint());
  }

  @Test
  public void testGetNavigationPointByBrandEnabled() {
    List<NavigationPointDto> navigationPointList =
        navigationPointServiceCacheable.getNavigationPointByBrandEnabled("bma");
    Assert.assertNotNull(navigationPointList);
  }

  @Test
  public void testSave() {
    //    Mockito.when(segmentRepository.save(Mockito.any(Segment.class)))
    //        .thenReturn(Segment.builder().id("universal").build());
    NavigationPoint dto = navigationPointServiceCacheable.save(getNavigationPoint());
    Assert.assertNotNull(dto);
  }

  @Test
  public void testDelete() {
    when(navigationPointRepository.findById(Mockito.anyString()))
        .thenReturn(Optional.of(getNavigationPoint()));
    navigationPointServiceCacheable.delete("1");
    Mockito.verify(navigationPointRepository, times(1)).deleteById(Mockito.anyString());
  }

  public NavigationPoint getNavigationPoint() {
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
    return navigationPoint;
  }
}
