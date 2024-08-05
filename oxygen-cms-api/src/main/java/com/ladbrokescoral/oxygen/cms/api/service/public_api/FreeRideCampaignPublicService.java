package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideCampaignService;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class FreeRideCampaignPublicService {

  private final FreeRideCampaignService freeRideCampaignService;

  private ModelMapper modelMapper;

  public FreeRideCampaignPublicService(
      FreeRideCampaignService freeRideCampaignService, ModelMapper modelMapper) {
    this.freeRideCampaignService = freeRideCampaignService;
    this.modelMapper = modelMapper;
  }

  public List<FreeRidePublicCampaignDto> getAllCampaignByBrand(String brand) {
    List<FreeRideCampaign> freeRideCampaignList =
        freeRideCampaignService.getAllCampaignByBrand(brand);
    return freeRideCampaignList.stream()
        .map(e -> modelMapper.map(e, FreeRidePublicCampaignDto.class))
        .collect(Collectors.toList());
  }
}
