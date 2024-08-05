package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplayConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentedModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.EventHubService;
import com.ladbrokescoral.oxygen.cms.api.service.HomeInplaySportService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Random;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

// @RunWith(SpringRunner.class)
@WebMvcTest({
  HomeInplaySports.class,
  HomeInplaySportService.class,
  SegmentService.class,
  ModelMapper.class,
  SegmentedModuleSerive.class
})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({SvgEntityService.class, EventHubService.class, BrandService.class})
@Import(ModelMapperConfig.class)
public class HomeInplaySportsTest extends AbstractControllerTest {

  private static final String HOME_INPLAY_URL = "/v1/api/home-inplay-sport";

  @MockBean private HomeInplaySportRepository repository;
  @MockBean private SiteServeApiProvider siteServeApiProvider;
  @MockBean private SiteServerApi siteServerApi;
  @MockBean private SportModuleArchivalRepository sportModuleArchivalRepository;
  @MockBean private SportModuleRepository sportModuleRepository;
  @MockBean private SegmentRepository segmentRepository;
  @MockBean private SegmentedModuleRepository segmentedModuleRepository;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  @Before
  public void init() {

    given(repository.findById("61ded854655d8c6879be78a0"))
        .willReturn(
            Optional.of(
                create(
                    "1", "a", "61ded854655d8c6879be78a0", 0.2, SegmentConstants.UNIVERSAL, true)));

    given(repository.save(any(HomeInplaySport.class))).will(AdditionalAnswers.returnsFirstArg());
    given(repository.saveAll(anyList())).will(AdditionalAnswers.returnsFirstArg());

    given(siteServeApiProvider.api("bma")).willReturn(siteServerApi);
    given(siteServerApi.getEvent(any(), eq(true))).willReturn(Optional.of(new Event()));

    given(repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(findUniversalRecords());

    given(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .willReturn(findSegmentsRecords());

    given(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(findAllEntites());

    given(
            sportModuleRepository.findAllByBrandAndPageTypeAndPageIdAndModuleType(
                "bma", PageType.sport, "0", SportModuleType.INPLAY))
        .willReturn(sportModule(0, SportModuleType.INPLAY));
  }

  @Test
  public void testCreateHomeInplaySportInplayNull() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(HOME_INPLAY_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.readFromFileAsBytes(
                        "controller/public_api/home-inplay-sport_null_brand.json")))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateHomeInplaySportSportModuleInplayConfigNull() throws Exception {

    Optional<SportModule> module = sportModule(0, SportModuleType.INPLAY);
    module.get().setInplayConfig(null);
    given(
            sportModuleRepository.findAllByBrandAndPageTypeAndPageIdAndModuleType(
                "bma", PageType.sport, "0", SportModuleType.INPLAY))
        .willReturn(module);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(HOME_INPLAY_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.readFromFileAsBytes("controller/public_api/home-inplay-sport.json")))
        .andExpect(MockMvcResultMatchers.jsonPath("$.categoryId").value("16"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateHomeInplaySportSportModuleNull() throws Exception {
    given(
            sportModuleRepository.findAllByBrandAndPageTypeAndPageIdAndModuleType(
                "bma", PageType.sport, "0", SportModuleType.INPLAY))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(HOME_INPLAY_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.readFromFileAsBytes("controller/public_api/home-inplay-sport.json")))
        .andExpect(MockMvcResultMatchers.jsonPath("$.categoryId").value("16"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateHomeInplaySport() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(HOME_INPLAY_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.readFromFileAsBytes("controller/public_api/home-inplay-sport.json")))
        .andExpect(MockMvcResultMatchers.jsonPath("$.categoryId").value("16"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateHomeInplaySport() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/home-inplay-sport/61ded854655d8c6879be78a0")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.readFromFileAsBytes("controller/public_api/home-inplay-sport.json")))
        .andExpect(MockMvcResultMatchers.jsonPath("$.eventCount").value(2))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/home-inplay-sport/61ded854655d8c6879be78a0")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.eventCount").value(3));
  }

  @Test
  public void testReadByBrandAndSegmentNameWithoutPageType() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    HOME_INPLAY_URL + "/brand/bma/segment/" + SegmentConstants.UNIVERSAL)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(8));
  }

  @Test
  public void testReadByBrandAndSegmentNameWithoutPageTypeForNonUniversal() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(HOME_INPLAY_URL + "/brand/bma/segment/segment1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(5));
  }

  @Test
  public void successfulDeleteShouldReturn204() throws Exception {

    String idToBeRemoved = "61ded854655d8c6879be78a0";
    mockMvc
        .perform(MockMvcRequestBuilders.delete(HOME_INPLAY_URL + "/" + idToBeRemoved))
        .andExpect(status().isNoContent());
  }

  @Test
  public void deleteShouldReturn404WhenEntityDoesntExist() throws Exception {

    String idToBeRemoved = "101";
    given(repository.findById(idToBeRemoved)).willReturn(Optional.empty());
    mockMvc
        .perform(MockMvcRequestBuilders.delete(HOME_INPLAY_URL + "/" + idToBeRemoved))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testorder() throws Exception {

    given(
            repository.findByIdMatches(
                Arrays.asList("61ded854655d8c6879be78a0", "61ded854655d8c6879be78a1")))
        .willReturn(
            Arrays.asList(
                create("2", "a", "61ded854655d8c6879be78a0", 0.5, SegmentConstants.UNIVERSAL, true),
                create(
                    "2", "a", "61ded854655d8c6879be78a1", 0.7, SegmentConstants.UNIVERSAL, true)));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(HOME_INPLAY_URL + "/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  private OrderDto createOrderDto() {
    List<String> strings = new ArrayList<>();
    strings.add("61ded854655d8c6879be78a0");
    strings.add("61ded854655d8c6879be78a1");

    return OrderDto.builder().order(strings).id("61ded854655d8c6879be78a0").build();
  }

  public static List<HomeInplaySport> findAllEntites() {

    List<HomeInplaySport> sCategories = new ArrayList<>();
    sCategories.addAll(findSegmentsRecords());
    sCategories.addAll(findUniversalRecords());
    HomeInplaySport sport = create("11", "ab", "1", 0.2, "segment1", false);
    sport.setInclusionList(Collections.emptyList());
    sCategories.add(sport);
    return sCategories;
  }

  public static List<HomeInplaySport> findSegmentsRecords() {
    List<HomeInplaySport> sCategories = new ArrayList<>();
    sCategories.add(create("11", "ab", "1", 0.2, "segment1", false));
    sCategories.add(create("21", "bc", "2", 0.3, "segment1", false));
    sCategories.add(create("31", "cd", "3", 0.4, "segment1", false));
    sCategories.add(create("41", "ef", "4", 0.5, "segment1", false));
    sCategories.add(create("41", "gh", "5", -1.0, "segment1", false));

    return sCategories;
  }

  public static List<HomeInplaySport> findUniversalRecords() {
    List<HomeInplaySport> sCategories = new ArrayList<>();
    sCategories.add(create("1", "a", "11", 0.2, SegmentConstants.UNIVERSAL, true));
    sCategories.add(create("2", "b", "16", 0.3, SegmentConstants.UNIVERSAL, true));
    sCategories.add(create("3", "c", "7", 0.4, SegmentConstants.UNIVERSAL, true));
    sCategories.add(create("4", "d", "8", 0.5, SegmentConstants.UNIVERSAL, true));
    sCategories.add(create("4", "e", "9", -1.2, SegmentConstants.UNIVERSAL, true));
    sCategories.add(create("4", "e", "9"));

    HomeInplaySport withExclusiveInSements =
        create("4", "e", "9", -1.2, SegmentConstants.UNIVERSAL, true);
    withExclusiveInSements.setExclusionList(Arrays.asList("segment1", "segment2"));
    sCategories.add(withExclusiveInSements);

    HomeInplaySport withExclusiveInSementsinvalid =
        create("4", "e", "13", -1.2, SegmentConstants.UNIVERSAL, true);
    withExclusiveInSementsinvalid.setExclusionList(Arrays.asList("segment2"));
    sCategories.add(withExclusiveInSementsinvalid);

    return sCategories;
  }

  private static HomeInplaySport create(
      String categoryId,
      String sportname,
      String id,
      Double sortOrder,
      String segmentName,
      boolean isuniversal) {
    HomeInplaySport sportCategory = create(categoryId, sportname, id);
    sportCategory.setCreatedAt(Instant.now());
    sportCategory.setUniversalSegment(isuniversal);

    List<SegmentReference> segmentReferences = new ArrayList<>();

    SegmentReference reference = new SegmentReference();
    reference.setSegmentName(segmentName);
    reference.setSortOrder(sortOrder);
    segmentReferences.add(reference);
    sportCategory.setSegmentReferences(segmentReferences);
    if (!isuniversal) sportCategory.setInclusionList(Arrays.asList(segmentName));

    return sportCategory;
  }

  private static HomeInplaySport create(String categoryId, String sportname, String id) {
    HomeInplaySport dto = new HomeInplaySport();
    dto.setId(id);
    dto.setBrand("bma");
    dto.setSportName(sportname);
    dto.setCategoryId(categoryId);
    dto.setEventCount(3);
    return dto;
  }

  private Optional<SportModule> sportModule(Integer sportId, SportModuleType moduleType) {
    SportModule module = sportModule();
    module.setSportId(sportId);
    module.setPageId(String.valueOf(sportId));
    module.setModuleType(moduleType);
    module.setId(String.valueOf(sportId) + new Random().nextInt());
    module.setPageType(PageType.sport);
    module.setInplayConfig(new HomeInplayConfig());
    return Optional.of(module);
  }

  private SportModule sportModule() {
    SportModule module = new SportModule();
    module.setTitle("title");
    module.setBrand("bma");
    return module;
  }
}
