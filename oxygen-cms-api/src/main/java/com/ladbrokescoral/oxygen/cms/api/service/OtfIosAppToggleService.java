package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.OtfIosAppToggle;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.OtfIosAppToggleRepository;
import org.springframework.stereotype.Service;

@Service
public class OtfIosAppToggleService extends AbstractService<OtfIosAppToggle> {
  private final OtfIosAppToggleRepository otfIosAppToggleRepository;

  public OtfIosAppToggleService(OtfIosAppToggleRepository otfIosAppToggleRepository) {
    super(otfIosAppToggleRepository);
    this.otfIosAppToggleRepository = otfIosAppToggleRepository;
  }

  @Override
  public OtfIosAppToggle save(OtfIosAppToggle entity) {
    if (otfIosAppToggleRepository.existsByBrand(entity.getBrand())) {
      throw new IllegalArgumentException(
          String.format(
              "Only one OtfIosAppToggle config could exist per brand: '%s'", entity.getBrand()));
    }
    return super.save(entity);
  }

  @Override
  public OtfIosAppToggle update(OtfIosAppToggle existingEntity, OtfIosAppToggle updateEntity) {
    if (!existingEntity.getBrand().equals(updateEntity.getBrand())) {
      throw new IllegalArgumentException(
          "Brand cannot be cannot be changed once OtfIosAppToggle config is created");
    }
    return otfIosAppToggleRepository.save(updateEntity);
  }

  public OtfIosAppToggle findOneByBrand(String brand) {
    return otfIosAppToggleRepository.findOneByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
