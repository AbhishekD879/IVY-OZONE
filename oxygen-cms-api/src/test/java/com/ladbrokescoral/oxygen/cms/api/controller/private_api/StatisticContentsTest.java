package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketType;
import com.ladbrokescoral.oxygen.cms.api.exception.MarketTypeInvalidException;
import com.ladbrokescoral.oxygen.cms.api.exception.SiteServEventAndMarketValidationException;
import com.ladbrokescoral.oxygen.cms.api.exception.StatisticalContentNotUniqueException;
import com.ladbrokescoral.oxygen.cms.api.repository.StatisticContentRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.StatisticContentService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.time.Instant;
import java.util.*;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@WebMvcTest(
    value = {StatisticContents.class, StatisticContentService.class, MasterSlaveExecutor.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBeans({@MockBean(BrandService.class), @MockBean(ScheduledTaskExecutor.class)})
class StatisticContentsTest extends AbstractControllerTest {

  @MockBean private StatisticContentRepository contentRepository;

  @MockBean private SiteServeApiProvider siteServeApiProvider;

  @MockBean private SiteServerApi siteServerApi;

  private StatisticContent entity;

  private Event event;

  private Market market;

  @BeforeEach
  public void init() {
    this.event = getOBEvent();
    this.market = getOBMarket();
    this.entity = getStatisticContent("bma", true);
    given(this.contentRepository.findById(any())).willReturn(Optional.of(entity));
    given(this.contentRepository.save(any())).will(AdditionalAnswers.returnsFirstArg());
    given(siteServeApiProvider.api(anyString())).willReturn(siteServerApi);
  }

  @Test
  void testGetEventTitle() throws Exception {
    given(
            this.siteServerApi.getEventToMarketForEvent(
                any(List.class), any(Optional.class), any(Optional.class), anyBoolean()))
        .willReturn(Optional.of(Collections.singletonList(event)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/bma/1111")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(
            MockMvcResultMatchers.jsonPath(
                "$.eventTitle", Matchers.is("Barcelona Vs Real Madrid")));
  }

  @Test
  void testGetEventTitleWithoutMarketIds() throws Exception {
    Event event = this.event;
    event.setChildren(Collections.emptyList());
    given(
            this.siteServerApi.getEventToMarketForEvent(
                any(List.class), any(Optional.class), any(Optional.class), anyBoolean()))
        .willReturn(Optional.of(Collections.singletonList(event)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/bma/1111")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.marketIds", Matchers.hasSize(0)));
  }

  @Test
  void testGetEventTitleNoEventInOB() throws Exception {
    given(
            this.siteServerApi.getEventToMarketForEvent(
                any(List.class), any(Optional.class), any(Optional.class), anyBoolean()))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/bma/1111")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is5xxServerError())
        .andExpect(
            mvcResult ->
                Assertions.assertTrue(
                    mvcResult.getResolvedException()
                        instanceof SiteServEventAndMarketValidationException));
  }

  @Test
  void testCreateError() throws Exception {
    StatisticContent content = new StatisticContent();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(content)))
        .andExpect(MockMvcResultMatchers.status().isBadRequest());
  }

  @Test
  void testCreate1() throws Exception {
    given(this.siteServerApi.getEventToMarketForMarket(anyString()))
        .willReturn(Optional.of(getOBMarket()));
    List<StatisticContent> list = new ArrayList<>();
    given(
            this.contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
                anyString(), any(), any(), any()))
        .willReturn(Optional.of(list));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(MockMvcResultMatchers.status().isCreated())
        .andExpect(MockMvcResultMatchers.jsonPath("$.title", Matchers.is("Man Vs Liv")));
  }

  @CsvSource({
    "2023-01-20T01:00:00.00Z,2023-01-20T22:59:59.00Z",
    "2023-01-20T01:00:00.00Z,2023-01-20T23:59:59.00Z",
    "2023-01-20T00:00:00.00Z,2023-01-20T22:59:59.00Z",
    "2023-01-20T23:59:59.00Z,2023-01-20T23:59:59.00Z",
    "2023-01-20T00:00:00.00Z,2023-01-20T23:59:59.00Z",
    "2023-01-19T00:00:00.00Z,2023-01-21T23:59:59.00Z"
  })
  @ParameterizedTest
  void testCreateFailureCases(String startTime, String endTime) throws Exception {
    List<StatisticContent> existingModels = new ArrayList<>();
    existingModels.add(this.entity);
    StatisticContent model = getStatisticContent("bma", true);
    model.setStartTime(Instant.parse(startTime));
    model.setEndTime(Instant.parse(endTime));
    given(
            contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
                anyString(), anyString(), anyString(), any()))
        .willReturn(Optional.of(existingModels));
    given(siteServerApi.getEventToMarketForMarket(anyString())).willReturn(Optional.of(market));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(model)))
        .andExpect(
            mvcResult ->
                Assertions.assertTrue(
                    mvcResult.getResolvedException()
                        instanceof StatisticalContentNotUniqueException));
  }

  @CsvSource({
    "2023-01-19T00:59:59.00Z,2023-01-19T22:59:59.00Z",
    "2023-01-21T00:00:00.00Z,2023-01-22T23:59:59.00Z"
  })
  @ParameterizedTest
  void testCreateCase5SuccessFull(String startTime, String endTime) throws Exception {
    List<StatisticContent> existingModels = new ArrayList<>();
    existingModels.add(this.entity);
    StatisticContent model = getStatisticContent("bma", true);
    model.setStartTime(Instant.parse(startTime));
    model.setEndTime(Instant.parse(endTime));
    given(
            contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
                anyString(), anyString(), anyString(), any()))
        .willReturn(Optional.of(existingModels));
    given(siteServerApi.getEventToMarketForMarket(anyString())).willReturn(Optional.of(market));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(model)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  void testCreateForNoMarketInOB() throws Exception {
    given(siteServerApi.getEventToMarketForMarket(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(MockMvcResultMatchers.status().is5xxServerError())
        .andExpect(
            mvcResult ->
                Assertions.assertTrue(
                    mvcResult.getResolvedException()
                        instanceof SiteServEventAndMarketValidationException));
  }

  @Test
  void testCreateForNoEventForRespectedMarket() throws Exception {
    Market market = this.market;
    market.setEventId("3435");
    given(siteServerApi.getEventToMarketForMarket(anyString())).willReturn(Optional.of(market));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(MockMvcResultMatchers.status().is5xxServerError())
        .andExpect(
            mvcResult ->
                Assertions.assertTrue(
                    mvcResult.getResolvedException()
                        instanceof SiteServEventAndMarketValidationException));
  }

  @Test
  void testCreateForInvalidMarketType() throws Exception {
    StatisticContent content = this.entity;
    content.setMarketType(MarketType.PB);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(content)))
        .andExpect(MockMvcResultMatchers.status().isConflict())
        .andExpect(
            result ->
                Assertions.assertTrue(
                    result.getResolvedException() instanceof MarketTypeInvalidException));
  }

  @Test
  void testCreateForInvalidMarketTypeForLads() throws Exception {

    StatisticContent content = this.entity;
    content.setBrand("ladbrokes");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(content)))
        .andExpect(MockMvcResultMatchers.status().isConflict())
        .andExpect(
            result ->
                Assertions.assertTrue(
                    result.getResolvedException() instanceof MarketTypeInvalidException));
  }

  @Test
  void testCreateForValidMarketType() throws Exception {
    given(this.siteServerApi.getEventToMarketForMarket(anyString()))
        .willReturn(Optional.of(getOBMarket()));
    StatisticContent content = this.entity;
    content.setBrand("ladbrokes");
    content.setMarketType(MarketType.PB);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content/")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(content)))
        .andExpect(MockMvcResultMatchers.status().isCreated());
  }

  @Test
  void testUpdateContent() throws Exception {
    given(this.contentRepository.findByIdAndBrand(any(), any())).willReturn(Optional.of(entity));
    StatisticContent cs = entity;
    cs.setContent("updated content");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(cs)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.content", Matchers.is("updated content")));
  }

  @Test
  void testUpdateContentErrorForChangeEventId() throws Exception {
    given(this.contentRepository.findByIdAndBrand(any(), any())).willReturn(Optional.of(entity));
    StatisticContent sc = getStatisticContent("bma", true);
    sc.setEventId("3333");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(sc)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.eventId", Matchers.is("1111")));
  }

  @Test
  void testUpdateContentErrorForChangeMarketId() throws Exception {
    given(this.contentRepository.findByIdAndBrand(any(), any())).willReturn(Optional.of(entity));
    StatisticContent sc = getStatisticContent("bma", true);
    sc.setMarketId("3333");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(sc)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.marketId", Matchers.is("2222")));
  }

  @Test
  void testUpdateContentForCase1() throws Exception {

    List<StatisticContent> contents = new ArrayList<>();
    StatisticContent model = getStatisticContent("bma", true);
    model.setId("5555");
    model.setMarketType(MarketType.OB);
    contents.add(model);

    StatisticContent model1 = getStatisticContent("bma", true);
    model1.setMarketType(MarketType.OB);

    given(this.contentRepository.findByIdAndBrand(anyString(), anyString()))
        .willReturn(Optional.of(this.entity));
    given(
            this.contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
                anyString(), anyString(), anyString(), any()))
        .willReturn(Optional.of(contents));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(model1)))
        .andExpect(
            mvcResult ->
                Assertions.assertTrue(
                    mvcResult.getResolvedException()
                        instanceof StatisticalContentNotUniqueException));
  }

  @Test
  void testUpdateContentForCase2SuccessFull() throws Exception {

    given(this.contentRepository.findByIdAndBrand(anyString(), anyString()))
        .willReturn(Optional.of(this.entity));
    given(
            this.contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
                anyString(), anyString(), anyString(), any()))
        .willReturn(Optional.of(Collections.emptyList()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  void testUpdateContentForCase3() throws Exception {

    List<StatisticContent> contents = new ArrayList<>();
    StatisticContent model = getStatisticContent("bma", true);
    model.setId(null);
    model.setMarketType(MarketType.OB);
    contents.add(model);

    given(this.contentRepository.findByIdAndBrand(anyString(), anyString()))
        .willReturn(Optional.of(this.entity));
    given(
            this.contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
                anyString(), anyString(), anyString(), any()))
        .willReturn(Optional.of(contents));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(
            mvcResult ->
                Assertions.assertTrue(
                    mvcResult.getResolvedException() instanceof IllegalArgumentException));
  }

  @Test
  void testUpdateContentForCase4() throws Exception {

    List<StatisticContent> contents = new ArrayList<>();
    StatisticContent model = getStatisticContent("bma", true);
    model.setId("1122");
    model.setMarketType(MarketType.OB);
    contents.add(model);

    given(this.contentRepository.findByIdAndBrand(anyString(), anyString()))
        .willReturn(Optional.of(this.entity));
    given(
            this.contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
                anyString(), anyString(), anyString(), any()))
        .willReturn(Optional.of(contents));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", Matchers.is("1122")))
        .andExpect(MockMvcResultMatchers.jsonPath("$.title", Matchers.is("Man Vs Liv")));
  }

  @Test
  void testReadOneNotFound() throws Exception {
    given(this.contentRepository.findById(any())).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().isNotFound());
  }

  @Test
  void testDelete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().isNoContent());
  }

  @Test
  void testDeleteNotFound() throws Exception {
    given(this.contentRepository.findById(any())).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/statistic-content/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().isNotFound());
  }

  @Test
  void testReadByEventId() throws Exception {
    given(this.contentRepository.findByEventId(any()))
        .willReturn(Collections.singletonList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/event/1111")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.[0].title", Matchers.is("Man Vs Liv")));
  }

  @Test
  void testReadByEventIdNoContent() throws Exception {
    given(this.contentRepository.findByEventId(any())).willReturn(Collections.emptyList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/event/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().isNoContent());
  }

  @Test
  void testReadAllByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  void testReadAll() throws Exception {
    given(this.contentRepository.findAll()).willReturn(Collections.singletonList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.[0].title", Matchers.is("Man Vs Liv")));
  }

  @Test
  void testReadAllWithNoContent() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/statistic-content")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().isNoContent());
  }

  @Test
  void testOrder() throws Exception {
    OrderDto orderDto = OrderDto.builder().id("11").order(Arrays.asList("1", "2", "3")).build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/statistic-content/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(orderDto)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  private StatisticContent getStatisticContent(String brand, boolean enabled) {
    StatisticContent content = new StatisticContent();
    content.setId("1122");
    content.setBrand(brand);
    content.setEnabled(enabled);
    content.setContent("Sample Content");
    content.setTitle("Man Vs Liv");
    content.setEventId("1111");
    content.setMarketId("2222");
    content.setStartTime(Instant.parse("2023-01-20T00:00:00.00Z"));
    content.setEndTime(Instant.parse("2023-01-20T23:59:59.00Z"));
    content.setMarketType(MarketType.OB);
    return content;
  }

  private Event getOBEvent() {
    Event event = new Event();
    event.setId("1111");
    event.setName("Barcelona Vs Real Madrid");
    Market market = new Market();
    market.setId("2222");
    Children children = new Children();
    children.setMarket(market);
    event.setChildren(Collections.singletonList(children));
    return event;
  }

  private Market getOBMarket() {
    Market market = new Market();
    market.setId("2222");
    market.setEventId("1111");
    return market;
  }
}
