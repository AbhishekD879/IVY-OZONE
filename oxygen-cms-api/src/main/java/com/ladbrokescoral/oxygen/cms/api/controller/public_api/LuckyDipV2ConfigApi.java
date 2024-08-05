package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipV2ConfigPublicProcessor;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipV2ConfigPublicService;
import java.util.List;
import java.util.Optional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LuckyDipV2ConfigApi implements Public {

  private final LuckyDipV2ConfigPublicService service;

  private final LuckyDipV2ConfigPublicProcessor luckyDipV2ConfigPublicProcessor;

  public LuckyDipV2ConfigApi(
      LuckyDipV2ConfigPublicService service,
      LuckyDipV2ConfigPublicProcessor luckyDipV2ConfigPublicProcessor) {
    this.service = service;
    this.luckyDipV2ConfigPublicProcessor = luckyDipV2ConfigPublicProcessor;
  }

  @GetMapping("{brand}/lucky-dip/{eventId}")
  public Optional<LuckyDipV2ConfigurationPublicDto> getAllLuckyDipConfigByBrandAndEvent(
      @PathVariable("brand") String brand, @PathVariable("eventId") String eventId) {
    return service.getAllLuckyDipConfigByBrandAndEvent(brand, eventId);
  }

  @GetMapping("{brand}/lucky-dip")
  public List<LuckyDipV2ConfigurationPublicDto> getAllLuckyDipConfigByBrand(
      @PathVariable("brand") String brand) {
    return luckyDipV2ConfigPublicProcessor.getAllActiveLDByBrand(brand);
  }
}
