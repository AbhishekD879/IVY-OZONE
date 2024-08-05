package com.ladbrokescoral.oxygen.bigcompetition.service.impl;

import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildAbbreviation;
import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildName;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionSubTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantWithSvgDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.factory.CompetitionConverterFactory;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.CompetitionFilterOutDisabledMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.CompetitionService;
import com.ladbrokescoral.oxygen.bigcompetition.util.Utils;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

@Service
public class CompetitionServiceImpl implements CompetitionService {

  private final CompetitionConverterFactory converterFactory;
  private final CmsApiService cmsApiService;
  private final String brand;

  public CompetitionServiceImpl(
      CompetitionConverterFactory converterFactory,
      CmsApiService cmsApiService,
      @Value("${cms.brand}") String brand) {
    this.converterFactory = converterFactory;
    this.cmsApiService = cmsApiService;
    this.brand = brand;
  }

  @Override
  public Optional<CompetitionDto> findCompetitionDtoWithoutModules(String uri) {
    Utils.newRelicLogTransaction("/BigComp-findCompetitionDtoWithoutModules");
    return cmsApiService
        .findCompetitionByBrandAndUri(brand, uri)
        .flatMap(CompetitionFilterOutDisabledMapper::filterOutDisabledWithOutModules)
        .map(converterFactory.getCompetitionDtoConverter()::convert);
  }

  @Override
  public Optional<CompetitionTabDto> findCompetitionTabDto(String id) {
    Utils.newRelicLogTransaction("/BigComp-findCompetitionTabDto");
    return cmsApiService
        .findCompetitionTabById(id)
        .flatMap(CompetitionFilterOutDisabledMapper::filterOutDisabled)
        .map(converterFactory.getCompetitionTabDtoConverter()::convert);
  }

  @Override
  public Optional<CompetitionSubTabDto> findCompetitionSubTabDto(String id) {
    Utils.newRelicLogTransaction("/BigComp-findCompetitionSubTabDto");
    return cmsApiService
        .findCompetitionSubTabById(id)
        .flatMap(CompetitionFilterOutDisabledMapper::filterOutDisabled)
        .map(converterFactory.getCompetitionSubTabDtoConverter()::convert);
  }

  @Override
  public Optional<CompetitionModuleDto> findCompetitionModuleDto(String id) {
    Utils.newRelicLogTransaction("/BigComp-findCompetitionModuleDto");
    return cmsApiService
        .findCompetitionModuleById(id)
        .flatMap(CompetitionFilterOutDisabledMapper::filterOutDisabled)
        .map(converterFactory.getCompetitionModuleDtoConverter()::convert);
  }

  @Override
  public Optional<Map<String, ParticipantWithSvgDto>> findCompetitionParticipants(String uri) {
    return cmsApiService
        .findCompetitionByBrandAndUri(brand, uri)
        .map(this::mapCompetitionParticipant);
  }

  public Map<String, ParticipantWithSvgDto> mapCompetitionParticipant(Competition competition) {
    List<CompetitionParticipant> participants = competition.getCompetitionParticipants();
    Assert.isTrue(!participants.isEmpty(), "participants in the competition is empty");
    return participants.stream()
        .collect(
            Collectors.toMap(
                CompetitionParticipant::getObName,
                p ->
                    ParticipantWithSvgDto.builder()
                        .name(buildName(p))
                        .abbreviation(buildAbbreviation(p))
                        .svgId(p.getSvgId())
                        .svg(p.getSvg())
                        .build()));
  }
}
