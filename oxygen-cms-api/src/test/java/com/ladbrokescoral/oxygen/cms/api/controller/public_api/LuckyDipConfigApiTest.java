package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipConfiguration;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipConfigPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({LuckyDipConfigApi.class, LuckyDipConfigPublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class LuckyDipConfigApiTest extends AbstractControllerTest {
  @MockBean private LuckyDipConfigService luckyDipConfigService;
  @MockBean private LuckyDipConfigRepository luckyDipConfigRepository;

  private List<LuckyDipConfiguration> lDipFieldsConfigList;
  private LuckyDipConfiguration entity;

  @BeforeEach
  public void setUp() throws Exception {
    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createLuckyDipConfig.json", LuckyDipConfiguration.class);
    lDipFieldsConfigList = new ArrayList<>();
    lDipFieldsConfigList.add(entity);
  }

  @Test
  void getAllLuckyDipFieldsConfigByBrandTest() throws Exception {

    given(luckyDipConfigRepository.findByBrand(any())).willReturn(lDipFieldsConfigList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/luckydip")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
