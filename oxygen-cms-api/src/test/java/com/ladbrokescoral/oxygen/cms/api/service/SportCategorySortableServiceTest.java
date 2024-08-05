package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.util.WithMockCustomUser;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.mockito.InjectMocks;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.util.CollectionUtils;

@RunWith(SpringRunner.class)
public class SportCategorySortableServiceTest {
  @InjectMocks SportCategoryService sportCategoryService;
  @MockBean SportCategoryRepository sportCategoryRepository;
  @MockBean SportCategoryArchivalRepository sportCategoryArchivalRepository;
  @MockBean SegmentService segmentService;
  @MockBean HomeInplaySportRepository homeInplaySportRepository;
  private String segmentName;

  @Before
  public void init() throws Exception {

    doAnswer(AdditionalAnswers.returnsFirstArg()).when(sportCategoryRepository).save(any());
    sportCategoryService =
        new SportCategoryService(
            sportCategoryRepository,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            sportCategoryArchivalRepository,
            segmentService,
            new ModelMapper(),
            homeInplaySportRepository);
  }

  @Test
  public void testUniversalSortOrderWithSegNameNull() {
    when(homeInplaySportRepository.findByCategoryIdAndBrand(any(), any()))
        .thenReturn(createHomeInplay("12121", "mongo", 16));
    prepareRepoNosegment();
    OrderDto dto = createOrder("b", Arrays.asList("b", "a", "c", "d", "e", "f", "g", "h"), null);
    sportCategoryService.dragAndDropOrder(dto);
    this.segmentName = "s1";
    Map<String, Double> resultObject =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertFalse(resultObject.get("b") > resultObject.get("a"));
  }

  @Test
  @WithMockCustomUser
  public void testSegmentSortOrderNoSegReferencesswapElemntToFirstplace() {
    when(homeInplaySportRepository.findByCategoryIdAndBrand(any(), any()))
        .thenReturn(createHomeInplay("12121", "mongo", 16));
    prepareRepoNosegment();
    OrderDto dto = createOrder("b", Arrays.asList("b", "a", "c", "d", "e", "f", "g", "h"), "s1");
    sportCategoryService.dragAndDropOrder(dto);
    this.segmentName = "s1";
    Map<String, Double> resultObject =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(resultObject.get("b") > resultObject.get("a"));
  }

  @Test
  @WithMockCustomUser
  public void testSegmentSortOrderNoSegmentReferencesAddSegment() {
    when(homeInplaySportRepository.findByCategoryIdAndBrand(any(), any()))
        .thenReturn(createHomeInplay("12121", "mongo", 16));
    prepareRepoNosegment();
    segmentreferenceOrderTest1();
    segmentreferenceOrderTest2();
    segmentreferenceOrderTest3();
    segmentreferenceOrderTest4();
    segmentreferenceOrderTest5();
    segmentreferenceOrderEqualOrderTest6();
  }

  @Test
  @WithMockCustomUser
  public void testReorderListSegmentSortOrder() {
    prepareRepo();
    mockFindByIds(Arrays.asList("d", "e", "f", "h"));
    OrderDto dto = createOrder("h", Arrays.asList("a", "b", "c", "d", "e", "f", "h", "g"), "s1");
    this.segmentName = dto.getSegmentName();
    sportCategoryService.dragAndDropOrder(dto);
    verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
  }

  private void segmentreferenceOrderTest1() {
    mockFindByIds(Arrays.asList("a", "b", "h"));
    OrderDto dto = createOrder("h", Arrays.asList("a", "b", "h", "c", "d", "e", "f", "g"), "s1");
    sportCategoryService.dragAndDropOrder(dto);
    this.segmentName = "s1";
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("a") < testResult.get("b") && testResult.get("b") < testResult.get("h"));

    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("a").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("b").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
    assertTrue(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("d").get().getSegmentReferences()));
    assertTrue(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("e").get().getSegmentReferences()));
    assertTrue(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("f").get().getSegmentReferences()));
    assertTrue(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("g").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest2() {
    mockFindByIds(Arrays.asList("c", "d", "e", "b"));
    OrderDto dto2 = createOrder("b", Arrays.asList("a", "h", "c", "d", "e", "b", "f", "g"), "s1");
    sportCategoryService.dragAndDropOrder(dto2);
    this.segmentName = "s1";
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("a") < testResult.get("h")
            && testResult.get("h") < testResult.get("c")
            && testResult.get("c") < testResult.get("d")
            && testResult.get("d") < testResult.get("e"));

    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("a").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("b").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("c").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("d").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("e").get().getSegmentReferences()));
    assertTrue(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("f").get().getSegmentReferences()));
    assertTrue(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("g").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest3() {
    mockFindByIds(Arrays.asList("f", "g", "a"));
    OrderDto dto1 = createOrder("a", Arrays.asList("h", "c", "d", "e", "b", "f", "g", "a"), "s1");
    sportCategoryService.dragAndDropOrder(dto1);
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("h") < testResult.get("c")
            && testResult.get("c") < testResult.get("d")
            && testResult.get("d") < testResult.get("e")
            && testResult.get("e") < testResult.get("b")
            && testResult.get("b") < testResult.get("f")
            && testResult.get("f") < testResult.get("g")
            && testResult.get("g") < testResult.get("a"));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("a").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("b").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("d").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("e").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("f").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("g").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest4() {
    OrderDto dto1 = createOrder("a", Arrays.asList("a", "h", "c", "d", "e", "b", "f", "g"), "s1");
    sportCategoryService.dragAndDropOrder(dto1);
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("a") < testResult.get("h")
            && testResult.get("h") < testResult.get("c")
            && testResult.get("c") < testResult.get("d")
            && testResult.get("d") < testResult.get("e")
            && testResult.get("e") < testResult.get("b")
            && testResult.get("b") < testResult.get("f")
            && testResult.get("f") < testResult.get("g"));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("a").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("b").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("d").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("e").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("f").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("g").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest5() {
    when(homeInplaySportRepository.findByCategoryIdAndBrand(any(), any()))
        .thenReturn(createHomeInplay("12121", "mongo", 16));
    OrderDto dto1 = createOrder("h", Arrays.asList("a", "c", "d", "e", "b", "f", "g", "h"), "s1");
    sportCategoryService.dragAndDropOrder(dto1);
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("a") < testResult.get("c")
            && testResult.get("c") < testResult.get("d")
            && testResult.get("d") < testResult.get("e")
            && testResult.get("e") < testResult.get("b")
            && testResult.get("b") < testResult.get("f")
            && testResult.get("f") < testResult.get("g")
            && testResult.get("g") < testResult.get("h"));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("a").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("b").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("d").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("e").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("f").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("g").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderEqualOrderTest6() {
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "10000000", "c", 150.0, Optional.of("s1"))))
        .when(sportCategoryRepository)
        .findById("c");
    mockFindByIds(Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h"));
    OrderDto dto1 = createOrder("b", Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h"), "s1");
    sportCategoryService.dragAndDropOrder(dto1);
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h"));

    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("a").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("b").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("d").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("e").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("f").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("g").get().getSegmentReferences()));
    assertFalse(
        CollectionUtils.isEmpty(
            sportCategoryRepository.findById("h").get().getSegmentReferences()));
  }

  public void mockFindByIds(List<String> documentIds) {

    doReturn(getlistReorderSegmentSportCategory(documentIds))
        .when(sportCategoryRepository)
        .findByIdMatches(documentIds);
  }

  private List<SportCategory> getlistReorderSegmentSportCategory(List<String> documentIds) {
    return documentIds.stream()
        .map(id -> sportCategoryRepository.findById(id).get())
        .collect(Collectors.toList());
  }

  private void prepareRepoNosegment() {

    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000009", "a", -1.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("a");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000010", "b", 2.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("b");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.eventhub, "0", "100000011", "c", 3.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("c");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000012", "d", 4.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("d");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000013", "e", 5.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("e");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000014", "f", 6.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("f");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000015", "g", 7.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("g");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000016", "h", -8.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("h");
  }

  private static SportCategory buildSportCategory(
      RelationType refType,
      String pageRef,
      String refId,
      String id,
      Double sortOrder,
      Optional<String> segmenName) {
    SportCategory point = new SportCategory();
    List<SegmentReference> segmentReferences = new ArrayList<>();

    if (segmenName.isPresent()) {
      segmentReferences.add(
          SegmentReference.builder()
              .id(segmenName.get())
              .sortOrder(sortOrder)
              .segmentName(segmenName.get())
              .pageRefId(refId)
              .build());
    }

    Set<Relation> refs = new HashSet<>();
    refs.add(Relation.builder().enabled(true).relatedTo(refType).refId(pageRef).id(refId).build());

    point.setSegmentReferences(segmentReferences);
    point.setArchivalId(id);
    point.setId(id);
    point.setSortOrder(sortOrder);
    point.setBrand("bma");
    return point;
  }

  private OrderDto createOrder(String id, List<String> list, String segmentName) {
    return OrderDto.builder()
        .id(id)
        .order(list)
        .segmentName(segmentName)
        .pageId("0")
        .pageType("sport")
        .build();
  }

  private Map<String, Double> verifySortOrder(List<String> order) {
    Map<String, Double> mp =
        order.stream().collect(Collectors.toMap(Function.identity(), idx -> getBody(idx)));
    mp.entrySet().stream()
        .sorted(Map.Entry.comparingByValue())
        .forEach(
            e -> {
              if (e.getValue() >= 0) System.out.print(e.getKey() + "=" + e.getValue() + " ,");
            });
    System.out.println();
    return mp;
  }

  Double getBody(String idx) {

    if (sportCategoryRepository.findById(idx).get().getSegmentReferences().isEmpty()) return -1.0;
    return sportCategoryRepository.findById(idx).get().getSegmentReferences().stream()
        .map(
            reference -> {
              return this.segmentName.equals(reference.getSegmentName())
                  ? reference.getSortOrder()
                  : -1.0;
            })
        .findFirst()
        .get();
  }

  private void prepareRepo() {

    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000001", "a", -1.0, Optional.of("s1"))))
        .when(sportCategoryRepository)
        .findById("a");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000002", "b", 2.0, Optional.of("s1"))))
        .when(sportCategoryRepository)
        .findById("b");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000003", "c", 3.0, Optional.of("s1"))))
        .when(sportCategoryRepository)
        .findById("c");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000004", "d", 4.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("d");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.eventhub, "0", "100000005", "e", 5.0, Optional.of("s2"))))
        .when(sportCategoryRepository)
        .findById("e");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "1", "100000006", "f", 6.0, Optional.of("s3"))))
        .when(sportCategoryRepository)
        .findById("f");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000007", "g", 7.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("g");
    doReturn(
            Optional.of(
                buildSportCategory(
                    RelationType.sport, "0", "100000008", "h", -8.0, Optional.empty())))
        .when(sportCategoryRepository)
        .findById("h");
  }

  private static List<HomeInplaySport> createHomeInplay(
      String id, String name, Integer categoryId) {
    List<HomeInplaySport> sports = new ArrayList<>();
    HomeInplaySport sport = new HomeInplaySport();
    sport.setId(id);
    sport.setBrand("bma");
    sport.setCategoryId(String.valueOf(categoryId));
    sport.setSportName(name);
    sports.add(sport);
    return sports;
  }
}
