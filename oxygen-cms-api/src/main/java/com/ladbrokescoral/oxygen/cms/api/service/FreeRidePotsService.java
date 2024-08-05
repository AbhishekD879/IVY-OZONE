package com.ladbrokescoral.oxygen.cms.api.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.dto.CreatePotsRequestDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FreeRideMsErrorDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePotsDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ViewPotResponseDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.exception.FreeRideException;
import com.ladbrokescoral.oxygen.cms.api.exception.PotCreationException;
import com.ladbrokescoral.oxygen.cms.api.exception.UnauthorizedException;
import com.ladbrokescoral.oxygen.cms.api.repository.FreeRideCampaignRepository;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Service
@Slf4j
public class FreeRidePotsService extends AbstractService<FreeRideCampaign>
    implements FreeRideService {

  private FreeRideCampaignRepository freeRideCampaignRepository;

  private FreeRideProcessorService processorService;

  private RestTemplate restTemplate;

  private final HttpHeaders headers;

  @Value("${freeride.baseUrl}")
  private String freeRidebaseUrl;

  @Value("${freeride.secret.ladbrokes}")
  private String ladsKeyValue;

  @Value("${freeride.secret.bma}")
  private String bmaKeyValue;

  private ObjectMapper objectMapper;

  private static final String CREATE_POTS_ERROR_MSG = "Error occurred while creating pots";

  private static final String VIEW_POTS_ERROR_MSG = "Error occurred while calling viewpots api";

  public FreeRidePotsService(
      FreeRideCampaignRepository freeRideCampaignRepository,
      RestTemplate restTemplate,
      FreeRideProcessorService processorService) {
    super(freeRideCampaignRepository);
    this.freeRideCampaignRepository = freeRideCampaignRepository;
    this.restTemplate = restTemplate;
    this.processorService = processorService;
    this.headers = new HttpHeaders();
    this.objectMapper = new ObjectMapper();
  }

  public FreeRideCampaign createPots(String campaignId) {
    FreeRideCampaign updatedFreeRideCampaign = null;
    try {
      Optional<FreeRideCampaign> freeRideCampaign = freeRideCampaignRepository.findById(campaignId);
      if (freeRideCampaign.isPresent()) {
        CreatePotsRequestDto requestData =
            processorService.prepareCreatePotsRequest(freeRideCampaign);
        FreeRideCampaign updatedCampaign = freeRideCampaign.get();
        createPots(requestData, updatedCampaign.getBrand());
        updatedCampaign.setIsPotsCreated(Boolean.TRUE);
        updatedFreeRideCampaign = freeRideCampaignRepository.save(updatedCampaign);
      }
    } catch (HttpStatusCodeException ex) {
      String errMsg = ex.getMessage();
      log.error(CREATE_POTS_ERROR_MSG + " {} ", errMsg);
      int statusCode = ex.getStatusCode().value();
      try {
        String errrJsndt = Objects.nonNull(errMsg) ? errMsg.substring(errMsg.indexOf("[")) : "";
        FreeRideMsErrorDto[] errordto =
            objectMapper.readValue(errrJsndt, FreeRideMsErrorDto[].class);
        if (statusCode == HttpStatus.UNAUTHORIZED.value()) {
          throw new UnauthorizedException(
              HttpStatus.UNAUTHORIZED.name() + " User : " + errordto[0].getErrMsg());
        } else {
          throw new PotCreationException(errordto[0].getErrMsg());
        }
      } catch (UnauthorizedException unEx) {
        throw unEx;
      } catch (Exception pEx) {
        if (statusCode == HttpStatus.UNAUTHORIZED.value()) {
          throw new UnauthorizedException(HttpStatus.UNAUTHORIZED.name() + " User");
        }
        throw new PotCreationException(pEx.getMessage());
      }
    } catch (Exception ex) {
      log.error(CREATE_POTS_ERROR_MSG + " {} ", ex.getMessage());
      throw new PotCreationException(CREATE_POTS_ERROR_MSG);
    }
    return updatedFreeRideCampaign;
  }

  private void createPots(CreatePotsRequestDto requestData, String brand) {
    String requestUri = UriComponentsBuilder.fromHttpUrl(freeRidebaseUrl + "pots").toUriString();
    addHeaderFields(headers, brand, bmaKeyValue, ladsKeyValue);
    HttpEntity<CreatePotsRequestDto> request = new HttpEntity<>(requestData, headers);
    restTemplate.exchange(requestUri, HttpMethod.POST, request, Void.class);
  }

  public Collection<FreeRidePotsDetailsDto> getPotsDetails(String campaignId, String brand) {
    Map<String, FreeRidePotsDetailsDto> responseMap = new LinkedHashMap<>();
    try {
      String requestUri =
          UriComponentsBuilder.fromHttpUrl(freeRidebaseUrl + "viewpots/" + campaignId)
              .toUriString();
      addHeaderFields(headers, brand, bmaKeyValue, ladsKeyValue);
      HttpEntity<String> request = new HttpEntity<>(headers);
      ResponseEntity<ViewPotResponseDto[]> response =
          restTemplate.exchange(requestUri, HttpMethod.GET, request, ViewPotResponseDto[].class);
      responseMap = processorService.processViewPotsResponse(response, responseMap);
    } catch (HttpStatusCodeException ex) {
      String errorMsg = ex.getMessage();
      log.error(VIEW_POTS_ERROR_MSG + " {} ", errorMsg);
      try {
        String errJsnDta =
            Objects.nonNull(errorMsg) ? errorMsg.substring(errorMsg.indexOf("[")) : "";
        FreeRideMsErrorDto[] errordto =
            objectMapper.readValue(errJsnDta, FreeRideMsErrorDto[].class);
        if (ex.getStatusCode().value() == HttpStatus.UNAUTHORIZED.value()) {
          throw new UnauthorizedException(
              HttpStatus.UNAUTHORIZED.name() + " User : " + errordto[0].getErrMsg());
        } else {
          throw new FreeRideException(errordto[0].getErrMsg());
        }
      } catch (UnauthorizedException unEx) {
        throw unEx;
      } catch (Exception pException) {
        throw new FreeRideException(pException.getMessage());
      }
    } catch (Exception ex) {
      log.error(VIEW_POTS_ERROR_MSG + " {} ", ex.getMessage());
      throw new FreeRideException(VIEW_POTS_ERROR_MSG);
    }
    return responseMap.values();
  }
}
