package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipV2ConfigService;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class LuckyDipV2ConfigPublicProcessor {

  private final LuckyDipV2ConfigService luckyDipV2ConfigService;
  private final ModelMapper modelMapper;

  public LuckyDipV2ConfigPublicProcessor(
      LuckyDipV2ConfigService luckyDipV2ConfigService, ModelMapper modelMapper) {
    this.luckyDipV2ConfigService = luckyDipV2ConfigService;
    this.modelMapper = modelMapper;
  }

  public List<LuckyDipV2ConfigurationPublicDto> getAllActiveLDByBrand(String brand) {
    return luckyDipV2ConfigService.getAllActiveLDByBrand(brand).stream()
        .filter(Objects::nonNull)
        .map(e -> modelMapper.map(e, LuckyDipV2ConfigurationPublicDto.class))
        .collect(Collectors.toList());
  }
}
