package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipV2ConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipV2ConfigService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.AdditionalAnswers;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({LuckyDipV2ConfigController.class, LuckyDipV2ConfigService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class LuckyDipV2ConfigControllerTest extends AbstractControllerTest {

  @MockBean LuckyDipV2ConfigRepository luckyDipConfigRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;

  private LuckyDipV2Config entity;
  private LuckyDipV2Config updateEntity;
  private List<LuckyDipV2Config> configurationList;

  public static final String API_BASE_URL = "/v1/api";
  public static final String LDIP_ID = "1";
  public static final String BRAND = "ladbrokes";
  public static final String BRAND_BMA = "bma";
  private static final String TYPE_ID = "Type ID";

  @BeforeEach
  public void setUp() throws IOException {
    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createLuckyDipV2Config.json", LuckyDipV2Config.class);

    updateEntity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/updateLuckyDipV2Config.json", LuckyDipV2Config.class);

    configurationList = new ArrayList<>();
    given(luckyDipConfigRepository.save(any(LuckyDipV2Config.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(luckyDipConfigRepository).findById(any(String.class));
  }

  @Test
  void createLuckyDipConfigTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL + "/" + BRAND + "/lucky-dip")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void createLuckyDipConfigTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL + "/" + BRAND_BMA + "/lucky-dip")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void updateLuckyDipConfigTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + BRAND + "/lucky-dip/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateLuckyDipConfigTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + BRAND_BMA + "/lucky-dip/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void findLuckyDipConfigByBrandTest() throws Exception {
    configurationList.add(updateEntity);
    given(luckyDipConfigRepository.findByBrand(any(), any())).willReturn(configurationList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/lucky-dip/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getLuckyDipConfigTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + BRAND + "/lucky-dip/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getLuckyDipConfigTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + BRAND_BMA + "/lucky-dip/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void deleteLuckyDipConfigTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + BRAND + "/lucky-dip/" + LDIP_ID)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void deleteLuckyDipConfigTestWithException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + BRAND_BMA + "/lucky-dip/" + LDIP_ID)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void getLDByBrandAndLDConfigLevelIdTest() {
    LuckyDipV2ConfigService luckyDipConfigService =
        new LuckyDipV2ConfigService(luckyDipConfigRepository, null);
    when(luckyDipConfigRepository.findByBrandAndLuckyDipConfigLevelId(any(), eq("1972")))
        .thenReturn(Optional.of(entity));
    Optional<LuckyDipV2Config> luckyDipConfiguration =
        luckyDipConfigService.getLDByBrandAndLDConfigLevelId(BRAND, "1972");
    Assertions.assertNotNull(luckyDipConfiguration);
  }

  @Test
  void getInitDataTest() throws Exception {
    LuckyDipV2ConfigService luckyDipV2ConfigService =
        new LuckyDipV2ConfigService(luckyDipConfigRepository, new ModelMapper());
    Method method = LuckyDipV2ConfigService.class.getDeclaredMethod("getInitData", String.class);
    method.setAccessible(true);
    method.invoke(luckyDipV2ConfigService, BRAND);
    Assertions.assertNotNull(luckyDipV2ConfigService);
  }

  @Test
  void getInitDataTestEventId() throws Exception {
    entity.setLuckyDipConfigLevel(TYPE_ID);
    updateEntity.setLuckyDipConfigLevel("Event");
    LuckyDipV2ConfigService luckyDipV2ConfigService =
        new LuckyDipV2ConfigService(luckyDipConfigRepository, new ModelMapper());
    when(luckyDipV2ConfigService.findByBrand(any()))
        .thenReturn(Arrays.asList(entity, updateEntity));
    Method method = LuckyDipV2ConfigService.class.getDeclaredMethod("getInitData", String.class);
    method.setAccessible(true);
    method.invoke(luckyDipV2ConfigService, BRAND);
    Assertions.assertNotNull(luckyDipV2ConfigService);
  }
}
