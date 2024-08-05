package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TimelineGeneralConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.TimelineSplashConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.mapping.TimelineGeneralConfigMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.TimelineSplashConfigMapper;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineCampaignService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineSplashConfigService;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class TimelineConfigPublicService {

  private final TimelineConfigService generalConfigService;
  private final TimelineSplashConfigService splashConfigService;
  private final TimelineCampaignService timelineCampaignService;

  public TimelineConfigPublicService(
      TimelineConfigService generalConfigService,
      TimelineSplashConfigService splashConfigService,
      TimelineCampaignService timelineCampaignService) {
    this.generalConfigService = generalConfigService;
    this.splashConfigService = splashConfigService;
    this.timelineCampaignService = timelineCampaignService;
  }

  public Optional<TimelineSplashConfigDto> findSplashConfigByBrand(String brand) {
    return splashConfigService
        .findOptionalByBrand(brand)
        .map(TimelineSplashConfigMapper.INSTANCE::toDto);
  }

  public Optional<TimelineGeneralConfigDto> findGeneralConfigByBrand(String brand) {
    return generalConfigService
        .findOptionalByBrand(brand)
        .map(TimelineGeneralConfigMapper.INSTANCE::toDto)
        .map(
            (TimelineGeneralConfigDto timelineConfigDto) -> {
              timelineCampaignService
                  .findCurrentLiveCampaignByBrand(brand)
                  .ifPresent(
                      (Campaign campaign) -> {
                        timelineConfigDto.setLiveCampaignDisplayFrom(campaign.getDisplayFrom());
                        timelineConfigDto.setLiveCampaignDisplayTo(campaign.getDisplayTo());
                        timelineConfigDto.setLiveCampaignId(campaign.getId());
                        timelineConfigDto.setLiveCampaignName(campaign.getName());
                      });
              return timelineConfigDto;
            });
  }
}
