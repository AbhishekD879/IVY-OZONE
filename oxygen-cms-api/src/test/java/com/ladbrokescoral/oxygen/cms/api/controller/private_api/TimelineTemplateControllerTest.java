package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Template;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelinePostPageRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineTemplateRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheServiceProvider;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineTemplateService;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {TimelineTemplateController.class, TimelineTemplateService.class})
@MockBean({
  BrandCacheServiceProvider.class,
  ImageService.class,
  SvgImageService.class,
  SvgImageParser.class
})
@AutoConfigureMockMvc(addFilters = false)
public class TimelineTemplateControllerTest extends AbstractControllerTest {

  public static final String TEMPLATE_ID = "5f047bea198b8025a62ec39d";
  public static final String BRAND = "ladbrokes";

  private Template template;

  // FIXME: mock repository, not service under test
  @SpyBean private TimelineTemplateService templateService;
  @MockBean private TimelineTemplateRepository repository;
  @MockBean private TimelinePostPageRepository postRepository;

  @Before
  public void init() {
    template = new Template();
    template.setId(TEMPLATE_ID);

    doReturn(template).when(templateService).save(any(Template.class));
    doReturn(Optional.of(template)).when(templateService).findOne(any(String.class));
  }

  @Test
  public void testCreate() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/timeline/template")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(template)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testGetById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/timeline/template/" + TEMPLATE_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testUpdate() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/timeline/template/" + TEMPLATE_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(template)))
        .andExpect(status().isOk());
  }

  @Test
  public void testDelete() throws Exception {
    when(postRepository.findByTemplateId(any())).thenReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/timeline/template/" + TEMPLATE_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }
}
