package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FeatureContainerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FeatureDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import com.ladbrokescoral.oxygen.cms.api.mapping.FeatureMapper;
import com.ladbrokescoral.oxygen.cms.api.service.FeatureService;
import com.ladbrokescoral.oxygen.cms.api.service.StructureService;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class FeaturePublicService {

  public static final int EXPANDED_AMOUNT_DEFAULT_VALUE = 2;
  private final FeatureService featureService;
  private final StructureService structureService;

  public FeaturePublicService(FeatureService featureService, StructureService structureService) {
    this.featureService = featureService;
    this.structureService = structureService;
  }

  public FeatureContainerDto findContainerByBrand(String brand) {
    List<Feature> features = featureService.findAllByBrand(brand);
    List<FeatureDto> list =
        features.stream().map(FeatureMapper.INSTANCE::toDto).collect(Collectors.toList());

    FeatureContainerDto container = new FeatureContainerDto();
    container.setFeatures(list);
    container.setExpandedAmount(getExpandedAmount(brand));

    return container;
  }

  private Integer getExpandedAmount(String brand) {
    return structureService
        .findByBrandAndConfigName(brand, "Features")
        .flatMap(featureValues -> Optional.ofNullable(featureValues.get("expandedAmount")))
        .map(amount -> Integer.valueOf(amount.toString()))
        .orElse(EXPANDED_AMOUNT_DEFAULT_VALUE);
  }
}
