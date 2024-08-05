package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({LuckyDipMappingApi.class, LuckyDipMappingPublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class LuckyDipMappingApiTest extends AbstractControllerTest {

  @MockBean private LuckyDipMappingService luckyDipMappingService;

  List<LuckyDipMapping> existingLuckyDipMappings;

  @BeforeEach
  public void setUp() throws Exception {
    existingLuckyDipMappings =
        TestUtil.deserializeListWithJackson(
            "service/luckyDip/existingLuckyDipMappings.json", LuckyDipMapping.class);
  }

  @Test
  void getAllLuckyDipMappingsByBrandTest() throws Exception {

    given(luckyDipMappingService.getAllLuckyDipMappingsByBrand(anyString()))
        .willReturn(existingLuckyDipMappings);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/lucky-dip-mapping")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
