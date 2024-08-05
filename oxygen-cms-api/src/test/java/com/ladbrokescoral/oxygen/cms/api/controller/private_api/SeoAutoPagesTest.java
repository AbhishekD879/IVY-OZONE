package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.PRIVATE_API;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SeoAutoPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SeoAutoPageService;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({SeoAutoPages.class, SeoAutoPageService.class})
@AutoConfigureMockMvc(addFilters = false)
public class SeoAutoPagesTest extends AbstractControllerTest {

  @MockBean private SeoAutoPageRepository repository;

  private SeoAutoPage entity = new SeoAutoPage();

  @Test
  public void testCreateWithvalidFields() throws Exception {
    entity.setId("1");
    entity.setBrand("BMA");
    entity.setUri("/event");
    entity.setMetaTitle("test");
    entity.setMetaDescription("test");
    given(repository.save(any(SeoAutoPage.class))).will(AdditionalAnswers.returnsFirstArg());
    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.findByBrand("BMA")).willReturn(Arrays.asList(entity));
    given(repository.findAllByBrand("BMA")).willReturn(Arrays.asList(entity));
    testPostSeoAutoPage(entity);
    testPutSeoAutoPage(entity);
    testDeleteSeoAutoPage();
    testGetAllByBrandSeoAutoPage();
  }

  private void testPostSeoAutoPage(SeoAutoPage seoAutoPage) throws Exception {
    mockMvc
        .perform(
            MockMvcRequestBuilders.post(PRIVATE_API + "/seo-auto-page")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(seoAutoPage)))
        .andExpect(status().is2xxSuccessful());
  }

  public void testPutSeoAutoPage(SeoAutoPage seoAutoPage) throws Exception {
    mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/seo-auto-page/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(seoAutoPage)))
        .andExpect(status().is2xxSuccessful());
  }

  public void testGetAllByBrandSeoAutoPage() throws Exception {
    mockMvc.perform(get("/v1/api/seo-auto-page/brand/BMA")).andExpect(status().is2xxSuccessful());
  }

  public void testDeleteSeoAutoPage() throws Exception {
    mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/seo-auto-page/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
