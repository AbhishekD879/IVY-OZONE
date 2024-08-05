package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideCampaignPublicService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FreeRideCampaignApi implements Public {

  private final FreeRideCampaignPublicService service;

  public FreeRideCampaignApi(FreeRideCampaignPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/freeride-campaign")
  public List<FreeRidePublicCampaignDto> getAllCampaignByBrand(
      @PathVariable("brand") String brand) {
    return service.getAllCampaignByBrand(brand);
  }
}
