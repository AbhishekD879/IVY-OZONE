package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoLeaderboardConfigPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.service.PromoLeaderboardService;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class PromoLeaderboardPublicService {

  private final PromoLeaderboardService promoLeaderboardService;
  private final ModelMapper modelMapper;

  public PromoLeaderboardPublicService(
      PromoLeaderboardService promoLeaderboardService, ModelMapper modelMapper) {
    this.promoLeaderboardService = promoLeaderboardService;
    this.modelMapper = modelMapper;
  }

  public List<PromoLeaderboardConfigPublicDto> findLeaderboardByBrand(String brand) {
    return promoLeaderboardService.findByBrand(brand).stream()
        .filter(PromoLeaderboardConfig::getStatus)
        .map(e -> modelMapper.map(e, PromoLeaderboardConfigPublicDto.class))
        .collect(Collectors.toList());
  }
}
