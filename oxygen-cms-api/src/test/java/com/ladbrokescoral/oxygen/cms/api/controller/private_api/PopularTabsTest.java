package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularTab;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.PopularTabService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.TrendingTabService;
import java.util.*;
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
      PopularTabs.class,
      PopularTabService.class,
      TrendingTabService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class PopularTabsTest extends AbstractControllerTest {

  @MockBean private TrendingTabRepository trendingTabRepository;

  @MockBean private PopularTabRepository popularTabRepository;
  private PopularTab entity;

  @Before
  public void init() {
    entity = createPopularTab();

    given(popularTabRepository.findById(anyString())).willReturn(Optional.of(entity));
    given(popularTabRepository.save(any(PopularTab.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(trendingTabRepository.findById(anyString())).willReturn(Optional.of(new TrendingTab()));
  }

  @Test
  public void testReadByOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("popularbets")));
  }

  @Test
  public void testCreate() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdate() throws Exception {

    entity.setPopularTabName("For-You personalized bets");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/popular-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("For-You personalized bets")));
  }

  @Test
  public void testDelete() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/popular-tab/5552086fd1de60906cff4478")
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
            MockMvcRequestBuilders.post("/v1/api/popular-tab/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  private static PopularTab createPopularTab() {
    PopularTab popularTab = new PopularTab();
    popularTab.setPopularTabName("popularbets");
    return popularTab;
  }
}
