package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.repository.ExtraNavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ExtraNavigationPointService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ExtraNavigationPointPublicService;
import java.io.IOException;
import java.util.List;
import org.junit.Before;
import org.junit.jupiter.api.Test;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({ExtraNavigationPointApi.class, ExtraNavigationPointPublicService.class})
@MockBean(ModelMapper.class)
@AutoConfigureMockMvc(addFilters = false)
class ExtraNavigationPointApiTest extends AbstractControllerTest {

  @MockBean ExtraNavigationPointService extraNavigationPointService;
  @MockBean ExtraNavigationPointRepository extraNavigationPointRepository;

  private List<ExtraNavigationPoint> extraNavigationPointPublicDtoList;

  @Before
  public void init() throws IOException {
    ExtraNavigationPoint extraNavigationPoint =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createExtraNavPoint.json", ExtraNavigationPoint.class);
    extraNavigationPointPublicDtoList.add(extraNavigationPoint);
  }

  @Test
  void findByBrandTest() throws Exception {
    given(extraNavigationPointRepository.findByBrand(any(), any()))
        .willReturn(extraNavigationPointPublicDtoList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/extra-navigation-points")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
