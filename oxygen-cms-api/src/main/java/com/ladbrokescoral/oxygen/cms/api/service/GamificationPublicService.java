package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDetailsPublicDto;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class GamificationPublicService {
  private final GamificationService gamificationService;
  private ModelMapper modelMapper;

  GamificationPublicService(GamificationService gamificationService, ModelMapper modelMapper) {
    this.gamificationService = gamificationService;
    this.modelMapper = modelMapper;
  }

  public List<GamificationDetailsPublicDto> findGamificationByBrand(String brand) {
    return gamificationService.findGamificationByBrand(brand).stream()
        .map(e -> modelMapper.map(e, GamificationDetailsPublicDto.class))
        .collect(Collectors.toList());
  }
}
