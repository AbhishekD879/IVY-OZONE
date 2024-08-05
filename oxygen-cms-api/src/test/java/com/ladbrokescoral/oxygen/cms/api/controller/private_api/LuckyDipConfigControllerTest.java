package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipConfiguration;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipConfigService;
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

@WebMvcTest({LuckyDipConfigController.class, LuckyDipConfigService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class LuckyDipConfigControllerTest extends AbstractControllerTest {

  @MockBean LuckyDipConfigRepository luckyDipConfigRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;

  private LuckyDipConfiguration entity;
  private LuckyDipConfiguration updateEntity;
  private List<LuckyDipConfiguration> configurationList;

  public static final String API_BASE_URL = "/v1/api/luckydip";
  public static final String LDIP_ID = "1";
  public static final String BRAND = "ladbrokes";

  @BeforeEach
  public void setUp() throws IOException {
    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createLuckyDipConfig.json", LuckyDipConfiguration.class);

    updateEntity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/updateLuckyDipConfig.json", LuckyDipConfiguration.class);

    configurationList = new ArrayList<>();
    given(luckyDipConfigRepository.save(any(LuckyDipConfiguration.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(luckyDipConfigRepository).findById(any(String.class));
  }

  @Test
  void createLuckyDipConfigTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateLuckyDipConfigTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + LDIP_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findLuckyDipConfigByBrandTest() throws Exception {
    configurationList.add(updateEntity);
    given(luckyDipConfigRepository.findByBrand(any())).willReturn(configurationList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findLuckyDipConfigByBrandTestWhenNotPresent() throws Exception {
    given(luckyDipConfigRepository.findByBrand(any())).willReturn(configurationList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
