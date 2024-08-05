package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.EventClassInfo;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Option;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Question;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Questionnarie;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideCampaignService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideCampaignPublicService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({FreeRideCampaignApi.class, FreeRideCampaignPublicService.class})
@MockBean(ModelMapper.class)
@AutoConfigureMockMvc(addFilters = false)
public class FreeRideCampaignApiTest extends AbstractControllerTest {

  @MockBean private FreeRideCampaignService freeRideCampaignService;

  private FreeRideCampaign entity;

  private List<FreeRideCampaign> campaignList;

  public static final String BRAND = "ladbrokes";

  @Before
  public void init() throws IOException {
    entity = new FreeRideCampaign();
    entity.setName(BRAND);
    entity.setQuestionnarie(new Questionnarie());
    entity.getQuestionnarie().setQuestions(new ArrayList<>());
    entity.getQuestionnarie().getQuestions().add(new Question());
    entity.getQuestionnarie().setSummaryMsg("FreeRide");
    entity.getQuestionnarie().getQuestions().get(0).setOptions(new ArrayList<Option>());
    entity.setEventClassInfo(new EventClassInfo());
    campaignList = new ArrayList<>();
    campaignList.add(entity);
  }

  @Test
  public void getTodayCampaignByBrandTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/" + BRAND + "/freeride-campaign")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
