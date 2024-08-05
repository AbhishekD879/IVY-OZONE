package com.ladbrokescoral.oxygen.cms.api.service;

import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HighlightCarouselArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.HighlightCarouselArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.repository.HighlightCarouselRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

@RunWith(MockitoJUnitRunner.class)
public class HighlightCarouselServiceTest {

  @Mock private HighlightCarouselRepository highlightCarouselRepository;

  @Mock private SiteServerApi siteServerApi;

  @Mock private SiteServeApiProvider siteServeApiProvider;

  @Mock private SegmentedService<?> segmentedService;

  @Mock private SegmentService segmentService;

  @Mock private ModelMapper modelMapper;
  @Mock private HighlightCarouselArchiveRepository highlightCarouselArchiveRepository;
  @Mock private CompetitionModuleService competitionModuleService;
  @InjectMocks private HighlightCarouselService highlightCarouselService;

  @Before
  public void setUp() {
    when(siteServeApiProvider.api("bma")).thenReturn(siteServerApi);
    when(siteServerApi.getEvent(any(), eq(true))).thenReturn(Optional.of(new Event()));
    when(siteServerApi.getClassToSubTypeForType(anyString(), any()))
        .thenReturn(Optional.of(Collections.singletonList(new Category())));
    when(siteServerApi.getClassToSubTypeForType(anyList(), any()))
        .thenReturn(Optional.of(Collections.singletonList(new Category())));
    when(highlightCarouselRepository.save(any())).thenReturn(createHighlightCarousel());
  }

  @Test
  public void saveWhileOnlyEventsIsSet() {
    HighlightCarousel highlightCarousel = createHighlightCarousel();
    Mockito.when(modelMapper.map(any(), any())).thenReturn(crateArchivalEntity());
    highlightCarouselService.save(highlightCarousel);
    verify(highlightCarouselRepository).save(highlightCarousel);
  }

  @Test(expected = IllegalArgumentException.class)
  public void saveEmptyEventId() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();

    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setEvents(Arrays.asList("event-1", "event-2", ""));
    highlightCarousel.setSportId(16);
    highlightCarousel.setBrand("bma");
    highlightCarouselService.save(highlightCarousel);
    verify(highlightCarouselRepository).save(highlightCarousel);
  }

  @Test
  public void saveWhileOnlyTypeIdIsSet() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();

    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setSportId(16);
    highlightCarousel.setTypeId(4);
    highlightCarousel.setBrand("bma");
    Mockito.when(modelMapper.map(any(), any())).thenReturn(crateArchivalEntity());
    highlightCarouselService.save(highlightCarousel);
    verify(highlightCarouselRepository).save(highlightCarousel);
  }

  @Test
  public void saveWhileOnlyTypeIdsIsSet() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();

    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setSportId(16);
    highlightCarousel.setTypeIds(Arrays.asList("442", "441"));
    highlightCarousel.setBrand("bma");
    Mockito.when(modelMapper.map(any(), any())).thenReturn(crateArchivalEntity());
    highlightCarouselService.save(highlightCarousel);
    verify(highlightCarouselRepository).save(highlightCarousel);
  }

  @Test
  public void saveWhileBothTypeIdAndEventsAreSet() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();
    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setEvents(Arrays.asList("event-1", "event-2"));
    highlightCarousel.setSportId(16);
    highlightCarousel.setTypeId(4);
    highlightCarousel.setBrand("bma");
    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "HighlightCarousel.typedId and HighlightCarousel.typedIds  must be null when HighlightCarousel.events is specified");
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void saveWhileBothTypeIdsAndEventsAreSet() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();
    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setEvents(Arrays.asList("event-1", "event-2"));
    highlightCarousel.setSportId(16);
    highlightCarousel.setTypeIds(Arrays.asList("442", "441"));
    highlightCarousel.setBrand("bma");
    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "HighlightCarousel.typedId and HighlightCarousel.typedIds  must be null when HighlightCarousel.events is specified");
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void saveWhileBothTypeIdAndTypeIdsAreSet() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();
    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setTypeId(445);
    highlightCarousel.setSportId(16);
    highlightCarousel.setTypeIds(Arrays.asList("442", "441"));
    highlightCarousel.setBrand("bma");
    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Both HighlightCarousel.typedId and HighlightCarousel.typedIds must not be set at same time");
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void saveWhileNeitherTypeIdNorEventsNorTypedsAreSet() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();
    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setSportId(16);
    highlightCarousel.setBrand("bma");
    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Either HighlightCarousel.typedId or HighlightCarousel.typedIds or HighlightCarousel.events must be set");
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void saveWhileTypeIdIsIncorrect() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();

    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setSportId(16);
    highlightCarousel.setTypeId(4);
    highlightCarousel.setBrand("bma");

    when(siteServerApi.getClassToSubTypeForType(anyString(), any()))
        .thenReturn(Optional.of(Collections.emptyList()));

    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Cannot save Highlights Carousel since Type ID/Type IDs doesn't exist");

    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void saveWhileTypeIdsIsIncorrect() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();

    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setSportId(16);
    highlightCarousel.setTypeIds(Arrays.asList("442", "441"));
    highlightCarousel.setBrand("bma");

    when(siteServerApi.getClassToSubTypeForType(anyList(), any()))
        .thenReturn(Optional.of(Collections.emptyList()));

    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Cannot save Highlights Carousel since Type ID/Type IDs doesn't exist");

    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void saveWhileSomeEventsIdsIncorrect() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();

    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setEvents(Arrays.asList("77", "98", "11", "32"));
    highlightCarousel.setSportId(16);
    highlightCarousel.setBrand("bma");

    when(siteServerApi.getEvent("77", true)).thenReturn(Optional.empty());

    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Cannot save Highlights Carousel since Event ID '77' doesn't exist");

    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void testTypeIdperSegment() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();

    highlightCarousel.setExclusionList(Arrays.asList("s2,s10"));

    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s4")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertTrue(result);
  }

  @Test
  public void testUniqueTypeIdperSegment() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(true);
    highlightCarousel.setExclusionList(Arrays.asList("s2,s10"));

    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertTrue(result);
  }

  @Test
  public void testTypeIdperSegmentForUniversalSave() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setExclusionList(new ArrayList<>());
    highlightCarousel.setEvents(new ArrayList<>());
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.save(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Type ID: 421 is already used for same period. Please amend your schedule.");
  }

  @Test
  public void testTypeIdperSegmentForUniversal() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setExclusionList(new ArrayList<>());
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);
    assertTrue(result);
  }

  @Test
  public void testTypeIdperSegmentForsegmentedmatchedData() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6"));
    highlightCarousel.setDisplayFrom(Instant.now().plus(10, ChronoUnit.DAYS));
    highlightCarousel.setDisplayTo(Instant.now().plus(11, ChronoUnit.DAYS));
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));

    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testTypeIdperSegmentForsegmentedUnmatchedData() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6"));
    highlightCarousel.setDisplayFrom(Instant.now().plus(4, ChronoUnit.DAYS));
    highlightCarousel.setDisplayTo(Instant.now().plus(5, ChronoUnit.DAYS));
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));

    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testTypeIdperSegmentForsegmented() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6"));

    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testTypeIdperSegmentForsegmentedemptyList() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6"));

    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(new ArrayList<>());

    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testTypeIdperSegmentForsegmentedFalse() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6", "s2"));

    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertTrue(result);
  }

  @Test
  public void testTypeIdperSegmentForExclusiveList() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6", "s2"));
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertTrue(result);
  }

  @Test
  public void testTypeIdperSegmentForExclusiveListTrue() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(Arrays.asList("s4")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testTypeIdperSegmentForrepoExclusiveListempty() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(new ArrayList<>()));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertTrue(result);
  }

  @Test
  public void testUpdateTypeIdperSegment() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s3"));
    highlightCarousel.setId("test");
    when(highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            421, "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(Arrays.asList("s4")));
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testUpdateTypeIdperSegmentisPage0() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s3"));
    highlightCarousel.setId("test");
    highlightCarousel.setPageType(PageType.eventhub);
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testUpdateTypeIdperSegmentwithEventHub() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s3"));
    highlightCarousel.setId("test");
    highlightCarousel.setPageId("22");
    highlightCarousel.setPageType(PageType.eventhub);
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testUpdateTypeIdperSegmentNotHomePage() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s3"));
    highlightCarousel.setId("test");
    highlightCarousel.setPageId("22");
    boolean result = highlightCarouselService.isUniqueTypeIdPerSegment(highlightCarousel);

    assertFalse(result);
  }

  @Test
  public void testEventIdperSegment() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();

    highlightCarousel.setExclusionList(Arrays.asList("s2,s10"));

    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s4")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Event IDs: event-1 are already used for same period. Please amend your schedule.");
  }

  @Test
  public void testUniqueEventIdperSegment() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(true);
    highlightCarousel.setExclusionList(Arrays.asList("s2,s10"));

    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Event IDs: event-1 are already used for same period. Please amend your schedule.");
  }

  @Test
  public void testEventIdperSegmentForUniversal() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setExclusionList(new ArrayList<>());
    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Event IDs: event-1 are already used for same period. Please amend your schedule.");
  }

  @Test
  public void testEventIdperSegmentForsegmentedFalse() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6", "s2"));

    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Event IDs: event-1 are already used for same period. Please amend your schedule.");
  }

  @Test
  public void testEventIdperSegmentForExclusiveList() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4", "s5", "s6", "s2"));
    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Event IDs: event-1 are already used for same period. Please amend your schedule.");
  }

  @Test
  public void testEventIdperSegmentForExclusiveListTrue() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(Arrays.asList("s4")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel);
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void testUpdateEventIdperSegment() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    highlightCarousel.setId("test");
    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(Arrays.asList("s4")));
    highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel);
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void testUpdateEventIdperSegmentNotPage0() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    highlightCarousel.setId("test");
    highlightCarousel.setPageId("16");
    highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel);
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void testUpdateEventIdperSegmentNotPage0andSport() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    highlightCarousel.setId("test");
    highlightCarousel.setPageId("16");
    highlightCarousel.setPageType(PageType.eventhub);

    highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel);
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void testUpdateEventIdperSegmentNotSport() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    highlightCarousel.setId("test");
    highlightCarousel.setPageType(PageType.eventhub);
    highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel);
    verify(highlightCarouselRepository, never()).save(highlightCarousel);
  }

  @Test
  public void testEventIdperSegmentForrepoExclusiveListempty() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(new ArrayList<>()));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Event IDs: event-1 are already used for same period. Please amend your schedule.");
  }

  @Test
  public void testEventId() {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(Arrays.asList("s4"));
    when(highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            "event-1", "bma", PageType.sport, "0"))
        .thenReturn(getSegmentedHCList(new ArrayList<>()));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    assertThatThrownBy(() -> highlightCarouselService.isUniqueEventIdsPerSegment(highlightCarousel))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage(
            "Event IDs: event-1 are already used for same period. Please amend your schedule.");
  }

  @Test
  public void testRemoveHighLightCarouselIdsFromCompetitionModules()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    when(competitionModuleService.findCompetitionModulesByType(
            CompetitionModuleType.HIGHLIGHT_CAROUSEL))
        .thenReturn(getCompModulesList());
    Method method =
        HighlightCarouselService.class.getDeclaredMethod(
            "removeHighLightCarouselIdsFromCompetitionModules", String.class);
    method.setAccessible(true);
    method.invoke(highlightCarouselService, "2");
    verify(competitionModuleService, times(2)).save((CompetitionModule) Mockito.any());
  }

  private List<CompetitionModule> getCompModulesList() {
    CompetitionModule competitionModule1 = new CompetitionModule();
    competitionModule1.getHighlightCarousels().addAll(Arrays.asList("1", "2", "3"));
    CompetitionModule competitionModule2 = new CompetitionModule();
    competitionModule2.getHighlightCarousels().addAll(Arrays.asList("2", "3", "4"));
    List<CompetitionModule> competitionModules = new ArrayList<>();
    competitionModules.add(competitionModule1);
    competitionModules.add(competitionModule2);
    return competitionModules;
  }

  private List<HighlightCarousel> getHCList(List<String> segments) {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setId("test");
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setInclusionList(segments);

    return Arrays.asList(highlightCarousel);
  }

  private List<HighlightCarousel> getSegmentedHCList(List<String> segments) {
    HighlightCarousel highlightCarousel = createHighlightCarouselwithSegment();
    highlightCarousel.setId("test");
    highlightCarousel.setUniversalSegment(true);
    highlightCarousel.setExclusionList(segments);
    return Arrays.asList(highlightCarousel);
  }

  private HighlightCarousel createHighlightCarousel() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();
    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setEvents(Arrays.asList("event-1", "event-2"));
    highlightCarousel.setSportId(16);
    highlightCarousel.setBrand("bma");
    highlightCarousel.setDisplayFrom(Instant.now());
    highlightCarousel.setDisplayTo(Instant.now().plus(3, ChronoUnit.DAYS));
    return highlightCarousel;
  }

  private HighlightCarouselArchive crateArchivalEntity() {
    HighlightCarouselArchive archive = new HighlightCarouselArchive();
    archive.setId(UUID.randomUUID().toString());
    archive.setEvents(Arrays.asList("event-1", "event-2"));
    archive.setSportId(16);
    archive.setBrand("bma");
    archive.setArchivalId("1");
    archive.setDeleted(false);
    return archive;
  }

  private HighlightCarousel createHighlightCarouselwithSegment() {
    HighlightCarousel highlightCarousel = new HighlightCarousel();
    highlightCarousel.setId(UUID.randomUUID().toString());
    highlightCarousel.setEvents(Arrays.asList("event-1", "event-2"));
    highlightCarousel.setSportId(16);
    highlightCarousel.setBrand("bma");
    highlightCarousel.setTypeId(421);
    highlightCarousel.setUniversalSegment(true);
    highlightCarousel.setPageId("0");
    highlightCarousel.setPageType(PageType.sport);
    highlightCarousel.setDisplayFrom(Instant.now().plus(5, ChronoUnit.DAYS));
    highlightCarousel.setDisplayTo(Instant.now().plus(6, ChronoUnit.DAYS));
    return highlightCarousel;
  }
}
