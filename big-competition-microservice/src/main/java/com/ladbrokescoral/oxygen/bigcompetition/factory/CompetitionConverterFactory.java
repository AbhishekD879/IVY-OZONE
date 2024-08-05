package com.ladbrokescoral.oxygen.bigcompetition.factory;

import com.ladbrokescoral.oxygen.bigcompetition.converter.CompetitionDtoConverter;
import com.ladbrokescoral.oxygen.bigcompetition.converter.CompetitionModuleDtoConverter;
import com.ladbrokescoral.oxygen.bigcompetition.converter.CompetitionSubTabDtoConverter;
import com.ladbrokescoral.oxygen.bigcompetition.converter.CompetitionTabDtoConverter;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.stereotype.Component;

@Component
@Getter
@AllArgsConstructor
public class CompetitionConverterFactory {
  private final CompetitionDtoConverter competitionDtoConverter;
  private final CompetitionTabDtoConverter competitionTabDtoConverter;
  private final CompetitionSubTabDtoConverter competitionSubTabDtoConverter;
  private final CompetitionModuleDtoConverter competitionModuleDtoConverter;
}
