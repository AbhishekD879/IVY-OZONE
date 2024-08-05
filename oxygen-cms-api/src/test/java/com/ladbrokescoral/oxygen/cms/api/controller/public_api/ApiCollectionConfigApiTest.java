package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static com.ladbrokescoral.oxygen.cms.api.TestUtil.deserializeWithJackson;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.ApiCollectionConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ApiCollectionConfigService;
import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;
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
@WebMvcTest(value = {ApiCollectionConfigService.class, ApiCollectionConfigApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class ApiCollectionConfigApiTest extends AbstractControllerTest {

  private ApiCollectionConfig createApiCollectionConfig;

  @MockBean ApiCollectionConfigRepository apiCollectionConfigRepository;

  @Before
  public void init() throws IOException {
    createApiCollectionConfig =
        deserializeWithJackson(
            "controller/private_api/apicollectionconfig/createApiCollectionConfig.json",
            ApiCollectionConfig.class);
    given(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
  }

  @Test
  public void testToReadAllConfigMap() throws Exception {
    given(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/api-collection-config/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
