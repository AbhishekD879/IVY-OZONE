package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackToken;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceService;
import java.io.IOException;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.BeanUtils;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      BetPackMarketPlaceController.class,
      BetPackEntity.class,
      BetPackMarketPlaceService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceControllerTest extends AbstractControllerTest {
  public static final String CORAL = "coral";
  private BetPackEntity betPackEntity = new BetPackEntity();
  private BetPackDto betPackDto;
  private BetPackEntity betPackEntities;
  private BetPackEntity betPackEntityFilterFalse;

  @MockBean BetPackMarketPlaceService betPackMarketPlaceService;
  @MockBean BetPackEnablerRepository betPackEnablerRepository;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    betPackDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackDtos.json", BetPackDto.class);
    betPackEntityFilterFalse =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackDtosFilterFalse.json",
            BetPackEntity.class);

    jsonMapper.enable(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT);
    betPackEntities =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/Betpack.json", BetPackEntity.class);

    BeanUtils.copyProperties(betPackDto, betPackEntity);
  }

  @Test
  public void testCreateBetPack() throws Exception {
    given(betPackMarketPlaceService.save(any(BetPackEntity.class))).willReturn(betPackEntity);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any())).willReturn(betPackEntity);
    given(betPackMarketPlaceService.checkActiveBetPackLimit(any(), any(BetPackDto.class)))
        .willReturn(betPackEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackDto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testCreateBetPack_IsFilterFalse() throws Exception {
    given(betPackMarketPlaceService.save(any(BetPackEntity.class)))
        .willReturn(betPackEntityFilterFalse);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any()))
        .willReturn(betPackEntityFilterFalse);

    given(betPackMarketPlaceService.checkActiveBetPackLimit(any(), any()))
        .willReturn(betPackEntityFilterFalse);
    betPackDto.setFilterBetPack(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateBetPackValidation() throws Exception {
    given(betPackMarketPlaceService.save(any(BetPackEntity.class)))
        .willReturn(betPackEntityFilterFalse);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any()))
        .willReturn(betPackEntityFilterFalse);
    betPackDto.setFilterBetPack(false);
    betPackDto.setFilterList(new ArrayList<>());
    betPackDto.setBetPackTokenList(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateBetPackValidationNull() throws Exception {
    given(betPackMarketPlaceService.save(any(BetPackEntity.class)))
        .willReturn(betPackEntityFilterFalse);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any()))
        .willReturn(betPackEntityFilterFalse);
    betPackDto.setFilterBetPack(false);
    betPackDto.setFilterList(null);
    betPackDto.setBetPackTokenList(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateBetPackValidationEmpty() throws Exception {
    given(betPackMarketPlaceService.save(any(BetPackEntity.class)))
        .willReturn(betPackEntityFilterFalse);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any()))
        .willReturn(betPackEntityFilterFalse);
    betPackDto.setFilterBetPack(false);
    List<String> list = new ArrayList<>();
    list.add(null);
    betPackDto.setFilterList(list);
    List<BetPackToken> tokenList = new ArrayList<>();
    tokenList.add(null);
    betPackDto.setBetPackTokenList(tokenList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateBetPack_IsFilterTrue_EmptyFilter() throws Exception {
    given(betPackMarketPlaceService.save(any(BetPackEntity.class)))
        .willReturn(betPackEntityFilterFalse);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any()))
        .willReturn(betPackEntityFilterFalse);
    betPackDto.setFilterList(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateBetPack_IsFilterFalse_EmptyFilter() throws Exception {
    given(betPackMarketPlaceService.save(any(BetPackEntity.class)))
        .willReturn(betPackEntityFilterFalse);
    given(betPackMarketPlaceService.checkActiveBetPackLimit(any(), any(BetPackDto.class)))
        .willReturn(betPackEntityFilterFalse);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any()))
        .willReturn(betPackEntityFilterFalse);
    betPackDto.setFilterBetPack(false);
    // betPackDto.setFilterList(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetAllBetPack() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-packs").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-packs/brand/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPack() throws Exception {
    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntities));
    given(betPackMarketPlaceService.prepareModelBeforeSave(any())).willReturn(betPackEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetActiveBetPackIds() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/active-ids/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetPack() throws Exception {
    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntity));
    given(betPackMarketPlaceService.checkActiveBetPackLimit(any(), any(BetPackDto.class)))
        .willReturn(betPackEntity);
    given(betPackMarketPlaceService.checkDateValidation(any(), any(BetPackDto.class)))
        .willReturn(betPackEntity);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any())).willReturn(betPackEntity);
    given(betPackMarketPlaceService.update(any(), any())).willReturn(betPackEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-pack/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetPackWithoutMaxExpiration() throws Exception {
    betPackEntity.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));

    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntity));
    given(betPackMarketPlaceService.checkActiveBetPackLimit(any(), any(BetPackDto.class)))
        .willReturn(betPackEntity);
    given(betPackMarketPlaceService.checkDateValidation(any(), any(BetPackDto.class)))
        .willReturn(betPackEntity);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any())).willReturn(betPackEntity);
    given(betPackMarketPlaceService.update(any(), any())).willReturn(betPackEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-pack/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetPackAfterBetpackStartDate() throws Exception {
    betPackEntity.setBetPackStartDate(Instant.now().plus(1, ChronoUnit.DAYS));
    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntity));
    given(betPackMarketPlaceService.checkActiveBetPackLimit(any(), any(BetPackDto.class)))
        .willReturn(betPackEntity);
    given(betPackMarketPlaceService.checkDateValidation(any(), any(BetPackDto.class)))
        .willReturn(betPackEntity);
    given(betPackMarketPlaceService.prepareModelBeforeSave(any())).willReturn(betPackEntity);
    given(betPackMarketPlaceService.update(any(), any())).willReturn(betPackEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-pack/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteById() throws Exception {
    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByIdAfterStartdate() throws Exception {
    betPackEntity.setBetPackStartDate(Instant.now().plus(1, ChronoUnit.DAYS));
    betPackEntity.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));
    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByIdMaxTokenExpiratonDate() throws Exception {
    betPackEntity.setBetPackStartDate(Instant.now().minus(1, ChronoUnit.DAYS));
    betPackEntity.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));
    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void testDeleteByIdInternal() throws Exception {
    given(betPackMarketPlaceService.findOne(anyString())).willReturn(Optional.of(betPackEntities));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/internal/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("1", "2", "3"))
            .id(UUID.randomUUID().toString())
            .build();
    return orderDto;
  }
}
