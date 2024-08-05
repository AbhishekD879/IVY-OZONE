package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.PostStatus;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelinePostPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineCampaignService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelinePostService;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.web.config.EnableSpringDataWebSupport;
import org.springframework.http.MediaType;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({TimelinePostController.class, TimelinePostService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({TimelineKafkaPublisher.class, TimelineCampaignService.class})
@EnableSpringDataWebSupport
public class TimelinePostControllerTest extends AbstractControllerTest {

  public static final String POST_ID = "98789987";
  public static final String BRAND = "ladbrokes";

  private TimelinePost entity;

  @MockBean private SecurityContext securityContext;
  @MockBean private Authentication authentication;

  @MockBean private TimelinePostPageRepository repository;

  @Before
  public void init() {
    entity = new TimelinePost();
    entity.setPostStatus(PostStatus.DRAFT);
    entity.setBrand(BRAND);

    // TODO: bed style. use spring-security-test and @WithMockUser or @WithUserDetails
    SecurityContextHolder.setContext(securityContext);
    given(securityContext.getAuthentication()).willReturn(authentication);
    given(authentication.getPrincipal()).willReturn(User.builder().id(POST_ID).build());

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(TimelinePost.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreatingPost() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/timeline/post")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testUpdatingPostById() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/timeline/post/" + POST_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isOk());
  }

  @Test
  public void testGettingPostById() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/timeline/post/" + POST_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testDeleting() throws Exception {

    entity.setId(POST_ID);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/timeline/post/" + POST_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testGetByBrandAndCampaign() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/timeline/post/brand/ladbrokes/" + "23783246" + "?sort=createdAt")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetCountByBrandAndCampaign() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/timeline/post/brand/ladbrokes/" + "23783246" + "/count")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetByBrandAndCampaignPaginated() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/timeline/post/brand/ladbrokes/" + "23783246/0/3" + "?sort=createdAt")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
