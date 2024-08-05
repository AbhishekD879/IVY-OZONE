package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTabMarket;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
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
      SportTabs.class,
      SportTabService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class SportTabsTest extends AbstractControllerTest {

  @MockBean private SportTabRepository repository;

  @MockBean private TrendingTabRepository trendingTabRepository;

  @MockBean private PopularTabRepository popularTabRepository;
  private SportTab entity;

  @Before
  public void init() {

    entity = createSportTab();

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(SportTab.class))).will(AdditionalAnswers.returnsFirstArg());

    given(repository.findAllByBrandAndSportIdOrderBySortOrderAsc("bma", 16))
        .willReturn(Collections.singletonList(entity));
  }

  @Test
  public void testReadByOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("Outrights")));
  }

  @Test
  public void testReadAllByBrandAndSport() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-tab/brand/bma/sport/16")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("Outrights")));
  }

  @Test
  public void testUpdate() throws Exception {

    entity.setDisplayName("Outrights-updated");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("Outrights-updated")));
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
            MockMvcRequestBuilders.post("/v1/api/sport-tab/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateTrendingTab() throws Exception {

    SportTab sportTab =
        TestUtil.deserializeWithJackson(
            "controller/private_api/TrendingTab/TrendingTab.json", SportTab.class);
    given(popularTabRepository.save(any())).will(AdditionalAnswers.returnsFirstArg());
    given(trendingTabRepository.save(any())).will(AdditionalAnswers.returnsFirstArg());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(sportTab)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateTrendingTabNotPOPULARBETS() throws Exception {

    SportTab sportTab =
        TestUtil.deserializeWithJackson(
            "controller/private_api/TrendingTab/TrendingTab.json", SportTab.class);
    sportTab.setName("coupons");
    given(popularTabRepository.save(any())).will(AdditionalAnswers.returnsFirstArg());
    given(trendingTabRepository.save(any())).will(AdditionalAnswers.returnsFirstArg());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-tab/5552086fd1de60906cff4478")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(sportTab)))
        .andExpect(status().is2xxSuccessful());
  }

  private static SportTab createSportTab() {
    List<SportTabMarket> marketsNames = new ArrayList<>();
    SportTabMarket sportTabMarket = new SportTabMarket();
    sportTabMarket.setTemplateMarketName("marketOne");
    sportTabMarket.setTitle("market1");
    SportTabMarket sportTabMarket1 = new SportTabMarket();
    sportTabMarket1.setTemplateMarketName("marketOne");
    sportTabMarket1.setTitle("market2");
    marketsNames.add(sportTabMarket);
    marketsNames.add(sportTabMarket1);

    return SportTab.builder()
        .name("outrights")
        .displayName("Outrights")
        .sortOrder(4.0)
        .enabled(true)
        .brand("bma")
        .sportId(16)
        .marketsNames(marketsNames)
        .trendingTabs(Arrays.asList(new TrendingTab()))
        .build();
  }
}
