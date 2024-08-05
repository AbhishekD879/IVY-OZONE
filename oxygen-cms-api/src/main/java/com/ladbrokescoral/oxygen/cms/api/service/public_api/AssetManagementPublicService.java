package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.AssetManagementDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.AssetManagementMapper;
import com.ladbrokescoral.oxygen.cms.api.service.AssetManagementService;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AssetManagementPublicService {

  private final AssetManagementService service;

  public List<AssetManagementDto> findAll(String brand) {
    return service.findByBrand(brand).stream()
        .map(AssetManagementMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  public List<AssetManagementDto> findByBrandAndNamesAndSportId(
      String brand, List<String> teamNames, Integer sportId) {
    return service.findByBrandAndNamesAndSportId(brand, teamNames, sportId).stream()
        .map(AssetManagementMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  public List<AssetManagementDto> findByBrand(String brand) {
    return service.findAllByBrand(brand).stream()
        .map(AssetManagementMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
