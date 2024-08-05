package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.FooterMenuArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.FooterMenuArchive;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.FooterMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mock;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {FooterMenus.class, FooterMenuService.class, SegmentService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({
  BrandService.class,
  ImageEntityService.class,
  SvgEntityService.class,
  ImageConfig.ImagePath.class,
  SegmentedModuleSerive.class
})
@Import(ModelMapperConfig.class)
public class FooterMenusTest extends AbstractControllerTest {

  @MockBean private FooterMenuRepository repository;
  @MockBean private FooterMenuArchivalRepository footerMenuArchivalRepository;
  @MockBean private SegmentRepository segmentRepository;
  @MockBean private SecurityContext securityContext;
  @MockBean private Authentication authentication;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  private FooterMenu entity;
  @Mock private org.springframework.security.core.Authentication auth;

  @Before
  public void init() {
    entity = createFooterMenu("1", false, "universal");

    SecurityContextHolder.setContext(securityContext);
    given(securityContext.getAuthentication()).willReturn(authentication);
    given(authentication.getPrincipal()).willReturn(User.builder().id("1").build());

    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getFooterMenuList());

    given(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .willReturn(getFooterMenuListForUniversalFalse());

    given(
            repository.findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                "bma",
                Arrays.asList("segment1"),
                Arrays.asList("1", "2"),
                SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getFooterMenuList());

    given(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getFooterMenuList());

    given(repository.save(any(FooterMenu.class))).will(AdditionalAnswers.returnsFirstArg());

    given(footerMenuArchivalRepository.save(any(FooterMenuArchive.class)))
        .will(AdditionalAnswers.returnsFirstArg());

    when(auth.getPrincipal()).thenReturn(User.builder().id("1234567").build());
    SecurityContextHolder.getContext().setAuthentication(auth);
  }

  @Test
  public void testCreateMarket() throws Exception {
    entity.setId(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateFooterForUniversalTrue() throws Exception {
    entity = createFooterMenu("1", true, "s1");
    entity.setExclusionList(Arrays.asList("s1"));
    entity.setId(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateFooterForUniversalTrueNotContainsSegment() throws Exception {
    entity = createFooterMenu("1", true, "s1");
    entity.setExclusionList(Arrays.asList("s4"));
    entity.setId(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreatewithsegments() throws Exception {

    when(segmentRepository.findByBrandAndSegmentName("bma", "s2"))
        .thenReturn(Optional.of(Segment.builder().segmentName("s2").build()));
    entity.setId(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getSegmentEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateMarket() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/footer-menu/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/footer-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.linkTitle", is("image1")))
        .andExpect(jsonPath("$.brand", is("bma")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(any(String.class))).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/footer-menu/3")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound())
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/footer-menu")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/footer-menu/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(1)));
  }

  @Test
  public void testReadAllByBrandAndSegmentForUniversalSegment() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/footer-menu/brand/bma/segment/universal")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(1)))
        .andExpect(jsonPath("$[0].universalSegment", is(true)));
  }

  @Test
  public void testReadAllByBrandAndSegmentForNonUniversalSegment() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/footer-menu/brand/bma/segment/segment1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(3)))
        .andExpect(jsonPath("$[0].universalSegment", is(false)));
  }

  @Test
  public void testDeleteOneFotNotFound() throws Exception {
    given(repository.findById(any(String.class))).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/footer-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testDeleteOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/footer-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateFooterMenu() throws Exception {
    entity = createFooterMenu("2", false, "universal");
    given(repository.save(any(FooterMenu.class))).willReturn(entity);
    given(repository.findByBrand(anyString())).willReturn(getFooterMenuList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testUpdateFooterMenu() throws Exception {
    entity = createFooterMenu("2", false, "segment1");
    given(repository.findById("2")).willReturn(Optional.of(entity));
    given(repository.findByBrand(anyString())).willReturn(getFooterMenuList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/footer-menu/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateWithsSameId() throws Exception {
    given(repository.findById("1")).willReturn(Optional.of(entity));
    given(repository.findByBrand(anyString())).willReturn(getFooterMenuList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/footer-menu/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderMenu() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderMenuForFailed() throws Exception {
    OrderDto orderDto =
        OrderDto.builder().order(Arrays.asList("1", "2", "3")).segmentName("segment1").build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(orderDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testOrderMenuForEmptyListFailed() throws Exception {
    OrderDto orderDto =
        OrderDto.builder().segmentName("segment1").id(UUID.randomUUID().toString()).build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(orderDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testOrderMenuForEmptyIdFailed() throws Exception {
    OrderDto orderDto =
        OrderDto.builder().order(Arrays.asList("1", "2", "3")).segmentName("segment1").build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/footer-menu/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(orderDto)))
        .andExpect(status().is4xxClientError());
  }

  private static FooterMenu createFooterMenu(String id, boolean value, String segmentName) {
    FooterMenu footerMenu = new FooterMenu();
    footerMenu.setId(id);
    footerMenu.setWidgetName("football");
    footerMenu.setUniversalSegment(value);
    footerMenu.setSegmentReferences(getSegmentReference(segmentName));
    footerMenu.setBrand("bma");
    // footerMenu.setSortOrder(5 + Math.random());
    footerMenu.setLinkTitleBrand("bma");
    footerMenu.setLinkTitle("image1");

    return footerMenu;
  }

  public static List<SegmentReference> getSegmentReference(String segmentName) {
    List<SegmentReference> segmentReferences = new ArrayList<>();
    segmentReferences.add(getSegmentReference(segmentName, "10", 1));
    return segmentReferences;
  }

  private static List<SegmentReference> getSegmentReference(String[] segmentName) {
    List<SegmentReference> segmentReferences = new ArrayList<>();

    Arrays.stream(segmentName)
        .forEach(
            x -> {
              segmentReferences.add(getSegmentReference(x, "10", 1));
              segmentReferences.add(getSegmentReference(x, "10", 2));
            });
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

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("1", "2", "3"))
            .segmentName("segment1")
            .id(UUID.randomUUID().toString())
            .build();
    return orderDto;
  }

  private static List<FooterMenu> getFooterMenuList() {
    List<FooterMenu> FooterMenuList = new ArrayList<>();
    FooterMenuList.add(createFooterMenu("1", true, "universal"));
    return FooterMenuList;
  }

  private List<FooterMenu> getFooterMenuListForUniversalFalse() {
    List<FooterMenu> footerMenus = new ArrayList<>();
    footerMenus.add(createFooterMenu("1", false, "segment1"));
    footerMenus.add(createFooterMenu("2", false, "segment1"));
    return footerMenus;
  }

  private Object getSegmentEntity() {
    FooterMenu footerMenu = new FooterMenu();
    footerMenu.setId("1213131313");
    footerMenu.setWidgetName("football");
    footerMenu.setUniversalSegment(false);
    footerMenu.setSegmentReferences(getSegmentReference(new String[] {"s1"}));
    footerMenu.setBrand("bma");
    footerMenu.setInclusionList(Arrays.asList("s1,s2".split(",")));
    footerMenu.setLinkTitleBrand("coral");
    footerMenu.setLinkTitle("image1");

    return footerMenu;
  }
}
