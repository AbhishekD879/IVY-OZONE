package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class BrandService extends SortableService<Brand> {

  private final BrandRepository brandRepository;

  @Autowired
  public BrandService(BrandRepository brandRepository) {
    super(brandRepository);
    this.brandRepository = brandRepository;
  }

  @Override
  public List<Brand> findAll() {
    return brandRepository.findAll(SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  @Override
  public Brand prepareModelBeforeSave(Brand model) {
    model.setKey(generateKey(model));
    return model;
  }

  public Optional<Brand> findByBrandCode(final String brandCode) {
    return brandRepository.findOneByBrandCode(brandCode);
  }

  private String generateKey(Brand model) {
    return model.getTitle().trim().toLowerCase().replace(" ", "-");
  }
}
