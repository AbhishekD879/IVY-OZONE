package com.ladbrokescoral.oxygen.cms.api.controller;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.PRIVATE_API;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.SeoPages;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SeoPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SeoPageService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;

@WebMvcTest({SeoPages.class, SeoPageService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean(WysiwygService.class)
public class SeoPagesTest extends AbstractControllerTest {

  @MockBean private SeoPageRepository repository;

  private SeoPage entity = new SeoPage();

  @Test
  public void testCreateWithInvalidFields() throws Exception {

    given(repository.save(any(SeoPage.class))).will(AdditionalAnswers.returnsFirstArg());

    // priority cannot be empty
    executeAndVerify400Response(entity);

    entity.setPriority(2.0);

    // priority must be less than or equal to 1
    executeAndVerify400Response(entity);

    entity.setPriority(-1.0);

    // priority must be greater than or equal to 0
    executeAndVerify400Response(entity);

    entity.setPriority(1.0);

    // changefreq may not be empty
    executeAndVerify400Response(entity);

    entity.setChangefreq("daily");

    // title may not be empty
    executeAndVerify400Response(entity);

    entity.setTitle("title");

    // url may not be empty
    executeAndVerify400Response(entity);

    entity.setUrl("url");

    // brand may not be empty
    executeAndVerify400Response(entity);

    entity.setBrand("brand");

    // success. All fields are valid
    executeAndVerify200Response(entity);
  }

  private void executeAndVerify400Response(SeoPage seoPage) throws Exception {
    mockMvc
        .perform(
            post(PRIVATE_API + "/seo-page")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(seoPage)))
        .andExpect(status().is4xxClientError());
  }

  private void executeAndVerify200Response(SeoPage seoPage) throws Exception {
    mockMvc
        .perform(
            post(PRIVATE_API + "/seo-page")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(seoPage)))
        .andExpect(status().is2xxSuccessful());
  }
}
