package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OtfGameTabsDto;
import com.ladbrokescoral.oxygen.cms.api.service.OtfGameTabsService;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class OtfGameTabPublicService {
  private final OtfGameTabsService otfGameTabsService;
  private final ModelMapper modelMapper;

  public OtfGameTabPublicService(OtfGameTabsService otfGameTabsService, ModelMapper modelMapper) {
    this.otfGameTabsService = otfGameTabsService;
    this.modelMapper = modelMapper;
  }

  public List<OtfGameTabsDto> findByBrand(String brand) {
    return otfGameTabsService.findByBrand(brand).stream()
        .map(e -> modelMapper.map(e, OtfGameTabsDto.class))
        .collect(Collectors.toList());
  }
}
