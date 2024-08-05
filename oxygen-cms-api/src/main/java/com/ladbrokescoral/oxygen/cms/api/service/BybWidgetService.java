package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BybWidget;
import com.ladbrokescoral.oxygen.cms.api.exception.BybWidgetCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.BybWidgetRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class BybWidgetService extends AbstractService<BybWidget> {

  private final BybWidgetRepository bybWidgetRepository;

  public BybWidgetService(BybWidgetRepository bybWidgetRepository) {
    super(bybWidgetRepository);
    this.bybWidgetRepository = bybWidgetRepository;
  }

  @Override
  public BybWidget save(BybWidget bybWidget) {
    if (!isExistByBrand(bybWidget)) return super.save(bybWidget);
    throw new BybWidgetCreateException();
  }

  public Optional<BybWidget> readByBrand(String brand) {
    List<BybWidget> bybWidgets = super.findByBrand(brand);
    if (CollectionUtils.isEmpty(bybWidgets)) return Optional.empty();
    return Optional.ofNullable(bybWidgets.get(0));
  }

  public boolean isExistByBrand(BybWidget entity) {

    return bybWidgetRepository.existsByBrand(entity.getBrand()) && entity.getId() == null;
  }
}
