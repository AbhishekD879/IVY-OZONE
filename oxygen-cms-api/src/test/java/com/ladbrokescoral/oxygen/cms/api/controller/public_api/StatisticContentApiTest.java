package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.repository.StatisticContentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StatisticContentPublicService;
import java.time.Duration;
import java.time.Instant;
import java.util.Collections;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@WebMvcTest(value = {StatisticContentsApi.class, StatisticContentPublicService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBeans({@MockBean(BrandService.class)})
public class StatisticContentApiTest extends AbstractControllerTest {

  @MockBean private StatisticContentRepository contentRepository;

  private StatisticContent entity;

  @Before
  public void init() {
    this.entity = getContent("bma", true);
  }

  @Test
  public void testReadByBrandAndEventIdWithNoContents() throws Exception {
    given(
            this.contentRepository.findAllByBrandAndEventIdOrderBySortOrderAsc(
                anyString(), anyString()))
        .willReturn(Collections.singletonList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.empty()));
  }

  @Test
  public void testReadByBrandAndEventId() throws Exception {
    StatisticContent content = entity;
    content.setStartTime(Instant.now());
    content.setEndTime(Instant.now().plus(Duration.ofDays(1)));
    given(
            this.contentRepository.findAllByBrandAndEventIdOrderBySortOrderAsc(
                anyString(), anyString()))
        .willReturn(Collections.singletonList(content));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrandAndEventIdNotInTimeRange() throws Exception {
    StatisticContent content = entity;
    content.setStartTime(Instant.now().plus(Duration.ofDays(1)));
    content.setEndTime(Instant.now().plus(Duration.ofDays(2)));
    given(
            this.contentRepository.findAllByBrandAndEventIdOrderBySortOrderAsc(
                anyString(), anyString()))
        .willReturn(Collections.singletonList(content));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.empty()));
  }

  private StatisticContent getContent(String brand, boolean enabled) {
    StatisticContent content = new StatisticContent();
    content.setContent("sample data");
    content.setEventId("1122");
    content.setTitle("Barcelona Vs Real Madrid");
    content.setBrand(brand);
    content.setEnabled(enabled);
    content.setStartTime(Instant.parse("2022-04-09T00:00:00.00Z"));
    content.setEndTime(Instant.parse("2022-04-09T23:59:59.00Z"));
    return content;
  }
}
