package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.YourCallStaticBlock;
import com.ladbrokescoral.oxygen.cms.api.repository.YourCallStaticBlockRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class YourCallStaticBlockService extends AbstractService<YourCallStaticBlock> {

  private final YourCallStaticBlockRepository yourCallStaticBlockRepository;

  @Autowired
  public YourCallStaticBlockService(YourCallStaticBlockRepository yourCallStaticBlockRepository) {
    super(yourCallStaticBlockRepository);
    this.yourCallStaticBlockRepository = yourCallStaticBlockRepository;
  }

  @Override
  public List<YourCallStaticBlock> findByBrand(String brand) {
    return yourCallStaticBlockRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public List<YourCallStaticBlock> findByBrandAndEnabled(String brand) {
    return yourCallStaticBlockRepository.findAllByBrandAndEnabled(brand, Boolean.TRUE);
  }

  @Override
  public YourCallStaticBlock prepareModelBeforeSave(YourCallStaticBlock model) {
    model.setTitleBrand(generateTitleBrand(model));
    return model;
  }

  private String generateTitleBrand(YourCallStaticBlock model) {
    return new StringBuilder(model.getTitle())
        .append("-")
        .append(model.getBrand())
        .toString()
        .toLowerCase();
  }

  public List<YourCallStaticBlock> findByBrandAndEnabledAnd5A(String brand) {
    return yourCallStaticBlockRepository.findAllByBrandAndEnabledAndFiveASide(
        brand, Boolean.TRUE, Boolean.TRUE);
  }
}
