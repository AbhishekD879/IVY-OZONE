package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import com.ladbrokescoral.oxygen.cms.api.repository.CountryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.CountryService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CountryPublicService;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({CountryApi.class, CountryPublicService.class, CountryService.class})
@AutoConfigureMockMvc(addFilters = false)
public class CountryApiTest extends AbstractControllerTest {

  @MockBean private CountryRepository repository;

  private Country entity;

  @Before
  public void init() {

    entity = new Country();

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(Country.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testFindByBrand() throws Exception {

    List<Country> dbCountryList =
        TestUtil.deserializeListWithJackson("controller/public_api/countries.json", Country.class);

    given(repository.findByBrand("bma")).willReturn(dbCountryList);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/countries-settings")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk())
        .andExpect(
            content()
                .json(
                    "[{'val': 'GB', 'phoneAreaCode': '+44', 'label': 'United Kingdom'},"
                        + "{'val': 'AX', 'phoneAreaCode': '+358', 'label': 'Aland Islands'}]"));
  }
}
