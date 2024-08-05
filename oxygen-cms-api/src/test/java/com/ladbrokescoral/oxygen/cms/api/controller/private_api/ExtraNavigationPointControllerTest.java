package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.ExtraNavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      ExtraNavigationPointController.class,
      ExtraNavigationPointService.class,
      AutomaticUpdateService.class
    })
@AutoConfigureMockMvc(addFilters = false)
class ExtraNavigationPointControllerTest extends AbstractControllerTest {
  @MockBean ExtraNavigationPointRepository extraNavigationPointRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;

  @MockBean RGYModuleService rgyModuleService;

  @MockBean RGYConfigUploadService rgyConfigUploadService;
  private ExtraNavigationPoint entity;
  private ExtraNavigationPoint updateEntity;

  public static final String API_BASE_URL = "/v1/api/extra-navigation-points";
  public static final String EXTRA_NAVIGATION_PT_ID = "1";
  public static final String BRAND = "bma";

  private RGYModuleEntity rgyModuleEntity;

  @BeforeEach
  public void setUp() throws IOException {
    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createExtraNavPoint.json", ExtraNavigationPoint.class);
    rgyModuleEntity = createRgyModuleEntity();
    updateEntity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/updateExtraNavPoint.json", ExtraNavigationPoint.class);
    given(extraNavigationPointRepository.save(any(ExtraNavigationPoint.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(extraNavigationPointRepository).findById(any(String.class));
  }

  @Test
  void createExtraNavigationPointTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getExtraNavigationPointTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + EXTRA_NAVIGATION_PT_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateExtraNavigationPointTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + EXTRA_NAVIGATION_PT_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateExtraNavigationPointAndRgyQuickLinks() throws Exception {
    ExtraNavigationPoint existing = createExtraNavigationPoint("11", "bma");
    ExtraNavigationPoint updated = createExtraNavigationPoint("11", "bma");
    updated.setTitle("supreme");

    given(this.extraNavigationPointRepository.findById(anyString()))
        .willReturn(Optional.of(existing));
    given(this.rgyModuleService.findByBrand(anyString()))
        .willReturn(Collections.singletonList(rgyModuleEntity));
    given(this.rgyConfigUploadService.uploadToS3(anyString())).willReturn(Collections.emptyList());
    given(this.extraNavigationPointRepository.save(any(ExtraNavigationPoint.class)))
        .willAnswer(AdditionalAnswers.returnsFirstArg());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + "11")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updated)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateExtraNavigationPointWithNoRgQuickLinkUpdate() throws Exception {
    ExtraNavigationPoint existing = createExtraNavigationPoint("11", "bma");
    given(this.extraNavigationPointRepository.findById(anyString()))
        .willReturn(Optional.of(existing));
    given(this.extraNavigationPointRepository.save(any(ExtraNavigationPoint.class)))
        .willAnswer(AdditionalAnswers.returnsFirstArg());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + "11")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(existing)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findByBrandTest() throws Exception {
    List<ExtraNavigationPoint> extraNavigationPointList = new ArrayList<>();
    extraNavigationPointList.add(entity);
    when(extraNavigationPointRepository.findByBrand(any())).thenReturn(extraNavigationPointList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void deleteExtraNavigationPointTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + EXTRA_NAVIGATION_PT_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testOrderMenu() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL + "/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getAllExtraNavPtsByBrandSortedTest() {
    AutomaticUpdateService automaticUpdateService = Mockito.mock(AutomaticUpdateService.class);
    ExtraNavigationPointService extraNavigationPointService =
        Mockito.spy(
            new ExtraNavigationPointService(
                extraNavigationPointRepository, automaticUpdateService));
    when(extraNavigationPointRepository.findByBrand(any(), any()))
        .thenReturn(Collections.singletonList(entity));
    extraNavigationPointService.getAllExtraNavPtsByBrandSorted(BRAND);
    Assertions.assertEquals(BRAND, entity.getBrand());
  }

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("1", "2", "3"))
            .id(UUID.randomUUID().toString())
            .build();
    return orderDto;
  }

  private ExtraNavigationPoint createExtraNavigationPoint(String id, String brand) {
    ExtraNavigationPoint extraNavigationPoint = new ExtraNavigationPoint();
    extraNavigationPoint.setId(id);
    extraNavigationPoint.setTitle("hello");
    extraNavigationPoint.setBrand(brand);
    extraNavigationPoint.setDescription("xyz");
    extraNavigationPoint.setTargetUri("/extra");
    extraNavigationPoint.setValidityPeriodStart(Instant.now());
    extraNavigationPoint.setValidityPeriodEnd(Instant.now().plus(Duration.ofDays(1)));
    extraNavigationPoint.setFeatureTag("tag");
    return extraNavigationPoint;
  }

  private RGYModuleEntity createRgyModuleEntity() {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    rgyModuleEntity.setAliasModules(Collections.singletonList(aliasModuleNamesDto("11", "hello")));
    rgyModuleEntity.setBrand("bma");
    return rgyModuleEntity;
  }

  private AliasModuleNamesDto aliasModuleNamesDto(String id, String title) {
    AliasModuleNamesDto aliasModuleNamesDto = new AliasModuleNamesDto();
    aliasModuleNamesDto.setId(id);
    aliasModuleNamesDto.setTitle(title);
    return aliasModuleNamesDto;
  }
}
