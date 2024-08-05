package com.ladbrokescoral.oxygen.betpackmp.controller;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackMessage;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackRedisOperationsImpl;
import java.util.Arrays;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@SpringBootTest
@AutoConfigureMockMvc
class RedisDataControllerTest extends AbstractControllerTest {

  @MockBean private BetPackRedisService betPackRedisService;

  @MockBean private BetPackRedisOperationsImpl betPackRedisOperations;

  @Test
  void testGetActiveBetPacks() throws Exception {
    when(betPackRedisService.getActiveBetPacks(anyString()))
        .thenReturn(new ActiveBetPacks(Arrays.asList("434", "980")));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/active-bet-packs").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testActiveBetPacksWithNullActiveBetPacks() throws Exception {
    when(betPackRedisService.getActiveBetPacks(anyString())).thenReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/active-bet-packs").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testBetPackById() throws Exception {
    BetPackMessage betPackMessage = new BetPackMessage();
    betPackMessage.setBetPackId("1245dbhek");
    when(betPackRedisOperations.getLastSavedMessage(anyString()))
        .thenReturn(Optional.of(betPackMessage));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/bet-pack/6g5ff98798xf6be")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testGetBetPackById_InvalidId() throws Exception {
    BetPackMessage betPackMessage = new BetPackMessage();
    betPackMessage.setBetPackId("1245dbhek");
    when(betPackRedisOperations.getLastSavedMessage(anyString())).thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/bet-pack/6g5ff98798xf6be")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  void testGetBetPackById() throws Exception {
    when(betPackRedisOperations.getAll()).thenReturn(Arrays.asList(new BetPackMessage()));
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/bet-packs").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
