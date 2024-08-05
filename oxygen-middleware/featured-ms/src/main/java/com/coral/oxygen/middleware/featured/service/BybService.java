package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.pojos.model.cms.CmsYcLeague;
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetLeaguesResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.LeaguesResponse;
import com.newrelic.api.agent.NewRelic;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class BybService {

  private final SystemConfigProvider systemConfigProvider;
  private final CmsService cmsService;
  private final BlockingBanachClient<GetLeaguesResponseDto, LeaguesResponse> leaguesClient;

  private Set<Long> typesAvailability;

  public void reloadData() {
    try {
      if (systemConfigProvider.systemConfig().getYourCallIconsAndTabs() != null
          && Boolean.TRUE.equals(
              systemConfigProvider.systemConfig().getYourCallIconsAndTabs().isEnableIcon())) {
        List<CmsYcLeague> cmsYcLeagues = cmsService.requestYcLeagues();
        Set<Long> cmsEnabledTypeIds =
            cmsYcLeagues.stream()
                .filter(league -> Boolean.TRUE.equals(league.getEnabled()))
                .map(CmsYcLeague::getTypeId)
                .filter(Objects::nonNull)
                .map(Integer::longValue)
                .collect(Collectors.toSet());

        Set<Long> typeIds = new HashSet<>(getBybLeagueTypeIds());
        cmsEnabledTypeIds.retainAll(typeIds);
        typesAvailability = cmsEnabledTypeIds;
      } else {
        typesAvailability = Collections.emptySet();
      }
    } catch (Exception e) {
      log.error("Error calculation BYB types availability", e);
      NewRelic.noticeError(e);
      typesAvailability = new HashSet<>();
    }
  }

  private Set<Long> getBybLeagueTypeIds() {

    LeaguesResponse bybResponse = leaguesClient.execute(UUID.randomUUID().toString());

    return bybResponse.getData().stream()
        .map(GetLeaguesResponseDto::getObTypeId)
        .filter(Objects::nonNull)
        .collect(Collectors.toSet());
  }

  public boolean isBuildYourBetAvailableForType(long typeId) {
    return typesAvailability.contains(typeId);
  }
}
