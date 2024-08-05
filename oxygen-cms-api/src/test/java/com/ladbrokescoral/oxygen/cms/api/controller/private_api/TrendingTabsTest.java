package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.TrendingTabService;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      TrendingTabs.class,
      TrendingTabService.class,
      SportTabService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class TrendingTabsTest extends AbstractControllerTest {

  @MockBean private TrendingTabRepository trendingTabRepository;

  @MockBean private SportTabRepository sportTabRepository;

  @MockBean private PopularTabRepository popularTabRepository;
  private TrendingTab entity;

  @Before
  public void init() {
    entity = createTrendingTab();

    given(trendingTabRepository.findById(anyString())).willReturn(Optional.of(entity));
    given(trendingTabRepository.save(any(TrendingTab.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(sportTabRepository.findById(anyString())).willReturn(Optional.of(new SportTab()));
  }

  @Test
  public void testReadByOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/trending-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("popularbets")));
  }

  @Test
  public void testCreate() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/trending-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdate() throws Exception {

    entity.setTrendingTabName("For-You");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/trending-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("For-You")));
  }

  @Test
  public void testDelete() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/trending-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Collections.singletonList("-1"))
            .id(UUID.randomUUID().toString())
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/trending-tab/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  private static TrendingTab createTrendingTab() {
    TrendingTab trendingTab = new TrendingTab();
    trendingTab.setTrendingTabName("popularbets");
    trendingTab.setPopularTabs(Arrays.asList(new PopularTab()));
    return trendingTab;
  }
}
