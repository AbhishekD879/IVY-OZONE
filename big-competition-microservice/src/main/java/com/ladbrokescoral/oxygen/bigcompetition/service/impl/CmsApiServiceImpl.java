package com.ladbrokescoral.oxygen.bigcompetition.service.impl;

import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.util.Utils;
import com.ladbrokescoral.oxygen.cms.client.api.CmsApiClient;
import com.ladbrokescoral.oxygen.cms.client.model.*;
import java.util.Optional;
import lombok.AllArgsConstructor;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class CmsApiServiceImpl implements CmsApiService {

  private final CmsApiClient cmsApiClient;

  @Override
  @Cacheable(value = "competition", key = "{ #root.methodName, #uri }", unless = "#result == null")
  public Optional<Competition> findCompetitionByBrandAndUri(String brand, String uri) {
    Utils.newRelicLogTransaction("/CMS-findCompetitionByBrandAndUri");
    return cmsApiClient.findCompetitionByBrandAndUri(brand, uri);
  }

  @Override
  @Cacheable(
      value = "competitionTab",
      key = "{ #root.methodName, #id }",
      unless = "#result == null")
  public Optional<CompetitionTab> findCompetitionTabById(String id) {
    Utils.newRelicLogTransaction("/CMS-findCompetitionTabById");
    return cmsApiClient.findCompetitionTabById(id);
  }

  @Override
  @Cacheable(
      value = "competitionSubTab",
      key = "{ #root.methodName, #id }",
      unless = "#result == null")
  public Optional<CompetitionSubTab> findCompetitionSubTabById(String id) {
    Utils.newRelicLogTransaction("/CMS-findCompetitionSubTabById");
    return cmsApiClient.findCompetitionSubTabById(id);
  }

  @Override
  @Cacheable(
      value = "competitionModule",
      key = "{ #root.methodName, #id }",
      unless = "#result == null")
  public Optional<CompetitionModule> findCompetitionModuleById(String id) {
    Utils.newRelicLogTransaction("/CMS-findCompetitionModuleById");
    return cmsApiClient.findCompetitionModuleById(id);
  }

  @Override
  @Cacheable(
      value = "competitionPromotions",
      key = "{ #root.methodName, #brand, #competitionId }",
      unless = "#result == null")
  public Optional<PromotionContainerDto<PromotionV2Dto>> findPromotionsByBrandAndCompetitionId(
      String brand, String competitionId) {
    Utils.newRelicLogTransaction("/CMS-findPromotionsByBrandAndCompetitionId");
    return cmsApiClient.findPromotionsByBrandAndCompetitionId(brand, competitionId);
  }

  @Override
  @Cacheable(value = "BybWidget")
  public Optional<BybWidgetDto> getBybWidget(String brand) {
    Utils.newRelicLogTransaction("/CMS-getBybWidget");
    return cmsApiClient.getBybWidget(brand);
  }
}
