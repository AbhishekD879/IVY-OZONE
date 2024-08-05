package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl.SORT_BY_DISPLAY_ORDER_ASC;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.EventsSelectionSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.Visibility;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

@RunWith(MockitoJUnitRunner.class)
public class HomeModuleServiceImplTest {
  @Mock private HomeModuleRepository repository;
  @Mock private EventHubService hubService;
  private HomeModuleServiceImpl homeModuleService;

  @Spy private ModelMapper modelMapper;
  HomeModuleServiceImpl homemoduleService;
  @Mock private SegmentedModuleSerive segmentedModuleSerive;

  HomeModuleArchivalRepository homeModuleArchivalRepository;
  @Mock SegmentService segmentService;

  @Before
  public void setUp() {
    homeModuleService =
        new HomeModuleServiceImpl(
            repository, homeModuleArchivalRepository, modelMapper, segmentService, hubService);
  }

  @Test
  public void testFindAllActive() {
    homeModuleService.findByActiveState(true);
    verify(repository, times(1)).findAllActive(any());
    verify(repository, times(0)).findAllInactive(any());
  }

  @Test
  public void testFindAllInactive() {
    homeModuleService.findByActiveState(false);
    verify(repository, times(0)).findAllActive(any());
    verify(repository, times(1)).findAllInactive(any());
  }

  @Test(expected = BadRequestException.class)
  public void testExceptionWasThrownByPrepareToSaveHeroGroupedModule() {
    HomeModule homeModule = createValidHomeModule();
    homeModule.setGroupedBySport(true);
    homeModule.setHero(true);

    homeModuleService.prepareModelBeforeSave(homeModule);
  }

  @Test
  public void testFindByBrand() {
    homeModuleService.findByBrand("bma");
    verify(repository, times(1)).findByBrand(any(), any());
  }

  @Test
  public void testFindByActiveStateAndPublishToChannelByUniversalSegmantName() {
    HomeModule homeModule = createValidHomeModule();
    when(repository.findAllUniversalActiveAndPublishToChannel(
            any(Instant.class), any(String.class), eq(true), eq(SORT_BY_DISPLAY_ORDER_ASC)))
        .thenReturn(Arrays.asList(homeModule));
    homeModuleService.findByActiveStateAndPublishToChannelBySegmantName(true, "bma", "Universal");
    verify(repository, times(1))
        .findAllUniversalActiveAndPublishToChannel(
            any(Instant.class), any(String.class), eq(true), eq(SORT_BY_DISPLAY_ORDER_ASC));
  }

  @Test
  public void testFindByInActiveStateAndPublishToChannelByUniversalSegmantName() {
    HomeModule homeModule = createValidHomeModule();
    when(repository.findAllUniversalInActiveAndPublishToChannel(
            any(Instant.class), any(String.class), eq(false), eq(SORT_BY_DISPLAY_ORDER_ASC)))
        .thenReturn(Arrays.asList(homeModule));
    homeModuleService.findByActiveStateAndPublishToChannelBySegmantName(false, "bma", "Universal");
    verify(repository, times(1))
        .findAllUniversalInActiveAndPublishToChannel(
            any(Instant.class), any(String.class), eq(false), eq(SORT_BY_DISPLAY_ORDER_ASC));
  }

  @Test
  public void testFindByInActiveStateAndPublishToChannelBySegmantName() {
    HomeModule homeModule = createValidHomeModule();
    when(repository.findAllUniversalAndSegmentInActiveAndPublishToChannel(
            any(Instant.class), any(String.class), eq(false), any(), eq(SORT_BY_DISPLAY_ORDER_ASC)))
        .thenReturn(Arrays.asList(homeModule));
    homeModuleService.findByActiveStateAndPublishToChannelBySegmantName(false, "bma", "s1");
    verify(repository, times(1))
        .findAllUniversalAndSegmentInActiveAndPublishToChannel(
            any(Instant.class), any(String.class), eq(false), any(), eq(SORT_BY_DISPLAY_ORDER_ASC));
  }

  @Test
  public void testFindByActiveStateAndPublishToChannelBySegmantName() {
    HomeModule homeModule = createValidHomeModule();
    List<SegmentReference> segRefList = new ArrayList<>();
    SegmentReference segmentReference = new SegmentReference();
    segmentReference.setSegmentName("segment-one");
    segmentReference.setSortOrder(new Double(1));
    segRefList.add(segmentReference);
    homeModule.setSegmentReferences(segRefList);
    when(repository.findAllPublishToChannelAndSegmentNameAndIsActive(
            any(Instant.class),
            any(String.class),
            any(List.class),
            eq(true),
            eq(SORT_BY_DISPLAY_ORDER_ASC)))
        .thenReturn(Arrays.asList(homeModule));
    homeModuleService.findByActiveStateAndPublishToChannelBySegmantName(true, "bma", "segment-one");
    verify(repository, times(1))
        .findAllPublishToChannelAndSegmentNameAndIsActive(
            any(Instant.class),
            any(String.class),
            any(List.class),
            eq(true),
            eq(SORT_BY_DISPLAY_ORDER_ASC));
  }

  @Test
  public void testFindAllForUniversalSegmant() {
    homeModuleService.findAll("bma", null, "", "Universal");
    verify(repository, times(1))
        .findAllUniversalByBrandAndPageIdAndPageType(any(), any(), any(), any());
  }

  @Test
  public void testFindAllForSegmant() {
    HomeModule homeModule = createValidHomeModule();
    List<SegmentReference> segRefList = new ArrayList<>();
    SegmentReference segmentReference = new SegmentReference();
    segmentReference.setSegmentName("segment-one");
    segmentReference.setSortOrder(new Double(1));
    segRefList.add(segmentReference);
    homeModule.setSegmentReferences(segRefList);
    when(repository.findAllSegmentByBrandAndPageIdAndPageType(
            any(String.class),
            any(PageType.class),
            any(String.class),
            any(String.class),
            eq(SORT_BY_DISPLAY_ORDER_ASC)))
        .thenReturn(Arrays.asList(homeModule));
    homeModuleService.findAll("bma", PageType.sport, "", "segment-one");
    verify(repository, times(1))
        .findAllSegmentByBrandAndPageIdAndPageType(
            any(String.class),
            any(PageType.class),
            any(String.class),
            any(String.class),
            eq(SORT_BY_DISPLAY_ORDER_ASC));
  }

  @Test
  public void testFindByActiveStateAndPublishToChannelAndApplyUniversalSegments() {
    homeModuleService.findByActiveStateAndPublishToChannelAndApplyUniversalSegments(true, "bma");
    verify(repository, times(1))
        .findAllActiveAndPublishToChannelAndApplyUniversalSegments(any(), any(), any());
  }

  @Test
  public void testFindByInActiveStateAndPublishToChannelAndApplyUniversalSegments() {
    homeModuleService.findByActiveStateAndPublishToChannelAndApplyUniversalSegments(false, "bma");
    verify(repository, times(1))
        .findAllInactiveAndPublishToChannelAndApplyUniversalSegments(any(), any(), any());
  }

  public HomeModule createValidHomeModule() {
    HomeModule homeModule = new HomeModule();

    homeModule.setTitle("HM Title");
    homeModule.setPublishToChannels(Collections.singletonList("bma"));

    DataSelection dataSelection = new DataSelection();
    dataSelection.setSelectionType("Type");
    dataSelection.setSelectionId("12345");
    homeModule.setDataSelection(dataSelection);

    Instant from = Instant.now();
    Instant to = from.plus(Duration.ofDays(3));

    EventsSelectionSetting eventsSelectionSetting = new EventsSelectionSetting();
    eventsSelectionSetting.setFrom(from);
    eventsSelectionSetting.setTo(to);
    homeModule.setEventsSelectionSettings(eventsSelectionSetting);

    Visibility visibility = new Visibility();
    visibility.setDisplayFrom(from);
    visibility.setDisplayTo(to);
    homeModule.setVisibility(visibility);
    return homeModule;
  }
}
