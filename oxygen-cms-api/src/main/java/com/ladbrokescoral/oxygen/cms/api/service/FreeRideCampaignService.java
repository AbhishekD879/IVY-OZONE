package com.ladbrokescoral.oxygen.cms.api.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.dto.FreeRideCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FreeRideMsErrorDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Option;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Question;
import com.ladbrokescoral.oxygen.cms.api.exception.DeleteCampaignException;
import com.ladbrokescoral.oxygen.cms.api.exception.UnauthorizedException;
import com.ladbrokescoral.oxygen.cms.api.repository.FreeRideCampaignRepository;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Service
@Slf4j
public class FreeRideCampaignService extends AbstractService<FreeRideCampaign>
    implements FreeRideService {

  private FreeRideCampaignRepository freeRideCampaignRepository;

  private ModelMapper modelMapper;

  private RestTemplate restTemplate;

  private final HttpHeaders headers;

  @Value("${freeride.baseUrl}")
  private String freeRideBaseUrl;

  @Value("${freeride.secret.ladbrokes}")
  private String ladsKeyValue;

  @Value("${freeride.secret.bma}")
  private String bmaKeyValue;

  private static final String DELETE_CAMPAIGN_ERROR_MSG = "Error occurred while deleting campaign";

  private enum Constants {
    ONE(1),
    TWO(2),
    THREE(3),
    FIVE(5),
    SIX(6),
    EIGHT(8),
    NINE(9);

    private Integer value;

    Constants(Integer value) {
      this.value = value;
    }

    public Integer getValue() {
      return this.value;
    }
  }

  public FreeRideCampaignService(
      FreeRideCampaignRepository freeRideCampaignRepository,
      ModelMapper modelMapper,
      RestTemplate restTemplate) {
    super(freeRideCampaignRepository);
    this.freeRideCampaignRepository = freeRideCampaignRepository;
    this.modelMapper = modelMapper;
    this.restTemplate = restTemplate;
    this.headers = new HttpHeaders();
  }

  public List<FreeRideCampaignDto> findAllByBrand(String brand, Sort sort) {
    return freeRideCampaignRepository.findByBrand(brand, sort).stream()
        .map(e -> modelMapper.map(e, FreeRideCampaignDto.class))
        .collect(Collectors.toList());
  }

  public List<FreeRideCampaign> getAllCampaignByBrand(String brand) {
    return freeRideCampaignRepository.findByBrand(brand);
  }

  public List<FreeRideCampaign> findAllByBrandAndDisplayFromBetween(
      String brand, Instant displayFrom) {
    Instant fromDate = displayFrom.minus(0, ChronoUnit.DAYS).truncatedTo(ChronoUnit.DAYS);
    Instant todate = displayFrom.plus(1, ChronoUnit.DAYS).truncatedTo(ChronoUnit.DAYS);
    return freeRideCampaignRepository.findAllByBrandAndDisplayFromBetween(brand, fromDate, todate);
  }

  public void mapProxyChoice(FreeRideCampaign freeRideCampaign) {
    freeRideCampaign.getQuestionnarie().getQuestions().stream()
        .forEach(
            (Question question) ->
                question.getOptions().stream()
                    .forEach(
                        (Option option) -> {
                          option.setProxyChoice(option.getOptionId());
                          if (question.getQuestionId().equals(Constants.ONE.getValue())
                              && option.getOptionId().equals(Constants.THREE.getValue())) {
                            option.setProxyChoice(Constants.TWO.getValue());
                          } else if (question.getQuestionId().equals(Constants.TWO.getValue())
                              && option.getOptionId().equals(Constants.SIX.getValue())) {
                            option.setProxyChoice(Constants.FIVE.getValue());
                          } else if (question.getQuestionId().equals(Constants.THREE.getValue())
                              && option.getOptionId().equals(Constants.NINE.getValue())) {
                            option.setProxyChoice(Constants.EIGHT.getValue());
                          }
                        }));
  }

  public void deleteFreeRideMsCampaign(String campaignId, String brand) {
    try {
      String requestUri =
          UriComponentsBuilder.fromHttpUrl(freeRideBaseUrl + "/campaign/" + campaignId)
              .toUriString();
      addHeaderFields(headers, brand, bmaKeyValue, ladsKeyValue);
      HttpEntity<String> request = new HttpEntity<>(headers);
      restTemplate.exchange(requestUri, HttpMethod.DELETE, request, Void.class);
    } catch (HttpStatusCodeException ex) {
      String errorMsg = ex.getMessage();
      log.error(DELETE_CAMPAIGN_ERROR_MSG + " {} ", errorMsg);
      try {
        ObjectMapper objectMapper = new ObjectMapper();
        String errJsnDta =
            Objects.nonNull(errorMsg) ? errorMsg.substring(errorMsg.indexOf("[")) : "";
        FreeRideMsErrorDto[] errordto =
            objectMapper.readValue(errJsnDta, FreeRideMsErrorDto[].class);
        if (ex.getStatusCode().value() == HttpStatus.UNAUTHORIZED.value()) {
          throw new UnauthorizedException(
              HttpStatus.UNAUTHORIZED.name() + " User : " + errordto[0].getErrMsg());
        } else {
          throw new DeleteCampaignException(errordto[0].getErrMsg());
        }
      } catch (UnauthorizedException unEx) {
        throw unEx;
      } catch (Exception pException) {
        throw new DeleteCampaignException(pException.getMessage());
      }
    } catch (Exception ex) {
      log.error(DELETE_CAMPAIGN_ERROR_MSG + " {} ", ex.getMessage());
      throw new DeleteCampaignException(DELETE_CAMPAIGN_ERROR_MSG);
    }
  }
}
