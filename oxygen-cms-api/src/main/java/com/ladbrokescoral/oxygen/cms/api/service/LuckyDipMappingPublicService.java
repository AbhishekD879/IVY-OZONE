package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class LuckyDipMappingPublicService {

  private final LuckyDipMappingService luckyDipMappingService;
  private final ModelMapper modelMapper;

  public LuckyDipMappingPublicService(
      LuckyDipMappingService luckyDipMappingService, ModelMapper modelMapper) {
    this.luckyDipMappingService = luckyDipMappingService;
    this.modelMapper = modelMapper;
  }

  public List<LuckyDipMappingPublicDto> findAllActiveLuckyDipMappingsByBrand(String brand) {
    return luckyDipMappingService.getAllLuckyDipMappingsByBrand(brand).stream()
        .filter(LuckyDipMapping::getActive)
        .map(e -> modelMapper.map(e, LuckyDipMappingPublicDto.class))
        .collect(Collectors.toList());
  }
}
