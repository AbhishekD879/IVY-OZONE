package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidget;
import com.ladbrokescoral.oxygen.cms.api.exception.PopularAccaWidgetCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularAccaWidgetRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class PopularAccaWidgetService extends AbstractService<PopularAccaWidget> {

  private final PopularAccaWidgetRepository popularAccaWidgetRepository;

  public PopularAccaWidgetService(PopularAccaWidgetRepository popularAccaWidgetRepository) {
    super(popularAccaWidgetRepository);
    this.popularAccaWidgetRepository = popularAccaWidgetRepository;
  }

  @Override
  public PopularAccaWidget save(PopularAccaWidget popularAccaWidget) {
    if (!isExistByBrand(popularAccaWidget)) return super.save(popularAccaWidget);
    throw new PopularAccaWidgetCreateException();
  }

  public Optional<PopularAccaWidget> readByBrand(String brand) {
    List<PopularAccaWidget> popularAccaWidgets = super.findByBrand(brand);
    if (CollectionUtils.isEmpty(popularAccaWidgets)) return Optional.empty();
    return Optional.ofNullable(popularAccaWidgets.get(0));
  }

  public boolean isExistByBrand(PopularAccaWidget entity) {

    return popularAccaWidgetRepository.existsByBrand(entity.getBrand()) && entity.getId() == null;
  }
}
