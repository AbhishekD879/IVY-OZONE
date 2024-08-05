package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.OfferModule;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.IdNamePair;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferModuleExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferModuleRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Component;

@Component
public class OfferModuleService extends SortableService<OfferModule> {

  private final OfferModuleRepository offerModuleRepository;
  private final OfferModuleExtendedRepository extendedRepository;

  @Autowired
  public OfferModuleService(
      OfferModuleRepository offerModuleRepository,
      OfferModuleExtendedRepository extendedRepository) {
    super(offerModuleRepository);
    this.offerModuleRepository = offerModuleRepository;
    this.extendedRepository = extendedRepository;
  }

  @CacheEvict(
      cacheNames = {"offer-modules"},
      key = "#entity.id")
  @Override
  public OfferModule save(OfferModule entity) {
    return offerModuleRepository.save(entity);
  }

  @Cacheable("offer-modules")
  public IdNamePair findIdNamePairById(String id) {
    return offerModuleRepository.findById(id, IdNamePair.class);
  }

  @CacheEvict(
      cacheNames = {"offer-modules"},
      key = "#updateEntity.id")
  @Override
  public OfferModule update(OfferModule existingEntity, OfferModule updateEntity) {
    return super.update(existingEntity, updateEntity);
  }

  @CacheEvict(
      cacheNames = {"offer-modules"},
      key = "#id")
  @Override
  public void delete(String id) {
    offerModuleRepository.deleteById(id);
  }

  public List<OfferModule> findByBrandAndDeviceType(String brand, String deviceType) {
    return extendedRepository.findAllByBrandAndDeviceType(brand, deviceType);
  }
}
