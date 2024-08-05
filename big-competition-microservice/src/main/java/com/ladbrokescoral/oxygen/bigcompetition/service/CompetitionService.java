package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.bigcompetition.dto.*;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import java.util.Map;
import java.util.Optional;

public interface CompetitionService {
  Optional<CompetitionDto> findCompetitionDtoWithoutModules(String uri);

  Optional<CompetitionTabDto> findCompetitionTabDto(String id);

  Optional<CompetitionSubTabDto> findCompetitionSubTabDto(String id);

  Optional<CompetitionModuleDto> findCompetitionModuleDto(String id);

  Optional<Map<String, ParticipantWithSvgDto>> findCompetitionParticipants(String uri);
}
