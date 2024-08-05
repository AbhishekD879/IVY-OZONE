package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.EdpMarket;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.EdpMarketRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class EdpMarketService extends SortableService<EdpMarket> {

  private final EdpMarketRepository edpMarketRepository;

  @Autowired
  public EdpMarketService(EdpMarketRepository edpMarketRepository) {
    super(edpMarketRepository);
    this.edpMarketRepository = edpMarketRepository;
  }

  @Override
  public EdpMarket save(EdpMarket entity) {
    verifyOnlyOneLastItem(entity);
    return super.save(entity);
  }

  private void verifyOnlyOneLastItem(EdpMarket entity) {
    if (entity.isLastItem() && isThereAlreadySelectedLastItem(entity)) {
      throw new ValidationException("Last Item is already selected");
    }
  }

  private boolean isThereAlreadySelectedLastItem(EdpMarket entity) {
    return edpMarketRepository.findByLastItemIsTrueAndIdNot(entity.getId()).stream()
            .filter(s -> s.getBrand().equalsIgnoreCase(entity.getBrand()))
            .count()
        >= 1;
  }

  public List<EdpMarket> findAllByBrandSorted(String brand) {
    return edpMarketRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
