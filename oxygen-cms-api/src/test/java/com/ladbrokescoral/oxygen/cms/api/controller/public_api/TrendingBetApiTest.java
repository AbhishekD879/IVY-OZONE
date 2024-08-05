package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingBetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.TrendingBetService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      TrendingBetApi.class,
      TrendingBetService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class TrendingBetApiTest {

  @MockBean private TrendingBetRepository repository;
  @MockBean private ModelMapper mapper;
  @MockBean private AuthenticationService authenticationService;
  @MockBean private UserService userService;
  private static final String BETSLIP = "bet-slip";
  private static final String BETRECEIPT = "bet-receipt";

  private TrendingBet trendingBet;
  @Autowired private MockMvc mockMvc;

  @Test
  public void testGetTrendingBetSlipsByBrand() throws Exception {
    trendingBet = createTrendingBet("62cd9ce3fa2d927e6d9c18ad", BETSLIP);
    given(repository.findTrendingBetByBrandAndType("coral", BETSLIP))
        .willReturn(Optional.of(trendingBet));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/trending-bet/bet-slip")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetTrendingBetSlipsByBrandNoContent() throws Exception {
    given(repository.findByBrand("coral")).willReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/trending-bet/bet-slip")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testGetTrendingBetReceiptsByBrand() throws Exception {
    trendingBet = createTrendingBet("62cd9ce3fa2d927e6d9c18ad", BETRECEIPT);
    given(repository.findTrendingBetByBrandAndType("coral", BETRECEIPT))
        .willReturn(Optional.of(trendingBet));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/trending-bet/bet-receipt")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetTrendingBetReceiptsByBrandNoContent() throws Exception {
    given(repository.findByBrand("coral")).willReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/trending-bet/bet-receipt")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  private static TrendingBet createTrendingBet(String id, String type) {
    TrendingBet trendingBet = new TrendingBet();
    trendingBet.setId(id);
    trendingBet.setBrand("coral");
    trendingBet.setType(type);
    trendingBet.setActive(true);
    trendingBet.setDisplayForAllUsers(true);
    trendingBet.setMostBackedIn("24Hr");
    trendingBet.setEventStartsIn("2Hr");
    trendingBet.setBetRefreshInterval(20);
    return trendingBet;
  }
}
