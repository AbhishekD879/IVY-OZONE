package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipV2ConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class LuckyDipV2ConfigPublicService {

  private final LuckyDipV2ConfigService luckyDipV2ConfigService;
  private final SiteServeApiProvider siteServeApiProvider;
  private final ModelMapper modelMapper;

  public LuckyDipV2ConfigPublicService(
      LuckyDipV2ConfigService luckyDipV2ConfigService,
      SiteServeApiProvider siteServeApiProvider,
      ModelMapper modelMapper) {
    this.luckyDipV2ConfigService = luckyDipV2ConfigService;
    this.siteServeApiProvider = siteServeApiProvider;
    this.modelMapper = modelMapper;
  }

  public Optional<LuckyDipV2ConfigurationPublicDto> getAllLuckyDipConfigByBrandAndEvent(
      String brand, String eventId) {

    Optional<LuckyDipV2Config> luckyDipConfiguration =
        luckyDipV2ConfigService.getLDByBrandAndLDConfigLevelId(brand, eventId);
    if (!luckyDipConfiguration.isPresent()) {
      Optional<Event> event = siteServeApiProvider.api(brand).getEvent(eventId, true);
      if (event.isPresent()) {
        luckyDipConfiguration =
            luckyDipV2ConfigService.getLDByBrandAndLDConfigLevelId(brand, event.get().getTypeId());
        if (!luckyDipConfiguration.isPresent()) {
          luckyDipConfiguration =
              luckyDipV2ConfigService.getLDByBrandAndLDConfigLevelId(
                  brand, event.get().getCategoryId());
        }
      } else {
        log.error("Error in fetching event details from siteserver for event id: {}", eventId);
        LuckyDipV2ConfigurationPublicDto dto = new LuckyDipV2ConfigurationPublicDto();
        dto.setStatus(null);
        return Optional.of(dto);
      }
    }
    if (luckyDipConfiguration.isPresent()) {
      log.info("lucky dip configuration present for event/type/category id{}:", eventId);
      return luckyDipConfiguration.map(
          e -> modelMapper.map(e, LuckyDipV2ConfigurationPublicDto.class));
    } else {
      log.error("No Lucky Dip configured for event id (typeId/categoryId): {}", eventId);
      LuckyDipV2ConfigurationPublicDto dto = new LuckyDipV2ConfigurationPublicDto();
      dto.setStatus(null);
      return Optional.of(dto);
    }
  }
}
