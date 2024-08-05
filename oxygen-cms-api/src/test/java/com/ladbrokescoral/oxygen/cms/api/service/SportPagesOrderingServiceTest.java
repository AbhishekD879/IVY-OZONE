package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetMongoRepository;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.Silent.class)
@SuppressWarnings("java:S2699")
public class SportPagesOrderingServiceTest {

  @InjectMocks private SportPagesOrderingService orderingService;

  @Mock private SurfaceBetMongoRepository surfaceBetMongoRepository;
  private static final int EXISTS_SELECTION_ID = 907016395;
  private static final String TEST_PAGE_ID = "test";

  @Before
  public void init() {
    orderingService = new SportPagesOrderingService(surfaceBetMongoRepository);
  }

  @Test(expected = IllegalArgumentException.class)
  public void emptyIdOrderDto() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    orderingService.dragAndDropOrder(orderDto);
  }

  @Test(expected = IllegalArgumentException.class)
  public void orderEmptyOrderDto() {
    final OrderDto orderDto =
        OrderDto.builder().id("1").pageId("16").pageType("sport").segmentName("segment1").build();
    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void reorderList() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void reorderListAllEmpty() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void reorderListAllEmptyFalse() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    // when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void reorderListAllSameSortOrder() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void reorderListAllSameSortOrderFalse() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(3.0)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void buildCurrentElementNewSortOrder() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(1.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(3.0)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(4.0)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void buildCurrentElementNewSortOrderWithPrevAndNextSortOrderNull() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();

    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(1.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(3.0)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(null)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void buildCurrentElementNewSortOrderWithPrevAndNextSortOrderNull22() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();

    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(1.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(1.0)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(3.0)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(5.0)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void buildCurrentElementNewSortOrderWithPrevAndNextSortOrderNullFalse() {
    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("16")
                .sortOrder(null)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(3.0)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(4.0)
                .build());

    when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    orderingService.dragAndDropOrder(orderDto);
  }

  @Test
  public void incrementSortOrderForSportPages() {

    final SurfaceBet surfaceBet1 = createValidSurfaceBetForFootball();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(1.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBetForFootball();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final SurfaceBet surfaceBet3 = createValidSurfaceBetForFootball();
    surfaceBet3.setId("3");
    surfaceBet3
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(3.0)
                .build());

    final SurfaceBet surfaceBet4 = createValidSurfaceBetForFootball();
    surfaceBet4.setId("4");
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(4.0)
                .build());

    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findTheMaxSortOrderOfThePage(PageType.sport.name(), "16"))
        .thenReturn(surfaceBets);

    orderingService.incrementSortOrderForSportPages(surfaceBet1);
  }

  @Test
  public void incrementSortOrderForSportPagesFalseCase() {

    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("16")
                .sortOrder(1.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("6")
                .sortOrder(2.0)
                .build());

    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet1, surfaceBet2).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findTheMaxSortOrderOfThePage(PageType.sport.name(), "16"))
        .thenReturn(surfaceBets);

    orderingService.incrementSortOrderForSportPages(surfaceBet1);
  }

  @Test
  public void buildCurrentElementNewSortOrderWithPrevAndNextElementEmpty() {

    final Optional<Double> prevElementSortOrder = Optional.empty();
    final Optional<Double> nexElementSortOrder = Optional.empty();
    final Optional<Double> currentElementSortOrder = Optional.of(2.0);

    final Optional<Double> newSortOrder =
        orderingService.buildCurrentElementNewSortOrder(
            prevElementSortOrder, currentElementSortOrder, nexElementSortOrder);

    assertTrue(newSortOrder.isPresent());
    assertEquals(
        "newSortOrder value must be present", newSortOrder.get(), currentElementSortOrder.get());
  }

  @Test
  public void buildCurrentElementNewSortOrderWithNextElementEmpty() {

    final Optional<Double> prevElementSortOrder = Optional.of(1.0);
    final Optional<Double> nexElementSortOrder = Optional.empty();
    final Optional<Double> currentElementSortOrder = Optional.of(2.0);

    final Optional<Double> newSortOrder =
        orderingService.buildCurrentElementNewSortOrder(
            prevElementSortOrder, currentElementSortOrder, nexElementSortOrder);

    assertTrue(newSortOrder.isPresent());
    assertEquals(
        "newSortOrder value must be present", newSortOrder.get(), currentElementSortOrder.get());
  }

  @Test
  public void findMaxSortOrderFalseCase() {

    final SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("16")
                .sortOrder(1.0)
                .build());

    final SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("6")
                .sortOrder(2.0)
                .build());

    final List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet1, surfaceBet2).collect(Collectors.toList());
    when(surfaceBetMongoRepository.findTheMaxSortOrderOfThePage(PageType.sport.name(), "16"))
        .thenReturn(surfaceBets);

    Optional<Double> maxSortOrder = orderingService.findMaxSortOrder(PageType.sport.name(), "16");
    assertFalse("maxSortOrder value must be false", maxSortOrder.isPresent());
  }

  @Test
  public void isPrevAndNextElementSame() {

    final Optional<Double> prevElementSortOrder = Optional.empty();
    final Optional<Double> nexElementSortOrder = Optional.empty();

    final boolean prevAndNextElementSame =
        orderingService.isPrevAndNextElementSame(prevElementSortOrder, nexElementSortOrder);

    assertFalse("prevAndNextElementSame value must be false", prevAndNextElementSame);

    final Optional<Double> prevElementSortOrder1 = Optional.of(2.0);
    final Optional<Double> nexElementSortOrder1 = Optional.of(2.0);

    final boolean prevAndNextElementSame1 =
        orderingService.isPrevAndNextElementSame(prevElementSortOrder1, nexElementSortOrder1);

    assertTrue("prevAndNextElementSame value must be true", prevAndNextElementSame1);

    final Optional<Double> prevElementSortOrder2 = Optional.of(2.0);
    ;
    final Optional<Double> nexElementSortOrder2 = Optional.empty();

    final boolean prevAndNextElementSame2 =
        orderingService.isPrevAndNextElementSame(prevElementSortOrder2, nexElementSortOrder2);

    assertFalse("prevAndNextElementSame value must be false", prevAndNextElementSame2);
  }

  @Test
  public void getReferencesSortOrder() {

    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();

    final SurfaceBet validSurfaceBet = createValidSurfaceBet();
    validSurfaceBet
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final Optional<Double> referencesSortOrder =
        orderingService.getReferencesSortOrder(Optional.of(validSurfaceBet), orderDto);

    assertFalse("referencesSortOrder value must be false", referencesSortOrder.isPresent());

    final OrderDto orderDto1 =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();

    final SurfaceBet validSurfaceBet1 = createValidSurfaceBet();
    validSurfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final Optional<Double> referencesSortOrder1 =
        orderingService.getReferencesSortOrder(Optional.of(validSurfaceBet1), orderDto1);

    assertEquals(
        "referencesSortOrder value must be same", referencesSortOrder1.get(), Double.valueOf(2.0));
  }

  @Test
  public void isNextElementSortOrderNull() {

    final Optional<Double> nextElementSortOrder = Optional.empty();

    final SurfaceBet validSurfaceBet = createValidSurfaceBet();
    validSurfaceBet
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final boolean nextElementSortOrderNull =
        orderingService.isNextElementSortOrderNull(
            Optional.of(validSurfaceBet), nextElementSortOrder);
    assertTrue("nextElementSortOrderNull value must be true", nextElementSortOrderNull);

    final Optional<Double> nextElementSortOrder1 = Optional.of(2.0);

    final SurfaceBet validSurfaceBet1 = createValidSurfaceBet();
    validSurfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.eventhub)
                .refId("16")
                .sortOrder(2.0)
                .build());

    final boolean nextElementSortOrderNull1 =
        orderingService.isNextElementSortOrderNull(
            Optional.of(validSurfaceBet1), nextElementSortOrder1);
    assertFalse("nextElementSortOrderNull1 value must be false", nextElementSortOrderNull1);

    final boolean nextElementSortOrderNull2 =
        orderingService.isNextElementSortOrderNull(Optional.empty(), nextElementSortOrder1);
    assertFalse("nextElementSortOrderNull1 value must be false", nextElementSortOrderNull2);
  }

  @Test
  public void getNexElementIndex() {

    final Optional<Integer> nexElementIndex =
        orderingService.getNexElementIndex(2, Arrays.asList("4", "1", "2", "3"));

    assertEquals("nexElementIndex value must be same", nexElementIndex.get(), Integer.valueOf(3));

    final Optional<Integer> nexElementIndex1 =
        orderingService.getNexElementIndex(3, Arrays.asList("4", "1", "2", "3"));

    assertFalse("nexElementIndex value must be false", nexElementIndex1.isPresent());
  }

  private static SurfaceBet createValidSurfaceBet() {
    final SurfaceBet result = new SurfaceBet();
    result.setDisplayFrom(Instant.now());
    result.setDisplayTo(Instant.now().plus(Duration.ofDays(5)));
    result.setEdpOn(true);
    result.setHighlightsTabOn(true);
    result.setPrice(
        new Price()
            .setPriceDec(BigDecimal.valueOf(1.27))
            .setPriceDen(27)
            .setPriceNum(10)
            .setPriceType("LP"));
    result.setSelectionId(BigInteger.valueOf(EXISTS_SELECTION_ID));
    Set<Relation> refs = new HashSet<>();
    refs.add(
        Relation.builder().enabled(true).relatedTo(RelationType.sport).refId(TEST_PAGE_ID).build());
    result.setReferences(refs);
    result.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    result.setBrand("bma");
    result.setTitle("test ;:#@&-+()!?'$£");
    result.setContent("content ;:#@&-+()!?'$£");
    result.setSvgBgId("image1");
    result.setSvgBgImgPath("/images/uploads/svg/test1.svg");
    result.setContentHeader("test");

    return result;
  }

  private static SurfaceBet createValidSurfaceBetForFootball() {
    final SurfaceBet result = new SurfaceBet();
    result.setDisplayFrom(Instant.now());
    result.setDisplayTo(Instant.now().plus(Duration.ofDays(5)));
    result.setEdpOn(true);
    result.setHighlightsTabOn(true);
    result.setPrice(
        new Price()
            .setPriceDec(BigDecimal.valueOf(1.27))
            .setPriceDen(27)
            .setPriceNum(10)
            .setPriceType("LP"));
    result.setSelectionId(BigInteger.valueOf(EXISTS_SELECTION_ID));
    Set<Relation> refs = new HashSet<>();
    refs.add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());
    result.setReferences(refs);
    result.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    result.setBrand("bma");
    result.setTitle("test ;:#@&-+()!?'$£");
    result.setContent("content ;:#@&-+()!?'$£");
    result.setSvgBgId("image1");
    result.setSvgBgImgPath("/images/uploads/svg/test1.svg");
    result.setContentHeader("test");

    return result;
  }

  private static SegmentReference getSegmentReferences(String segmentName) {
    return SegmentReference.builder().segmentName(segmentName).sortOrder(1.0).build();
  }
}
