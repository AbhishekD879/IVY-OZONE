package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SurfaceBetArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

@RunWith(MockitoJUnitRunner.Silent.class)
@SuppressWarnings("java:S2699")
public class SurfaceBetServiceTest {

  private static final int EXISTS_SELECTION_ID = 907016395;

  private static final String TEST_PAGE_ID = "test";

  @InjectMocks private SurfaceBetService sbService;
  @Mock private BrandService brandService;
  @Mock private UserService userServiceMock;
  @Mock private SurfaceBetRepository surfaceBetRepository;
  @Mock SvgImageParser svgImageParser;
  @Mock ImageService imageService;
  @Mock SvgEntityService<SurfaceBet> svgEntityService;
  @Mock SiteServeApiProvider siteServeApiProvider;
  @Mock SurfaceBetArchivalRepository surfaceBetArchivalRepository;
  @Mock private SegmentService segmentService;
  @Mock private ModelMapper modelMapper;
  @Mock private SiteServerApi siteServerApi;
  @Mock private SegmentedService<?> segmentedService;
  @Mock private CompetitionModuleService competitionModuleService;

  @Mock private SportPagesOrderingService sportPagesOrderingService;

  @Mock private SurfaceBetTitleService surfaceBetTitleService;

  @Before
  public void init() {
    when(siteServeApiProvider.api("bma")).thenReturn(siteServerApi);
    when(siteServerApi.getEvent(any(), eq(true))).thenReturn(Optional.of(new Event()));
    when(siteServerApi.getClassToSubTypeForType(anyString(), any()))
        .thenReturn(Optional.of(Collections.singletonList(new Category())));
    when(surfaceBetRepository.save(any())).thenReturn(createSurfaceBet());
    surfaceBetRepository = Mockito.mock(SurfaceBetRepository.class);
    Relation ref = Relation.builder().refId("2").relatedTo(RelationType.eventhub).build();
    SurfaceBet surfaceBet = createValidSurfaceBet();
    surfaceBet.getReferences().add(ref);
    List<SurfaceBet> singletonList = Collections.singletonList(surfaceBet);
    Mockito.when(surfaceBetRepository.findByBrand("bma")).thenReturn(singletonList);

    siteServeApiProvider = Mockito.mock(SiteServeApiProvider.class);
    SiteServerApi siteServeApi = Mockito.mock(SiteServerApi.class);
    ArrayList<Event> arrayList = new ArrayList<>();

    Optional<List<Event>> empty = Optional.of(arrayList);
    Mockito.when(
            siteServeApi.getEventToOutcomeForOutcome(
                Mockito.anyList(), Mockito.any(), Mockito.anyList()))
        .thenReturn(empty);
    Page mock = Mockito.mock(Page.class);
    Mockito.when(mock.getContent()).thenReturn(singletonList);
    Mockito.when(surfaceBetRepository.findAll(Mockito.any(Pageable.class))).thenReturn(mock);
    Mockito.when(siteServeApiProvider.api("bma")).thenReturn(siteServeApi);

    sbService =
        new SurfaceBetService(
            surfaceBetRepository,
            svgEntityService,
            "/foo/test",
            siteServeApiProvider,
            surfaceBetArchivalRepository,
            segmentService,
            modelMapper,
            competitionModuleService,
            sportPagesOrderingService,
            surfaceBetTitleService);
  }

  @Test
  public void hasOnPage() {
    Set<Relation> refs = new HashSet<>();
    refs.add(Relation.builder().refId(TEST_PAGE_ID).relatedTo(RelationType.sport).build());
    assertTrue(sbService.hasOnPage(RelationType.sport, TEST_PAGE_ID, refs));
  }

  @Test
  public void testSurfaceBetTest() {

    when(surfaceBetRepository.findUniversalRecordsByBrandAndPageRef("bma", RelationType.sport, "0"))
        .thenReturn(findSurfaceBets());
    List<SurfaceBet> bets =
        sbService.findByBrandAndSegmentNameAndRelationRef(
            "bma", "sport", "0", SegmentConstants.UNIVERSAL);
    Assert.assertEquals("10", bets.get(0).getId());
  }

  @Test
  public void testFindActiveSurfaceBetsByBrand() {
    List<SurfaceBet> activeSurfaceBets = new ArrayList<>();
    activeSurfaceBets.add(createSurfaceBet());

    when(surfaceBetRepository.findActiveSurfaceBetsByBrand("bma", Instant.now()))
        .thenReturn(activeSurfaceBets);
    Set<String> activeBets = sbService.findActiveSurfaceBetsByBrand("bma");
    Assert.assertEquals(0, activeBets.size());
  }

  @Test
  public void testFindActiveSurfaceBetsByBrandWithEmpty() {
    List<SurfaceBet> activeSurfaceBets = new ArrayList<>();

    when(surfaceBetRepository.findActiveSurfaceBetsByBrand("bma", Instant.now()))
        .thenReturn(activeSurfaceBets);
    Set<String> activeBets = sbService.findActiveSurfaceBetsByBrand("bma");
    Assert.assertEquals(0, activeBets.size());
  }

  @Test
  public void testSelectionIdPerSegment() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();

    surfaceBet.setExclusionList(Arrays.asList("s2,s10"));

    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s4")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);

    assertNotNull(result);
  }

  @Test
  public void testUniqueSelectionIdPerSegment() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(true);
    surfaceBet.setExclusionList(Arrays.asList("s2,s10"));

    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertNotNull(result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForUniversal() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setExclusionList(new ArrayList<>());
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertNotNull(result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForsegmentedmatchedData() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4", "s5", "s6"));
    surfaceBet.setDisplayFrom(Instant.now().plus(10, ChronoUnit.DAYS));
    surfaceBet.setDisplayTo(Instant.now().plus(11, ChronoUnit.DAYS));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));

    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForsegmentedUnmatchedData() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4", "s5", "s6"));
    surfaceBet.setDisplayFrom(Instant.now().plus(4, ChronoUnit.DAYS));
    surfaceBet.setDisplayTo(Instant.now().plus(5, ChronoUnit.DAYS));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));

    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForsegmented() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4", "s5", "s6"));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForsegmentedemptyList() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4", "s5", "s6"));

    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(new ArrayList<>());

    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForsegmentedFalse() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4", "s5", "s6", "s2"));

    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertNotNull(result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForExclusiveList() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4", "s5", "s6", "s2"));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertNotNull(result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForExclusiveListDisplayTo() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4", "s5", "s6", "s2"));
    surfaceBet.setDisplayTo(Instant.now().minus(1, ChronoUnit.DAYS));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Arrays.asList("s2")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertNotNull(result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentExclusiveListTrue() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4"));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getSegmentedHCList(Arrays.asList("s4")));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentForrepoExclusiveListempty() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s4"));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getSegmentedHCList(new ArrayList<>()));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertNotNull(result);
  }

  @Test
  public void testUpdateSelectionIdPerSegment() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s3"));
    surfaceBet.setId("test");
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getSegmentedHCList(Arrays.asList("s4")));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUpdateSelectionIdPerSegmentisPage0() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s3"));
    surfaceBet.setId("test");
    surfaceBet.setPageType(PageType.eventhub);

    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUniqueSelectionIdPerSegmentInclusiveEmpty() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(true);
    surfaceBet.setExclusionList(Arrays.asList("s2,s10"));
    when(surfaceBetRepository.findBySelectionIdAndBrand(anyString(), any(), any()))
        .thenReturn(getHCList(Collections.EMPTY_LIST));
    when(segmentService.getSegmentsForSegmentedViews("bma"))
        .thenReturn(Arrays.asList("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"));
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertNotNull(result);
  }

  @Test
  public void testUpdateSelectionIdPerSegmentwithEventHub() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s3"));
    surfaceBet.setId("test");
    surfaceBet.setPageId("22");
    surfaceBet.setPageType(PageType.eventhub);
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testUpdateSelectionIdPerSegmentNotHomePage() {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(Arrays.asList("s3"));
    surfaceBet.setId("test");
    surfaceBet.setPageId("22");
    Optional<SurfaceBet> result = sbService.isUniqueSelectionIdPerSegment(surfaceBet);
    assertEquals(Optional.empty(), result);
  }

  @Test
  public void testRemoveIdsFromCompetitionModules()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    when(competitionModuleService.findCompetitionModulesByType(CompetitionModuleType.SURFACEBET))
        .thenReturn(getCompModulesList());
    Method method =
        SurfaceBetService.class.getDeclaredMethod("removeIdsFromCompetitionModules", String.class);
    method.setAccessible(true);
    method.invoke(sbService, "2");
    verify(competitionModuleService, times(2)).save((CompetitionModule) Mockito.any());
  }

  @Test
  public void dragAndDropOrder() {

    final OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .build();

    sbService.dragAndDropOrder(orderDto);
  }

  @Test
  public void dragAndDropOrderForHomePage() {

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

    when(surfaceBetRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    when(surfaceBetRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    when(surfaceBetRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    when(surfaceBetRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));

    sbService.dragAndDropOrder(orderDto);
  }

  @Test
  public void testVerifyAndSaveSBTitle_Null() {
    when(surfaceBetTitleService.findSurfaceBetTitleByTitle(Mockito.any())).thenReturn(null);
    sbService.verifyAndSaveSBTitle(Mockito.mock(SurfaceBet.class));
    verify(surfaceBetTitleService, times(1)).save(Mockito.any(SurfaceBetTitle.class));
  }

  @Test
  public void testVerifyAndSaveSBTitle_NotNull() {
    when(surfaceBetTitleService.findSurfaceBetTitleByTitle(Mockito.any()))
        .thenReturn(new SurfaceBetTitle());
    sbService.verifyAndSaveSBTitle(Mockito.mock(SurfaceBet.class));
    verify(surfaceBetTitleService, times(0)).save(Mockito.any(SurfaceBetTitle.class));
  }

  private List<CompetitionModule> getCompModulesList() {
    CompetitionModule competitionModule1 = new CompetitionModule();
    competitionModule1.getSurfaceBets().addAll(Arrays.asList("1", "2", "3"));
    CompetitionModule competitionModule2 = new CompetitionModule();
    competitionModule2.getSurfaceBets().addAll(Arrays.asList("2", "3", "4"));
    List<CompetitionModule> competitionModules = new ArrayList<>();
    competitionModules.add(competitionModule1);
    competitionModules.add(competitionModule2);
    return competitionModules;
  }

  private List<SurfaceBet> getSegmentedHCList(List<String> segments) {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();
    surfaceBet.setId("test");
    surfaceBet.setUniversalSegment(true);
    surfaceBet.setExclusionList(segments);
    return Arrays.asList(surfaceBet);
  }

  private List<SurfaceBet> getHCList(List<String> segments) {
    SurfaceBet surfaceBet = createSurfaceBetWithSegment();

    surfaceBet.setId("test");
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setInclusionList(segments);

    return Arrays.asList(surfaceBet);
  }

  private SurfaceBet createSurfaceBet() {
    SurfaceBet surfaceBet = new SurfaceBet();
    surfaceBet.setId(UUID.randomUUID().toString());
    surfaceBet.setSportId(16);
    surfaceBet.setSelectionId(BigInteger.valueOf(1));
    surfaceBet.setBrand("bma");
    surfaceBet.setDisplayFrom(Instant.now());
    surfaceBet.setDisplayTo(Instant.now().plus(3, ChronoUnit.DAYS));
    return surfaceBet;
  }

  private SurfaceBet createSurfaceBetWithSegment() {
    SurfaceBet surfaceBet = new SurfaceBet();
    surfaceBet.setId(UUID.randomUUID().toString());
    surfaceBet.setSportId(16);
    surfaceBet.setBrand("bma");
    surfaceBet.setUniversalSegment(true);
    surfaceBet.setPageId("0");
    surfaceBet.setPageType(PageType.sport);
    surfaceBet.setDisplayFrom(Instant.now().plus(5, ChronoUnit.DAYS));
    surfaceBet.setDisplayTo(Instant.now().plus(6, ChronoUnit.DAYS));
    surfaceBet.setSelectionId(BigInteger.valueOf(1));
    return surfaceBet;
  }

  public SurfaceBet createValidSurfaceBet() {
    SurfaceBet result = new SurfaceBet();
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
    result.setBrand("bma");
    result.setTitle("test");
    return result;
  }

  public List<SurfaceBet> findSurfaceBets() {

    List<SurfaceBet> surfaceBets = new ArrayList<>();
    surfaceBets.add(createSurfabet("1", 1.2));
    surfaceBets.add(createSurfabet("2", 1.01));
    surfaceBets.add(createSurfabet("3", 1.001));
    surfaceBets.add(createSurfabet("4", 1.2));
    surfaceBets.add(createSurfabet("5", 1.0));
    surfaceBets.add(createSurfabet("1.1", 500.0));
    surfaceBets.add(createSurfabet("6", 1.2));
    surfaceBets.add(createSurfabet("7", 200.0));
    surfaceBets.add(createSurfabet("9", 0.2));
    surfaceBets.add(createSurfabet("10", 0.01));

    return surfaceBets;
  }

  private SurfaceBet createSurfabet(String id, Double sortOrder) {
    SurfaceBet s1 = createValidSurfaceBet();
    s1.setId(id);
    List<SegmentReference> segmentReferences1 = new ArrayList<>();
    SegmentReference reference1 = new SegmentReference();
    reference1.setSegmentName(SegmentConstants.UNIVERSAL);
    reference1.setSortOrder(sortOrder);
    reference1.setPageRefId("121");
    segmentReferences1.add(reference1);
    s1.setSegmentReferences(segmentReferences1);
    Set<Relation> refs1 = new HashSet<>();
    refs1.add(
        Relation.builder()
            .enabled(true)
            .relatedTo(RelationType.sport)
            .refId("0")
            .id("121")
            .build());
    s1.setReferences(refs1);
    return s1;
  }
}
