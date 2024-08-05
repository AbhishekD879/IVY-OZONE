package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionTabService;
import com.ladbrokescoral.oxygen.cms.api.service.SportCategoryService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({Competitions.class, CompetitionService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean(CompetitionModuleService.class)
@MockBean(CompetitionTabService.class)
@MockBean(SportCategoryService.class)
public class CompetitionsTest extends AbstractControllerTest {

  @MockBean private CompetitionRepository repository;

  @MockBean private SiteServeService siteServeService;

  private Competition entity;

  @Before
  public void init() {

    entity = new Competition();

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(Competition.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testGetMarketById() throws Exception {

    given(siteServeService.getMarketById("bma", "122861380"))
        .willReturn(Optional.of(new SiteServeMarketDto()));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/competition/brand/bma/ss/market/122861380")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
