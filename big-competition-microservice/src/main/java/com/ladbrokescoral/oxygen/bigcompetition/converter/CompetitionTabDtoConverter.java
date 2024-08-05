package com.ladbrokescoral.oxygen.bigcompetition.converter;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionSubTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.CompetitionTabDtoMapper;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionTab;
import java.util.List;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class CompetitionTabDtoConverter
    implements BaseConverter<CompetitionTab, CompetitionTabDto> {

  private final CompetitionSubTabDtoConverter subTabDtoConverter;
  private final CompetitionModuleDtoConverter moduleDtoConverter;

  @Override
  public CompetitionTabDto map(CompetitionTab competitionTab) {
    CompetitionTabDto competitionTabDto = CompetitionTabDtoMapper.INSTANCE.toDto(competitionTab);

    List<CompetitionModuleDto> modules =
        moduleDtoConverter.convert(competitionTab.getCompetitionModules());
    competitionTabDto.setCompetitionModules(modules);

    List<CompetitionSubTabDto> subTabs =
        subTabDtoConverter.convert(competitionTab.getCompetitionSubTabs());
    competitionTabDto.setCompetitionSubTabs(subTabs);

    return competitionTabDto;
  }
}
