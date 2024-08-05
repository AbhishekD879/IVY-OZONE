package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.OtfGameTabs;
import com.ladbrokescoral.oxygen.cms.api.repository.OtfGameTabsRepository;
import com.ladbrokescoral.oxygen.cms.api.service.OtfGameTabsService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OtfGameTabPublicService;
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

@WebMvcTest({OtfGameTabsApi.class, OtfGameTabPublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class OtfGameTabsApiTest extends AbstractControllerTest {

  @MockBean private OtfGameTabsService otfGameTabsService;
  @MockBean OtfGameTabsRepository otfGameTabsRepository;

  private List<OtfGameTabs> otfGamesTabList;

  @BeforeEach
  public void setUp() throws Exception {
    OtfGameTabs entity = new OtfGameTabs();
    entity.setBrand("ladbrokes");
    otfGamesTabList = new ArrayList<>();
    otfGamesTabList.add(entity);
    given(otfGameTabsRepository.findByBrand(any())).willReturn(otfGamesTabList);
  }

  @Test
  void findAllByBrandTest() throws Exception {
    given(otfGameTabsService.findByBrand(any())).willReturn(otfGamesTabList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/one-two-free/otf-tab-config")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
