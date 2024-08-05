package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import com.ladbrokescoral.oxygen.cms.api.repository.RacingEdpMarketRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.RacingEdpMarketService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RacingEdpMarketPublicService;
import java.util.Arrays;
import java.util.Collections;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      RacingEdpMarketsApi.class,
      RacingEdpMarketPublicService.class,
      RacingEdpMarketService.class
    })
@AutoConfigureMockMvc(addFilters = false)
@MockBeans({@MockBean(BrandService.class)})
public class RacingEdpMarketsApiTest extends AbstractControllerTest {
  @MockBean private RacingEdpMarketRepository repository;
  private RacingEdpMarket entity;

  @Before
  public void init() {
    entity = new RacingEdpMarket();
    entity.setId("1");
    entity.setName("WIN");
    entity.setBrand("bma");
    entity.setDescription("Win is Racing Edp Market");
    entity.setBirDescription("Win is Racing Edp Bir Description");
    given(repository.findAllByBrandOrderBySortOrderAsc(anyString()))
        .willReturn(Arrays.asList(entity));
  }

  @Test
  public void testByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/racing-edp-markets")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.[0].id", is("1")))
        .andExpect(jsonPath("$.[0].name", is("WIN")))
        .andExpect(jsonPath("$.[0].brand", is("bma")))
        .andExpect(jsonPath("$.[0].description", is("Win is Racing Edp Market")))
        .andExpect(jsonPath("$.[0].birDescription", is("Win is Racing Edp Bir Description")));
  }

  @Test
  public void testByBrandForEmpty() throws Exception {
    given(repository.findAllByBrandOrderBySortOrderAsc(anyString()))
        .willReturn(Collections.emptyList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/racing-edp-markets")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(status().isNoContent());
  }
}
