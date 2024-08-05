package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.NavigationPointArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import com.ladbrokescoral.oxygen.cms.util.WithMockCustomUser;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.util.CollectionUtils;

@RunWith(SpringRunner.class)
@Import(ModelMapperConfig.class)
public class NavigationSegmentSortableServiceTest {

  private static final String universal = "Universal_veiw";
  private static final String segment = "Segment_veiw";

  @MockBean NavigationPointRepository repository;
  @MockBean NavigationPointArchivalRepository navigationPointArchivalRepository;
  @MockBean SegmentService segmentService;
  @Autowired private ModelMapper modelMapper;
  @MockBean private SegmentedModuleSerive segmentedModuleSerive;

  @InjectMocks NavigationPointService service;
  private String segmentName;

  @Mock private AutomaticUpdateService automaticUpdateService;

  @Before
  public void init() throws Exception {
    service =
        new NavigationPointService(
            repository,
            navigationPointArchivalRepository,
            modelMapper,
            segmentService,
            segmentedModuleSerive,
            automaticUpdateService);

    doAnswer(AdditionalAnswers.returnsFirstArg()).when(repository).save(any());
  }

  @Test
  public void testUniversalSortOrder() {
    prepareRepo();
    OrderDto dto_a =
        createOrder("a", Arrays.asList("b", "a", "c", "d", "e", "f", "g", "h"), "Universal");
    checkUniversalSortOrder(dto_a, getResultView(2.5, 1.0), Optional.of("s1"));
    doReturn(Optional.of(buildNavigationPoint("a", 1.0, Optional.of("s1"))))
        .when(repository)
        .findById("a");

    OrderDto dto_h =
        createOrder("h", Arrays.asList("h", "a", "b", "c", "d", "e", "f", "g"), "Universal");
    checkUniversalSortOrder(dto_h, getResultView(0.0, 8.0), Optional.empty());
    doReturn(Optional.of(buildNavigationPoint("h", 8.0, Optional.empty())))
        .when(repository)
        .findById("h");

    OrderDto dto_d =
        createOrder("d", Arrays.asList("a", "b", "c", "e", "f", "g", "h", "d"), "Universal");
    checkUniversalSortOrder(dto_d, getResultView(9.0, 4.0), Optional.empty());

    OrderDto dto_e =
        createOrder("e", Arrays.asList("a", "b", "c", "d", "f", "e", "g", "h"), "Universal");
    checkUniversalSortOrder(dto_e, getResultView(6.5, 5.0), Optional.of("s2"));
  }

  @Test(expected = Exception.class)
  public void testUniversalSortOrderWithSegmentNameNull() {

    OrderDto dto = createOrder("a", Arrays.asList("b", "a", "c", "d", "e", "f", "g", "h"), null);
    service.dragAndDropOrder(dto);
  }

  @Test
  @WithMockCustomUser
  public void testSegmentSortOrderNoSegmentReferencesswapElemntToFirstplace() {

    prepareRepoNosegment();
    OrderDto dto = createOrder("b", Arrays.asList("b", "a", "c", "d", "e", "f", "g", "h"), "s1");
    service.dragAndDropOrder(dto);
    this.segmentName = "s1";
    Map<String, Double> resultObject =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(resultObject.get("b") > resultObject.get("a"));
  }

  @Test
  @WithMockCustomUser
  public void testSegmentSortOrderNoSegmentReferencesAddSegment() {

    prepareRepoNosegment();
    segmentreferenceOrderTest1();
    segmentreferenceOrderTest2();
    segmentreferenceOrderTest3();
    segmentreferenceOrderTest4();
    segmentreferenceOrderTest5();
    segmentreferenceOrderEqualOrderTest6();
  }

  private void segmentreferenceOrderTest1() {
    mockFindByIds(Arrays.asList("a", "b", "h"));
    OrderDto dto = createOrder("h", Arrays.asList("a", "b", "h", "c", "d", "e", "f", "g"), "s1");
    service.dragAndDropOrder(dto);
    this.segmentName = "s1";
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("a") < testResult.get("b") && testResult.get("b") < testResult.get("h"));

    assertFalse(CollectionUtils.isEmpty(repository.findById("a").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("b").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
    assertTrue(CollectionUtils.isEmpty(repository.findById("d").get().getSegmentReferences()));
    assertTrue(CollectionUtils.isEmpty(repository.findById("e").get().getSegmentReferences()));
    assertTrue(CollectionUtils.isEmpty(repository.findById("f").get().getSegmentReferences()));
    assertTrue(CollectionUtils.isEmpty(repository.findById("g").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest2() {
    mockFindByIds(Arrays.asList("c", "d", "e", "b"));
    OrderDto dto2 = createOrder("b", Arrays.asList("a", "h", "c", "d", "e", "b", "f", "g"), "s1");
    service.dragAndDropOrder(dto2);
    this.segmentName = "s1";
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("a") < testResult.get("h")
            && testResult.get("h") < testResult.get("c")
            && testResult.get("c") < testResult.get("d")
            && testResult.get("d") < testResult.get("e"));

    assertFalse(CollectionUtils.isEmpty(repository.findById("a").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("b").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("c").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("d").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("e").get().getSegmentReferences()));
    assertTrue(CollectionUtils.isEmpty(repository.findById("f").get().getSegmentReferences()));
    assertTrue(CollectionUtils.isEmpty(repository.findById("g").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest3() {
    mockFindByIds(Arrays.asList("f", "g", "a"));
    OrderDto dto1 = createOrder("a", Arrays.asList("h", "c", "d", "e", "b", "f", "g", "a"), "s1");
    service.dragAndDropOrder(dto1);
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
    assertFalse(CollectionUtils.isEmpty(repository.findById("a").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("b").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("d").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("e").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("f").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("g").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest4() {
    OrderDto dto1 = createOrder("a", Arrays.asList("a", "h", "c", "d", "e", "b", "f", "g"), "s1");
    service.dragAndDropOrder(dto1);
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
    assertFalse(CollectionUtils.isEmpty(repository.findById("a").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("b").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("d").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("e").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("f").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("g").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderTest5() {
    OrderDto dto1 = createOrder("h", Arrays.asList("a", "c", "d", "e", "b", "f", "g", "h"), "s1");
    service.dragAndDropOrder(dto1);
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
    assertFalse(CollectionUtils.isEmpty(repository.findById("a").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("b").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("d").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("e").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("f").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("g").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
  }

  private void segmentreferenceOrderEqualOrderTest6() {
    doReturn(Optional.of(buildNavigationPoint("c", 150.0, Optional.of("s1"))))
        .when(repository)
        .findById("c");
    mockFindByIds(Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h"));
    OrderDto dto1 = createOrder("b", Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h"), "s1");
    service.dragAndDropOrder(dto1);
    Map<String, Double> testResult =
        verifySortOrder(Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h"));
    assertTrue(
        testResult.get("a") < testResult.get("b")
            && testResult.get("b") < testResult.get("c")
            && testResult.get("c") < testResult.get("d")
            && testResult.get("d") < testResult.get("e")
            && testResult.get("e") < testResult.get("f")
            && testResult.get("f") < testResult.get("g")
            && testResult.get("g") < testResult.get("h"));
    assertFalse(CollectionUtils.isEmpty(repository.findById("a").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("b").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("d").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("e").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("f").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("g").get().getSegmentReferences()));
    assertFalse(CollectionUtils.isEmpty(repository.findById("h").get().getSegmentReferences()));
  }

  @Test
  @WithMockCustomUser
  public void testreorderListSegmentSortOrder() {
    prepareRepo();
    mockFindByIds(Arrays.asList("d", "e", "f", "h"));
    OrderDto dto = createOrder("h", Arrays.asList("a", "b", "c", "d", "e", "f", "h", "g"), "s1");
    this.segmentName = dto.getSegmentName();
    service.dragAndDropOrder(dto);
    verifySortOrder(Arrays.asList("a", "b", "d", "c", "e", "f", "g", "h"));
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

    if (repository.findById(idx).get().getSegmentReferences().isEmpty()) return -1.0;
    return repository.findById(idx).get().getSegmentReferences().stream()
        .map(
            reference -> {
              return this.segmentName.equals(reference.getSegmentName())
                  ? reference.getSortOrder()
                  : -1.0;
            })
        .findFirst()
        .get();
  }

  private void checkUniversalSortOrder(
      OrderDto dto, Map<String, Double> resultView, Optional<String> segmentName) {
    service.dragAndDropOrder(dto);
    verify(repository, times(1))
        .save(getResultNavigationPoint(dto.getId(), segmentName, resultView));
  }

  private Map<String, Double> getResultView(double universalValue, double segmentVal) {
    Map<String, Double> resultview = new HashMap<>();
    resultview.put(universal, universalValue);
    resultview.put(segment, segmentVal);
    return resultview;
  }

  private OrderDto createOrder(String id, List<String> list, String segmantName) {
    return OrderDto.builder().id(id).order(list).segmentName(segmantName).build();
  }

  private static NavigationPoint buildNavigationPoint(
      String id, Double sortOrder, Optional<String> segmenName) {
    NavigationPoint point = new NavigationPoint();
    List<SegmentReference> segmentReferences = new ArrayList<>();

    if (segmenName.isPresent()) {
      segmentReferences.add(
          SegmentReference.builder()
              .id(segmenName.get())
              .sortOrder(sortOrder)
              .segmentName(segmenName.get())
              .build());
    }
    point.setSegmentReferences(segmentReferences);
    point.setArchivalId(id);
    point.setId(id);
    point.setSortOrder(sortOrder);
    return point;
  }

  private NavigationPoint getResultNavigationPoint(
      String id, Optional<String> segmenName, Map<String, Double> resultview) {
    NavigationPoint point = new NavigationPoint();
    List<SegmentReference> segmentReferences = new ArrayList<>();

    if (segmenName.isPresent()) {
      segmentReferences.add(
          SegmentReference.builder()
              .id(segmenName.get())
              .sortOrder(resultview.get(segment))
              .segmentName(segmenName.get())
              .build());
    }
    point.setSegmentReferences(segmentReferences);

    point.setArchivalId(id);
    point.setId(id);
    point.setSortOrder(resultview.get(universal));
    return point;
  }

  private NavigationPoint getResultSegmentNavigationPoint(
      String id, Optional<String> segmenName, Map<String, Double> resultview) {
    NavigationPoint point = new NavigationPoint();

    if (segmenName.isPresent()) {
      List<SegmentReference> segmentReferences = new ArrayList<>();
      segmentReferences.add(
          SegmentReference.builder()
              .id(segmenName.get())
              .sortOrder(resultview.get(segment))
              .segmentName(segmenName.get())
              .build());
      point.setSegmentReferences(segmentReferences);
    }
    point.setArchivalId(id);
    point.setId(id);
    point.setSortOrder(resultview.get(universal));
    return point;
  }

  public void mockFindByIds(List<String> documentIds) {

    doReturn(getlistReorderSegmentNavigationPoint(documentIds))
        .when(repository)
        .findByIdMatches(documentIds);
  }

  private List<NavigationPoint> getlistReorderSegmentNavigationPoint(List<String> documentIds) {
    return documentIds.stream()
        .map(id -> repository.findById(id).get())
        .collect(Collectors.toList());
  }

  private void prepareRepo() {

    doReturn(Optional.of(buildNavigationPoint("a", 1.0, Optional.of("s1"))))
        .when(repository)
        .findById("a");
    doReturn(Optional.of(buildNavigationPoint("b", 2.0, Optional.of("s1"))))
        .when(repository)
        .findById("b");
    doReturn(Optional.of(buildNavigationPoint("c", 3.0, Optional.of("s1"))))
        .when(repository)
        .findById("c");
    doReturn(Optional.of(buildNavigationPoint("d", 4.0, Optional.empty())))
        .when(repository)
        .findById("d");
    doReturn(Optional.of(buildNavigationPoint("e", 5.0, Optional.of("s2"))))
        .when(repository)
        .findById("e");
    doReturn(Optional.of(buildNavigationPoint("f", 6.0, Optional.of("s3"))))
        .when(repository)
        .findById("f");
    doReturn(Optional.of(buildNavigationPoint("g", 7.0, Optional.empty())))
        .when(repository)
        .findById("g");
    doReturn(Optional.of(buildNavigationPoint("h", 8.0, Optional.empty())))
        .when(repository)
        .findById("h");
  }

  private void prepareRepoNosegment() {

    doReturn(Optional.of(buildNavigationPoint("a", 1.0, Optional.empty())))
        .when(repository)
        .findById("a");
    doReturn(Optional.of(buildNavigationPoint("b", 2.0, Optional.empty())))
        .when(repository)
        .findById("b");
    doReturn(Optional.of(buildNavigationPoint("c", 3.0, Optional.empty())))
        .when(repository)
        .findById("c");
    doReturn(Optional.of(buildNavigationPoint("d", 4.0, Optional.empty())))
        .when(repository)
        .findById("d");
    doReturn(Optional.of(buildNavigationPoint("e", 5.0, Optional.empty())))
        .when(repository)
        .findById("e");
    doReturn(Optional.of(buildNavigationPoint("f", 6.0, Optional.empty())))
        .when(repository)
        .findById("f");
    doReturn(Optional.of(buildNavigationPoint("g", 7.0, Optional.empty())))
        .when(repository)
        .findById("g");
    doReturn(Optional.of(buildNavigationPoint("h", 8.0, Optional.empty())))
        .when(repository)
        .findById("h");
  }
}
