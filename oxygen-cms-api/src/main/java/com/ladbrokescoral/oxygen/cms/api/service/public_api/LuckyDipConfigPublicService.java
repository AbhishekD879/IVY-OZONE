package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipConfigService;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class LuckyDipConfigPublicService {

  private final LuckyDipConfigService luckyDipConfigService;

  private final ModelMapper modelMapper;

  public LuckyDipConfigPublicService(
      LuckyDipConfigService luckyDipConfigService, ModelMapper modelMapper) {
    this.luckyDipConfigService = luckyDipConfigService;
    this.modelMapper = modelMapper;
  }

  public List<LuckyDipConfigurationPublicDto> getAllLuckyDipConfigByBrand(String brand) {
    return luckyDipConfigService.findByBrand(brand).stream()
        .map(e -> modelMapper.map(e, LuckyDipConfigurationPublicDto.class))
        .collect(Collectors.toList());
  }
}
