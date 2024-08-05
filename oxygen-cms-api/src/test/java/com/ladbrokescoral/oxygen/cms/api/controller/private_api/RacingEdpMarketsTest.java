package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import com.ladbrokescoral.oxygen.cms.api.exception.RacingEdpValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.RacingEdpMarketRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.RacingEdpMarketService;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      RacingEdpMarkets.class,
      RacingEdpMarketService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
@MockBeans({@MockBean(BrandService.class)})
public class RacingEdpMarketsTest extends AbstractControllerTest {

  @MockBean private RacingEdpMarketRepository repository;
  private RacingEdpMarket entity;

  @Before
  public void init() {
    entity = createMarket("1", true);
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.save(any(RacingEdpMarket.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateRacingEdpMarketError() throws Exception {
    RacingEdpMarket dto = new RacingEdpMarket(); // empty object
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/racing-edp-market")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError())
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testCreateMarket() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/racing-edp-market")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateMarket() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/racing-edp-market/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/racing-edp-market/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.name", is("win")))
        .andExpect(jsonPath("$.brand", is("coral")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(any(String.class))).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/racing-edp-market/3")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound())
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/racing-edp-market")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/racing-edp-market/brand/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/racing-edp-market/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateMarketForError() throws Exception {
    entity.setId("2");
    given(repository.findById("2")).willReturn(Optional.of(entity));
    given(repository.findByName(anyString())).willReturn(getRacingEdpMarketList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/racing-edp-market/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError())
        .andExpect(
            result ->
                assertTrue(result.getResolvedException() instanceof RacingEdpValidationException))
        .andExpect(
            result ->
                assertEquals(
                    "Validation Failed with the Reason: There May be More than two items with same name or Market with same name in repo posses duplicate fields",
                    result.getResolvedException().getMessage()));
  }

  @Test
  public void testCreateDuplicateMarketError() throws Exception {
    entity.setId("2");
    given(repository.save(any(RacingEdpMarket.class))).willReturn(entity);
    given(repository.findByName(anyString())).willReturn(getRacingEdpMarketList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/racing-edp-market")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError())
        .andExpect(
            result ->
                assertTrue(result.getResolvedException() instanceof RacingEdpValidationException))
        .andExpect(
            result ->
                assertEquals(
                    "Validation Failed with the Reason: There May be More than two items with same name or Market with same name in repo posses duplicate fields",
                    result.getResolvedException().getMessage()));
  }

  @Test
  public void testCreateMarketWithDiffHRandGH() throws Exception {
    entity = createMarket("2", false);
    given(repository.save(any(RacingEdpMarket.class))).willReturn(entity);
    given(repository.findByName(anyString())).willReturn(getRacingEdpMarketList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/racing-edp-market")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testUpdateMarketWithDiffHRAndGH() throws Exception {
    entity = createMarket("2", false);
    given(repository.findById("2")).willReturn(Optional.of(entity));
    given(repository.findByName(anyString())).willReturn(getRacingEdpMarketList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/racing-edp-market/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateMarketForErrorsWithDiffGH() throws Exception {
    entity.setId("2");
    entity.setGh(false);
    given(repository.findById("2")).willReturn(Optional.of(entity));
    given(repository.findByName(anyString())).willReturn(getRacingEdpMarketList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/racing-edp-market/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError())
        .andExpect(
            result ->
                assertTrue(result.getResolvedException() instanceof RacingEdpValidationException))
        .andExpect(
            result ->
                assertEquals(
                    "Validation Failed with the Reason: There May be More than two items with same name or Market with same name in repo posses duplicate fields",
                    result.getResolvedException().getMessage()));
  }

  @Test
  public void testCreateMoreThanTwoMarketsError() throws Exception {
    entity = createMarket("3", false);
    List<RacingEdpMarket> list = getRacingEdpMarketList();
    list.add(createMarket("2", false));
    given(repository.save(any(RacingEdpMarket.class))).willReturn(entity);
    given(repository.findByName(anyString())).willReturn(list);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/racing-edp-market")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError())
        .andExpect(
            result ->
                assertTrue(result.getResolvedException() instanceof RacingEdpValidationException))
        .andExpect(
            result ->
                assertEquals(
                    "Validation Failed with the Reason: There May be More than two items with same name or Market with same name in repo posses duplicate fields",
                    result.getResolvedException().getMessage()));
  }

  @Test
  public void testUpdateOnlyBySameID() throws Exception {
    given(repository.findById("1")).willReturn(Optional.of(entity));
    given(repository.findByName(anyString())).willReturn(getRacingEdpMarketList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/racing-edp-market/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderMarket() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/racing-edp-market/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  private static RacingEdpMarket createMarket(String id, boolean value) {
    RacingEdpMarket market = new RacingEdpMarket();
    market.setId(id);
    market.setName("win");
    market.setBrand("coral");
    market.setDescription("");
    market.setBirDescription("");
    market.setGh(value);
    market.setHr(value);
    return market;
  }

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("1", "2", "3"))
            .id(UUID.randomUUID().toString())
            .build();
    return orderDto;
  }

  private static List<RacingEdpMarket> getRacingEdpMarketList() {
    List<RacingEdpMarket> racingEdpMarketList = new ArrayList<>();
    racingEdpMarketList.add(createMarket("1", true));
    return racingEdpMarketList;
  }
}
