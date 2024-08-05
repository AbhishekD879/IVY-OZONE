package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.PromotionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.PromotionModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.PromotionModuleService;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
// @Slf4j
public class PromotionModuleServiceImpl implements PromotionModuleService {

  private final CmsApiService cmsApiService;
  private final String brand;

  @Autowired
  public PromotionModuleServiceImpl(
      CmsApiService cmsApiService, @Value("${cms.brand}") String brand) {
    this.cmsApiService = cmsApiService;
    this.brand = brand;
  }

  @Override
  public PromotionModuleDto process(CompetitionModule module) {
    PromotionModuleDto moduleDto = PromotionModuleDtoMapper.INSTANCE.toDto(module);

    cmsApiService
        .findCompetitionByBrandAndUri(brand, moduleDto.getCompetitionUriFromPath())
        .map(Competition::getId)
        .flatMap(id -> cmsApiService.findPromotionsByBrandAndCompetitionId(brand, id))
        .ifPresent(moduleDto::setPromotionsData);
    return moduleDto;
  }
}
