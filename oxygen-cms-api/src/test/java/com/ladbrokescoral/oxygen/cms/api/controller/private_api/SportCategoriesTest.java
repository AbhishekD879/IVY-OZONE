package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService;
import com.ladbrokescoral.oxygen.cms.api.service.SportCategoryService;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.ArrayList;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({SportCategories.class})
@AutoConfigureMockMvc(addFilters = false)
public class SportCategoriesTest extends AbstractControllerTest {

  @MockBean private TierCategoriesCache tierCategoriesCache;
  @MockBean private SportCategoryService SportCategoryService;
  @MockBean private SportCategoryRepository sportCategoryRepository;
  @MockBean private SiteServerApi siteServerApi;
  @MockBean private SiteServeApiProvider siteServeApiProvider;
  @MockBean private CompetitionService competitionService;
  private SportCategory sportCategoryEntity;

  @Before
  public void init() {
    sportCategoryEntity = new SportCategory();
    given(sportCategoryRepository.findById(anyString()))
        .willReturn(Optional.of(sportCategoryEntity));
    given(sportCategoryRepository.save(any(SportCategory.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(siteServeApiProvider.api("bma")).willReturn(siteServerApi);
    given(siteServerApi.getEventToOutcomeForOutcome(anyList(), any(SimpleFilter.class), anyList()))
        .willReturn(Optional.of(new ArrayList<>()));
  }

  @Test
  public void testReadAllSportNameByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-category/sport-name/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testreadByBrandAndSegmentName() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-category/brand/ladbrokes/segment/falcons")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
