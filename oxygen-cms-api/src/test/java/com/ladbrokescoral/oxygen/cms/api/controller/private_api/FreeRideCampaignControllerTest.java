package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertNotNull;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.CreatePotsRequestDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ViewPotResponseDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.repository.FreeRideCampaignRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideCampaignService;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRidePotsService;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideProcessorService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Matchers;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.NestedServletException;

@SuppressWarnings("deprecation")
@WebMvcTest({
  FreeRideCampaignController.class,
  FreeRideCampaignService.class,
  FreeRidePotsService.class,
  FreeRideProcessorService.class
})
@MockBean(ModelMapper.class)
@AutoConfigureMockMvc(addFilters = false)
public class FreeRideCampaignControllerTest extends AbstractControllerTest {

  @MockBean private FreeRideCampaignRepository repository;

  @MockBean private RestTemplate restTemplate;

  private FreeRideCampaign entity;

  private FreeRideCampaign updateCampaign;

  private FreeRideCampaign createPotsInfo;

  private ViewPotResponseDto viewPotResponseDto;

  private List<FreeRideCampaign> campaignList;

  public static final String CAMPAIGN_ID = "6113873f03e1756af760b586";
  public static final String API_BASE_URL = "/v1/api/freeride/campaign";
  public static final String JSON_INPUT_BASE_URL = "controller/private_api/free_ride/";
  public static final String ERROR_MSG =
      "[{\"errMsg\":\"Secret not matched BMA\",\"path\":\"/v1/api/\"}]";
  public static final String LADBROKES = "ladbrokes";
  public static final String BMA = "bma";

  @Before
  public void init() throws IOException {

    entity =
        TestUtil.deserializeWithJackson(
            JSON_INPUT_BASE_URL + "createCampaign.json", FreeRideCampaign.class);

    updateCampaign =
        TestUtil.deserializeWithJackson(
            JSON_INPUT_BASE_URL + "updateCampaign.json", FreeRideCampaign.class);

    createPotsInfo =
        TestUtil.deserializeWithJackson(
            JSON_INPUT_BASE_URL + "createPots.json", FreeRideCampaign.class);

    viewPotResponseDto =
        TestUtil.deserializeWithJackson(
            JSON_INPUT_BASE_URL + "viewPots.json", ViewPotResponseDto.class);

    campaignList = new ArrayList<>();
    campaignList.add(entity);

    given(repository.save(any(FreeRideCampaign.class))).will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(repository).findById(any(String.class));
  }

  @Test
  public void createCampaignTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void campaingAlreadyExistTest() throws Exception {
    given(repository.findAllByBrandAndDisplayFromBetween(anyString(), any(), any()))
        .willReturn(campaignList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateCampaignTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + CAMPAIGN_ID + "/" + false)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateCampaign)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateCampaignWithDateChangedAndCampaingNotExistTest() throws Exception {
    given(repository.findAllByBrandAndDisplayFromBetween(anyString(), any(), any()))
        .willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + CAMPAIGN_ID + "/" + true)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateCampaign)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateCampaignWithDateChangedAndCampaingExistTest() throws Exception {
    given(repository.findAllByBrandAndDisplayFromBetween(anyString(), any(), any()))
        .willReturn(campaignList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + CAMPAIGN_ID + "/" + true)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateCampaign)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void getCampaignDetailsTest() throws Exception {
    given(repository.findOne(any())).willReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getCampaignsByBrandTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + LADBROKES + "?sort=updatedAt,asc")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteLadsCampaignTest() throws Exception {
    given(
            restTemplate.exchange(
                eq("/delete"),
                eq(HttpMethod.DELETE),
                Matchers.<HttpEntity<String>>any(),
                eq(Void.class)))
        .willReturn(new ResponseEntity<>(HttpStatus.OK));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteCoralCampaignTest() throws Exception {
    given(
            restTemplate.exchange(
                eq("/delete"),
                eq(HttpMethod.DELETE),
                Matchers.<HttpEntity<String>>any(),
                eq(Void.class)))
        .willReturn(new ResponseEntity<>(HttpStatus.OK));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/brand/" + BMA + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteCmpgn401StatusCodeTest() throws Exception {
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<Void>>any()))
        .thenThrow(new HttpClientErrorException(HttpStatus.UNAUTHORIZED, ERROR_MSG));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void deleteCmpgn503StatusCodeTest() throws Exception {
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<Void>>any()))
        .thenThrow(new HttpClientErrorException(HttpStatus.SERVICE_UNAVAILABLE, ERROR_MSG));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteCmpgn500WithNullErrorMsgTest() throws Exception {
    HttpClientErrorException httpClientErrorException =
        new HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR, null);
    httpClientErrorException = Mockito.spy(httpClientErrorException);
    Mockito.doReturn(null).when(httpClientErrorException).getMessage();
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<Void>>any()))
        .thenThrow(httpClientErrorException);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteCmpgnFailureest() throws Exception {
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<Void>>any()))
        .thenThrow(new NullPointerException());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createPotsPots() throws Exception {
    given(repository.findById(CAMPAIGN_ID)).willReturn(Optional.of(createPotsInfo));
    given(
            restTemplate.exchange(
                eq("/createpots"),
                eq(HttpMethod.POST),
                Matchers.<HttpEntity<CreatePotsRequestDto>>any(),
                eq(Void.class)))
        .willReturn(new ResponseEntity<>(HttpStatus.OK));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/createpots/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test(expected = NestedServletException.class)
  public void createPotsWithEmptyData() throws Exception {
    given(repository.findById(CAMPAIGN_ID)).willReturn(Optional.empty());
    given(
            restTemplate.exchange(
                eq("/createpots"),
                eq(HttpMethod.POST),
                Matchers.<HttpEntity<CreatePotsRequestDto>>any(),
                eq(Void.class)))
        .willReturn(new ResponseEntity<>(HttpStatus.OK));
    this.mockMvc.perform(
        MockMvcRequestBuilders.get(API_BASE_URL + "/createpots/" + CAMPAIGN_ID)
            .contentType(MediaType.APPLICATION_JSON));
  }

  @Test
  public void createPots500Failure() throws Exception {
    given(repository.findById(CAMPAIGN_ID))
        .willThrow(new HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR, ERROR_MSG));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/createpots/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createPots401Failure() throws Exception {
    given(repository.findById(CAMPAIGN_ID))
        .willThrow(new HttpClientErrorException(HttpStatus.UNAUTHORIZED, ERROR_MSG));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/createpots/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createPots401WithNullMsgFailure() throws Exception {
    HttpClientErrorException httpClientErrorException =
        new HttpClientErrorException(HttpStatus.UNAUTHORIZED, null);
    httpClientErrorException = Mockito.spy(httpClientErrorException);
    Mockito.doReturn(null).when(httpClientErrorException).getMessage();
    given(repository.findById(CAMPAIGN_ID)).willThrow(httpClientErrorException);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/createpots/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createPots503Failure() throws Exception {
    given(repository.findById(CAMPAIGN_ID))
        .willThrow(new ResourceAccessException(HttpStatus.SERVICE_UNAVAILABLE.toString()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/createpots/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void viewPotsLadsSuccessTest() throws Exception {
    ViewPotResponseDto[] responseArray = new ViewPotResponseDto[1];
    responseArray[0] = viewPotResponseDto;
    HttpHeaders headers = new HttpHeaders();
    headers.set("USER_NAME", "TEST");
    ResponseEntity<ViewPotResponseDto[]> responseEntity =
        new ResponseEntity<>(responseArray, headers, HttpStatus.OK);
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<ViewPotResponseDto[]>>any()))
        .thenReturn(responseEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    API_BASE_URL + "/viewpots/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void viewPotsCoralsSuccessTest() throws Exception {
    ViewPotResponseDto[] responseArray = new ViewPotResponseDto[2];
    responseArray[0] = viewPotResponseDto;
    responseArray[1] = viewPotResponseDto;
    HttpHeaders headers = new HttpHeaders();
    headers.set("USER_NAME", "TEST");
    ResponseEntity<ViewPotResponseDto[]> responseEntity =
        new ResponseEntity<>(responseArray, headers, HttpStatus.OK);
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<ViewPotResponseDto[]>>any()))
        .thenReturn(responseEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/viewpots/brand/" + BMA + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void viewPots401Test() throws Exception {
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<ViewPotResponseDto[]>>any()))
        .thenThrow(new HttpClientErrorException(HttpStatus.UNAUTHORIZED, ERROR_MSG));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    API_BASE_URL + "/viewpots/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void viewPots500WithNullMsgTest() throws Exception {
    HttpClientErrorException httpClientErrorException =
        new HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR, null);
    httpClientErrorException = Mockito.spy(httpClientErrorException);
    Mockito.doReturn(null).when(httpClientErrorException).getMessage();
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<ViewPotResponseDto[]>>any()))
        .thenThrow(httpClientErrorException);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    API_BASE_URL + "/viewpots/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void viewPots500Test() throws Exception {
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<ViewPotResponseDto[]>>any()))
        .thenThrow(new HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR, ERROR_MSG));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    API_BASE_URL + "/viewpots/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void viewPots500WithEmptyErrorTest() throws Exception {
    when(restTemplate.exchange(
            Matchers.anyString(),
            Matchers.any(HttpMethod.class),
            Matchers.<HttpEntity<?>>any(),
            Matchers.<Class<ViewPotResponseDto[]>>any()))
        .thenThrow(new HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR, ""));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    API_BASE_URL + "/viewpots/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void viewPotsFailureTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    API_BASE_URL + "/viewpots/brand/" + LADBROKES + "/" + CAMPAIGN_ID)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void getAllCampaingByBrandTest() throws Exception {
    FreeRideCampaignService freeRideCampaignService =
        Mockito.spy(new FreeRideCampaignService(repository, null, restTemplate));
    List<FreeRideCampaign> campaignList = freeRideCampaignService.getAllCampaignByBrand(BMA);
    assertNotNull(campaignList);
  }
}
