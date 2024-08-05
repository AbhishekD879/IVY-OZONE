package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.ContestRequest;
import com.ladbrokescoral.oxygen.cms.api.dto.ContestStatus;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.PrizePool;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ContestPrizeService;
import com.ladbrokescoral.oxygen.cms.api.service.ContestService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import com.ladbrokescoral.oxygen.cms.api.service.showdown.ShowdownService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.beans.BeanUtils;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      ContestController.class,
      ContestService.class,
      SiteServeServiceImpl.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class ContestControllerTest extends AbstractControllerTest {

  @MockBean private ContestRepository repository;
  @MockBean private ImageService imageService;
  @MockBean private SvgImageParser svgImageParser;
  @MockBean private SiteServeApiProvider provider;
  @MockBean private ShowdownService service;
  @MockBean private SiteServerApi siteServerApi;
  @MockBean private SiteServeService siteServeService;
  @MockBean private ContestPrizeService contestPrizesService;

  private Contest entity;
  private Contest entityInvitational;
  private Contest entityNonInvitational;
  private Contest entityNoContestUrl;
  private String path = "/images/uploads/svg";
  private List<Event> events = null;
  private ContestRequest request;

  @Before
  public void init() {
    entity = createContest();
    request = new ContestRequest();
    entityInvitational = createInvitationalContest();
    events = createEvent();
    entityNonInvitational = createNonInvitationalContest();
    entityNoContestUrl = createNoContestUrl();
    BeanUtils.copyProperties(entity, request);
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.save(any(Contest.class))).will(AdditionalAnswers.returnsFirstArg());
    given(repository.findAllByBrandOrderBySortOrderAsc(anyString()))
        .willReturn(Arrays.asList(entity));
    given(provider.api(any())).willReturn(siteServerApi);
    given(siteServerApi.getCommentaryForEvent(any())).willReturn(Optional.of(events));
    given(siteServeService.getCommentsByEventId(any(String.class), any(List.class)))
        .willReturn(events);
  }

  @Test
  public void testCreateContest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/contest")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateContest_1() throws Exception {
    request.setIntialContestId("12345");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/contest")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(request)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateContest_2() throws Exception {
    request.setIntialContestId(null);
    request.setInvitationalContest(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/contest")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(request)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateContest_3() throws Exception {
    request.setIntialContestId("12345");
    request.setInvitationalContest(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/contest")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(request)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateNonInvitationalContest() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/contest/5")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entityNonInvitational)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testClonedContest() throws Exception {
    request.setInvitationalContest(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/cloneContest")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(request)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testClonedContest_1() throws Exception {
    request.setInvitationalContest(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/cloneContest")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(request)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateContestWithNoUrl() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/contest/6")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entityNoContestUrl)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contest").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    ContestStatus contestStatus = new ContestStatus();
    contestStatus.setEntriesSize(10);
    contestStatus.setReportGenerated(true);
    given(service.getContestStatus(Mockito.any(), Mockito.any()))
        .willReturn(Optional.of(contestStatus));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contest/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.brand", is("ladbrokes")))
        .andExpect(jsonPath("$.completed", is(false)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne_1() throws Exception {
    Contest contest = entity;
    contest.setEvent(null);
    given(repository.findById(any(String.class))).willReturn(Optional.of(contest));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contest/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.brand", is("ladbrokes")))
        .andExpect(jsonPath("$.completed", is(false)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne_2() throws Exception {
    Contest contest = entity;
    contest.setCompleted(true);
    given(repository.findById(any(String.class))).willReturn(Optional.of(contest));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contest/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.brand", is("ladbrokes")))
        .andExpect(jsonPath("$.completed", is(true)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne_3() throws Exception {
    given(siteServeService.getCommentsByEventId(any(String.class), any(List.class)))
        .willReturn(Collections.emptyList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contest/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.brand", is("ladbrokes")))
        .andExpect(jsonPath("$.completed", is(false)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(any(String.class))).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contest/3").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound())
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateContest() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/contest/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateContestInvitation() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/contest/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entityInvitational)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contest/brand/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/contest/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderContests() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/contest/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void uploadContestLogo() throws Exception {

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", "file".getBytes());
    given(repository.findById("1")).willReturn(Optional.of(entity));
    given(imageService.upload(anyString(), any(), eq(path)))
        .willReturn(Optional.of(getFilename("android.svg", "323566.svg")));
    Svg svg = new Svg();
    svg.setSvg("<svg>");
    given(svgImageParser.parse(any())).willReturn(Optional.of(svg));
    this.mockMvc
        .perform(
            multipart("/v1/api/contest/1/file")
                .file("contestLogo", file.getBytes())
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());

    Assert.assertNotNull(entity.getSponsorLogo());
    Assert.assertEquals("android.svg", entity.getSponsorLogo().getOriginalname());
    Assert.assertEquals("323566.svg", entity.getSponsorLogo().getFilename());
  }

  @Test
  public void deleteImage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/contest/1/file?imageType=CONTESTLOGO")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static Contest createContest() {
    Instant startDate = Instant.parse("2021-05-06T09:29:50.628Z");
    Contest contests = new Contest();
    contests.setEntryStake("1");
    contests.setSponsorLogo(getFilename("android.svg", "323566.svg"));
    contests.setId("1");
    contests.setBrand("ladbrokes");
    contests.setEvent("12345");
    contests.setStartDate(startDate);
    PrizePool prizes = new PrizePool();
    prizes.setCash("1000");
    contests.setPrizePool(prizes);
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize table = new ContestPrize();
    table.setNumberOfEntries("8");
    table.setIcon(getFilename("android.svg", "image/svg"));
    table.setText("Contest");
    contestPrizes.add(table);
    contests.setContestPrizes(contestPrizes);
    contests.setInvitationalContest(true);
    contests.setContestURL(null);
    return contests;
  }

  private static Contest createNonInvitationalContest() {
    Instant startDate = Instant.parse("2021-05-06T09:29:50.628Z");
    Contest contests = new Contest();
    contests.setEntryStake("1");
    contests.setSponsorLogo(getFilename("android.svg", "323566.svg"));
    contests.setId("1");
    contests.setBrand("ladbrokes");
    contests.setEvent("12345");
    contests.setStartDate(startDate);
    PrizePool prizes = new PrizePool();
    prizes.setCash("1000");
    contests.setPrizePool(prizes);
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize table = new ContestPrize();
    table.setNumberOfEntries("8");
    table.setIcon(getFilename("android.svg", "image/svg"));
    table.setText("Contest");
    contestPrizes.add(table);
    contests.setContestPrizes(contestPrizes);
    contests.setInvitationalContest(true);
    contests.setContestURL("test");
    return contests;
  }

  private static Contest createNoContestUrl() {
    Instant startDate = Instant.parse("2021-05-06T09:29:50.628Z");
    Contest contests = new Contest();
    contests.setEntryStake("1");
    contests.setSponsorLogo(getFilename("android.svg", "323566.svg"));
    contests.setId("1");
    contests.setBrand("ladbrokes");
    contests.setEvent("12345");
    contests.setStartDate(startDate);
    PrizePool prizes = new PrizePool();
    prizes.setCash("1000");
    contests.setPrizePool(prizes);
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize table = new ContestPrize();
    table.setNumberOfEntries("8");
    table.setIcon(getFilename("android.svg", "image/svg"));
    table.setText("Contest");
    contestPrizes.add(table);
    contests.setContestPrizes(contestPrizes);
    contests.setInvitationalContest(false);
    contests.setContestURL("test");
    return contests;
  }

  private static Contest createInvitationalContest() {
    Instant startDate = Instant.parse("2021-05-06T09:29:50.628Z");
    Contest contests = new Contest();
    contests.setEntryStake("1");
    contests.setSponsorLogo(getFilename("android.svg", "323566.svg"));
    contests.setId("1");
    contests.setBrand("ladbrokes");
    contests.setEvent("12345");
    contests.setStartDate(startDate);
    PrizePool prizes = new PrizePool();
    prizes.setCash("1000");
    contests.setPrizePool(prizes);
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize table = new ContestPrize();
    table.setNumberOfEntries("8");
    table.setIcon(getFilename("android.svg", "image/svg"));
    table.setText("Contest");
    contestPrizes.add(table);
    contests.setContestPrizes(contestPrizes);
    contests.setInvitationalContest(false);
    contests.setContestURL(null);
    return contests;
  }

  private List<Event> createEvent() {
    List<Event> events = new ArrayList<>();
    Event event = new Event();
    event.setId("12345");
    event.setIsResulted(true);
    events.add(event);
    return events;
  }

  private static Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
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
