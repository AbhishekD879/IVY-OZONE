package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.HighlightCarouselModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.HighlightCorosolModuleMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.HighlightCarouselService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.springframework.stereotype.Service;

@Service
public class HighlightCarouselServiceImpl implements HighlightCarouselService {
  @Override
  public HighlightCarouselModuleDto process(CompetitionModule module) {
    return HighlightCorosolModuleMapper.INSTANCE.toDto(module);
  }
}
