package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.StaticBlock;
import com.ladbrokescoral.oxygen.cms.api.repository.StaticBlockRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class StaticBlockService extends AbstractService<StaticBlock> {

  private final StaticBlockRepository staticBlockRepository;

  @Autowired
  public StaticBlockService(StaticBlockRepository staticBlockRepository) {
    super(staticBlockRepository);
    this.staticBlockRepository = staticBlockRepository;
  }

  @Override
  public List<StaticBlock> findByBrand(String brand) {
    return staticBlockRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public Optional<StaticBlock> findByBrandAndUri(String brand, String uri) {
    return staticBlockRepository.findFirstByBrandAndUriAndEnabled(brand, uri, true);
  }

  @Override
  public StaticBlock prepareModelBeforeSave(StaticBlock model) {
    model.setTitleBrand(generateTitleBrand(model));
    return model;
  }

  private String generateTitleBrand(StaticBlock model) {
    return new StringBuilder(model.getTitle())
        .append("-")
        .append(model.getBrand())
        .toString()
        .toLowerCase();
  }
}
