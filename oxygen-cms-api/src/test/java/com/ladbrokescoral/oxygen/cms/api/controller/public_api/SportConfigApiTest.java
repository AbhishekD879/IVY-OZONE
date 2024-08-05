package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.SportPageConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import java.util.Arrays;
import java.util.Collections;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest({SportConfigApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class SportConfigApiTest extends AbstractControllerTest {

  private static final String CORAL_BRAND = "bma";

  @MockBean private SportCategoryPublicService service;

  @Before
  public void init() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setBrand(CORAL_BRAND);
    sportCategory.setCategoryId(16);
    sportCategory.setTier(SportTier.TIER_1);
    sportCategory.setTargetUri("sport/football");
    given(service.getSportConfig(CORAL_BRAND, 16))
        .willReturn(SportPageConfigDto.builder().config(sportCategory).build());
    given(service.getSportsConfigs(CORAL_BRAND, Arrays.asList(16, 17, 1111)))
        .willReturn(
            Collections.singletonList(SportPageConfigDto.builder().config(sportCategory).build()));
  }

  @Test
  public void shouldRetrieveConfigForSport() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-config/16")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("football")));
  }

  @Test
  public void shouldRetrieveConfigsByCategoryIds() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-config?categoryIds=16,17,1111")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("football")));
  }

  @Test
  public void shouldRetrieve404forInvalidSport() throws Exception {
    given(service.getSportConfig(CORAL_BRAND, 1111)).willThrow(new NotFoundException());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-config/1111")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }
}
