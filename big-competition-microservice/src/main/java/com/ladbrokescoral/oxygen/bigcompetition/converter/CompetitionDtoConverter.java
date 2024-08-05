package com.ladbrokescoral.oxygen.bigcompetition.converter;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.CompetitionDtoMapper;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class CompetitionDtoConverter implements BaseConverter<Competition, CompetitionDto> {

  private CompetitionTabDtoConverter competitionTabDtoConverter;

  @Autowired
  public CompetitionDtoConverter(CompetitionTabDtoConverter competitionTabDtoConverter) {
    this.competitionTabDtoConverter = competitionTabDtoConverter;
  }

  @Override
  public CompetitionDto map(Competition competition) {
    CompetitionDto competitionDto = CompetitionDtoMapper.INSTANCE.toDto(competition);
    List<CompetitionTabDto> tabs =
        competitionTabDtoConverter.convert(competition.getCompetitionTabs());
    competitionDto.setCompetitionTabs(tabs);
    competitionDto.setSportId(competition.getSportId());
    return competitionDto;
  }
}
