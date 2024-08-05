package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipV2ConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipV2ConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipV2ConfigPublicProcessor;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipV2ConfigPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({
  LuckyDipV2ConfigApi.class,
  LuckyDipV2ConfigPublicService.class,
  LuckyDipV2ConfigService.class,
  LuckyDipV2ConfigPublicProcessor.class
})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class LuckyDipV2ConfigApiTest extends AbstractControllerTest {
  @MockBean private LuckyDipV2ConfigRepository luckyDipConfigRepository;
  @MockBean private SiteServeApiProvider siteServeApiProvider;
  @MockBean private SiteServerApi siteServerApi;

  private List<LuckyDipV2Config> lDipFieldsConfigList;
  private LuckyDipV2Config entity;
  private Event event;
  private static final String EVENT_ID = "8070616";
  private static final String TYPE_ID = "442";
  private static final String CATEGORY_ID = "16";
  public static final String API_BASE_URL = "/cms/api/ladbrokes/lucky-dip";

  @BeforeEach
  public void setUp() throws Exception {
    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createLuckyDipV2Config.json", LuckyDipV2Config.class);

    event =
        TestUtil.deserializeWithJackson(
            "controller/private_api/validateSSIds/event_from_ss.json", Event.class);

    lDipFieldsConfigList = new ArrayList<>();
    lDipFieldsConfigList.add(entity);
  }

  @Test
  void getAllLuckyDipConfigByBrandAndEvent() throws Exception {
    given(siteServeApiProvider.api(any())).willReturn(siteServerApi);
    given(siteServerApi.getEvent(any(), (Boolean) any())).willReturn(Optional.of(event));
    given(luckyDipConfigRepository.findByBrandAndLuckyDipConfigLevelId(any(), eq(EVENT_ID)))
        .willReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + EVENT_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getAllLuckyDipConfigByBrandAndEventAtTypeLevel() throws Exception {
    given(siteServeApiProvider.api(any())).willReturn(siteServerApi);
    given(siteServerApi.getEvent(any(), (Boolean) any())).willReturn(Optional.of(event));
    given(luckyDipConfigRepository.findByBrandAndLuckyDipConfigLevelId(any(), eq(TYPE_ID)))
        .willReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + EVENT_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getAllLuckyDipConfigByBrandAndEventAtCategoryLevel() throws Exception {
    given(siteServeApiProvider.api(any())).willReturn(siteServerApi);
    given(siteServerApi.getEvent(any(), (Boolean) any())).willReturn(Optional.of(event));
    given(luckyDipConfigRepository.findByBrandAndLuckyDipConfigLevelId(any(), eq(CATEGORY_ID)))
        .willReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + EVENT_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getAllActiveLuckyDipConfigByBrand() throws Exception {
    List<LuckyDipV2Config> luckyDipV2Configs =
        TestUtil.deserializeWithJacksonToType(
            "controller/private_api/lucky-dip-config.json",
            new TypeReference<List<LuckyDipV2Config>>() {});
    given(luckyDipConfigRepository.findAllByBrandAndStatusTrue(any()))
        .willReturn(luckyDipV2Configs);
    this.mockMvc
        .perform(MockMvcRequestBuilders.get(API_BASE_URL).contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
