package com.ladbrokescoral.oxygen.bigcompetition.converter;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionSubTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.CompetitionSubTabDtoMapper;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionSubTab;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class CompetitionSubTabDtoConverter
    implements BaseConverter<CompetitionSubTab, CompetitionSubTabDto> {

  private final CompetitionModuleDtoConverter moduleDtoConverter;

  @Autowired
  public CompetitionSubTabDtoConverter(CompetitionModuleDtoConverter moduleDtoConverter) {
    this.moduleDtoConverter = moduleDtoConverter;
  }

  @Override
  public CompetitionSubTabDto map(CompetitionSubTab competitionSubTab) {
    CompetitionSubTabDto competitionSubTabDto =
        CompetitionSubTabDtoMapper.INSTANCE.toDto(competitionSubTab);

    List<CompetitionModuleDto> modules =
        moduleDtoConverter.convert(competitionSubTab.getCompetitionModules());
    competitionSubTabDto.setCompetitionModules(modules);

    return competitionSubTabDto;
  }
}
