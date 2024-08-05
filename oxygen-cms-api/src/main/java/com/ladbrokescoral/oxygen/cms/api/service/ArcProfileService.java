package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.repository.ArcProfileRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ArcProfileService extends SortableService<ArcProfile> {
  private ArcProfileRepository arcProfileRepository;

  @Autowired
  public ArcProfileService(ArcProfileRepository faqRepository) {
    super(faqRepository);
    this.arcProfileRepository = faqRepository;
  }

  public ArcProfile findArcProfileByBrandAndModelRiskLevelAndReasonCode(
      String brand, Integer modelAndRiskLevel, Integer reasonCode) {
    return arcProfileRepository
        .findByBrandAndModelRiskLevelAndReasonCode(brand, modelAndRiskLevel, reasonCode)
        .orElse(null);
  }

  public Optional<List<ArcProfile>> findAllByBrand(String brand) {
    return arcProfileRepository.findAllByBrand(brand);
  }

  public Long deleteArcProfileByBrandAndModelRiskLevelAndReasonCode(
      String brand, Integer modelRiskLevel, Integer reasonCode) {
    return arcProfileRepository.deleteArcProfileByBrandAndModelRiskLevelAndReasonCode(
        brand, modelRiskLevel, reasonCode);
  }
}
