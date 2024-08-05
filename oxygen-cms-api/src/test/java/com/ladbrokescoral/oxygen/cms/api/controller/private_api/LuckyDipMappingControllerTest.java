package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipMappingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({LuckyDipMappingController.class, LuckyDipMappingService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class LuckyDipMappingControllerTest extends AbstractControllerTest {

  @MockBean LuckyDipMappingRepository luckyDipMappingRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;

  private LuckyDipMapping entity;
  private LuckyDipMapping updateEntity;
  private List<LuckyDipMapping> configurationList;

  public static final String API_BASE_URL = "/v1/api";
  public static final String LDIP_ID = "1";
  public static final String BRAND = "bma";
  public static final String BRAND_LADS = "LADBROKES";

  @BeforeEach
  public void setUp() throws IOException {
    entity =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LdMappingWithNoDuplicates.json", LuckyDipMapping.class);
    updateEntity =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LDMappingUpdateEntity.json", LuckyDipMapping.class);

    configurationList = new ArrayList<>();
    given(luckyDipMappingRepository.save(any(LuckyDipMapping.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(luckyDipMappingRepository).findById(any(String.class));
  }

  @Test
  void createLuckyDipMappingTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL + "/" + BRAND + "/lucky-dip-mapping")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void createLuckyDipMappingTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL + "/" + BRAND_LADS + "/lucky-dip-mapping")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void updateLuckyDipMappingTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + BRAND + "/lucky-dip-mapping/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateLuckyDipMappingTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(
                    API_BASE_URL + "/" + BRAND_LADS + "/lucky-dip-mapping/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void findLuckyDipMappingByBrandTest() throws Exception {
    configurationList.add(updateEntity);
    given(luckyDipMappingRepository.findByBrand(any(), any())).willReturn(configurationList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/lucky-dip-mapping/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getLuckyDipMappingTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + BRAND + "/lucky-dip-mapping/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getLuckyDipMappingTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    API_BASE_URL + "/" + BRAND_LADS + "/lucky-dip-mapping/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void deleteLuckyDipMappingTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(
                    API_BASE_URL + "/" + BRAND + "/lucky-dip-mapping/" + LDIP_ID)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void deleteLuckyDipMappingTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(
                    API_BASE_URL + "/" + BRAND_LADS + "/lucky-dip-mapping/" + LDIP_ID)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void testOrder() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/lucky-dip-mapping/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  private OrderDto createOrderDto() {
    return OrderDto.builder()
        .order(Arrays.asList("1", "2", "3"))
        .id(UUID.randomUUID().toString())
        .build();
  }
}
