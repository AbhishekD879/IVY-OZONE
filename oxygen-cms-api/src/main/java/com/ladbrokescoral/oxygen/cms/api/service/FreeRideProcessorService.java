package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.CreatePotsCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.dto.CreatePotsChoiceDto;
import com.ladbrokescoral.oxygen.cms.api.dto.CreatePotsQuestionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.CreatePotsRequestDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePotsDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.dto.HorseDetails;
import com.ladbrokescoral.oxygen.cms.api.dto.ViewPotResponseDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Event;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Option;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Question;
import java.util.*;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class FreeRideProcessorService {

  private ModelMapper modelMapper;

  public FreeRideProcessorService(ModelMapper modelMapper) {
    this.modelMapper = modelMapper;
  }

  public CreatePotsRequestDto prepareCreatePotsRequest(
      Optional<FreeRideCampaign> freeRideCampaign) {
    CreatePotsRequestDto createPotsRequestDto = new CreatePotsRequestDto();
    CreatePotsCampaignDto campaignDto = new CreatePotsCampaignDto();
    freeRideCampaign.ifPresent(
        (FreeRideCampaign campaign) -> {
          campaignDto.setId(campaign.getId());
          campaignDto.setName(campaign.getName());
          campaignDto.setDisplayFrom(campaign.getDisplayFrom());
          campaignDto.setDisplayTo(campaign.getDisplayTo());
          campaignDto.setQuestions(new ArrayList<>());
          campaign.getQuestionnarie().getQuestions().stream()
              .forEach(
                  (Question question) -> {
                    CreatePotsQuestionDto questionDto = new CreatePotsQuestionDto();
                    questionDto.setQuesDescription(question.getQuesDescription());
                    questionDto.setQuestionId(question.getQuestionId());
                    questionDto.setChoices(new ArrayList<>());
                    question.getOptions().stream()
                        .forEach(
                            (Option option) -> {
                              CreatePotsChoiceDto choiceDto = new CreatePotsChoiceDto();
                              choiceDto.setChoiceNo(option.getOptionId());
                              choiceDto.setProxyChoice(option.getProxyChoice());
                              choiceDto.setChoiceName(option.getOptionText());
                              questionDto.getChoices().add(choiceDto);
                            });
                    campaignDto.getQuestions().add(questionDto);
                  });
          createPotsRequestDto.setCategoryId(campaign.getEventClassInfo().getCategoryId());
          createPotsRequestDto.setEventIds(
              campaign.getEventClassInfo().getMarketPlace().stream()
                  .flatMap(e -> e.getEvents().stream().map(Event::getId))
                  .collect(Collectors.toList()));
        });
    createPotsRequestDto.setCampaign(campaignDto);
    return createPotsRequestDto;
  }

  public Map<String, FreeRidePotsDetailsDto> processViewPotsResponse(
      ResponseEntity<ViewPotResponseDto[]> response,
      Map<String, FreeRidePotsDetailsDto> responseMap) {
    Arrays.stream(response.getBody())
        .forEach(
            (ViewPotResponseDto outcomeData) -> {
              if (!responseMap.containsKey(outcomeData.getPotId())) {
                responseMap.put(
                    outcomeData.getPotId(),
                    new FreeRidePotsDetailsDto(outcomeData.getPotId(), new ArrayList<>()));
              }
              responseMap
                  .get(outcomeData.getPotId())
                  .getHorses()
                  .add(modelMapper.map(outcomeData, HorseDetails.class));
            });
    return responseMap;
  }
}
