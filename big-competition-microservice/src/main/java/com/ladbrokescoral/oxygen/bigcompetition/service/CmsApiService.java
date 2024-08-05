package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.cms.client.model.*;
import java.util.Optional;

public interface CmsApiService {
  Optional<Competition> findCompetitionByBrandAndUri(String brand, String uri);

  Optional<CompetitionTab> findCompetitionTabById(String id);

  Optional<CompetitionSubTab> findCompetitionSubTabById(String id);

  Optional<CompetitionModule> findCompetitionModuleById(String id);

  Optional<PromotionContainerDto<PromotionV2Dto>> findPromotionsByBrandAndCompetitionId(
      String brand, String competitionId);

  Optional<BybWidgetDto> getBybWidget(String brand);
}
