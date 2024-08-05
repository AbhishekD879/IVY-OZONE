package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BadgeDto;
import com.ladbrokescoral.oxygen.cms.api.service.BadgeService;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class BadgePublicService {
  private final BadgeService badgeService;

  private ModelMapper modelMapper;

  public BadgePublicService(BadgeService badgeService, ModelMapper modelMapper) {
    this.badgeService = badgeService;
    this.modelMapper = modelMapper;
  }

  public List<BadgeDto> findAllByBrand(String brand) {
    return badgeService.findByBrand(brand).stream()
        .map(e -> modelMapper.map(e, BadgeDto.class))
        .collect(Collectors.toList());
  }
}
