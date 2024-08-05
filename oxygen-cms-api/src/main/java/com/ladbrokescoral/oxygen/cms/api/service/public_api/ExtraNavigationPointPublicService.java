package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ExtraNavigationPointPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.ExtraNavigationPointService;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class ExtraNavigationPointPublicService {
  private final ExtraNavigationPointService extraNavigationPointService;
  private final ModelMapper modelMapper;

  public ExtraNavigationPointPublicService(
      ExtraNavigationPointService extraNavigationPointService, ModelMapper modelMapper) {
    this.extraNavigationPointService = extraNavigationPointService;
    this.modelMapper = modelMapper;
  }

  public List<ExtraNavigationPointPublicDto> findAllActiveExtraNavPointsByBrand(String brand) {
    return extraNavigationPointService.getAllExtraNavPtsByBrandSorted(brand).stream()
        .filter(ExtraNavigationPoint::isEnabled)
        .map(e -> modelMapper.map(e, ExtraNavigationPointPublicDto.class))
        .collect(Collectors.toList());
  }
}
