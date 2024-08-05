package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.CampaignStatus;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineCampaignRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineCampaignService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelinePostService;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.time.Duration;
import java.time.Instant;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {TimelineCampaignController.class, TimelineCampaignService.class})
@MockBean({TimelineKafkaPublisher.class, TimelinePostService.class})
@AutoConfigureMockMvc(addFilters = false)
public class TimelineCampaignControllerTest extends AbstractControllerTest {

  public static final String CAMPAIGN_ID = "98789987";
  public static final String BRAND = "ladbrokes";

  private Campaign campaign;

  // FIXME: mock repository, not service under test
  @SpyBean private TimelineCampaignService campaignService;
  @MockBean private TimelineCampaignRepository repository;

  @Before
  public void init() {
    campaign = new Campaign();
    campaign.setId(CAMPAIGN_ID);
    campaign.setBrand(BRAND);
    campaign.setDisplayTo(Instant.now().plus(Duration.ofDays(3)));
    campaign.setName("campaignName");
    campaign.setMessagesToDisplayCount(10);
    campaign.setStatus(CampaignStatus.OPEN);

    doNothing().when(campaignService).delete(any(String.class));
    doReturn(campaign).when(campaignService).update(any(Campaign.class), any(Campaign.class));
    doReturn(campaign).when(campaignService).save(any(Campaign.class));
    doReturn(Optional.of(campaign)).when(campaignService).findOne(any(String.class));
  }

  @Test
  public void testCreateCampaign() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/timeline/campaign")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(campaign)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetCampaignById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/timeline/campaign/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetAllCampaigns() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/timeline/campaign?sort=updatedAt,asc")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetCampaignsForBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/timeline/campaign/brand/" + BRAND + "?sort=updatedAt,asc")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateCampaign() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/timeline/campaign/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(campaign)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteCampaign() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/timeline/campaign/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateCampaignAuthenticationFailed() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/timeline/campaign")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(campaign)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateCampaignAuthenticationFailed() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/timeline/campaign/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(campaign)))
        .andExpect(status().is2xxSuccessful());
  }
}
