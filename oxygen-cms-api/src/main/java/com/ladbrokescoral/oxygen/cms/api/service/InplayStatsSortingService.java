package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsSorting;
import com.ladbrokescoral.oxygen.cms.api.repository.InplayStatsSortingRepository;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class InplayStatsSortingService extends SortableService<InplayStatsSorting> {

  private final InplayStatsSortingRepository inplayStatsSortingRepository;

  public InplayStatsSortingService(InplayStatsSortingRepository inplayStatsSortingRepository) {
    super(inplayStatsSortingRepository);
    this.inplayStatsSortingRepository = inplayStatsSortingRepository;
  }

  public List<InplayStatsSorting> findByBrandAndCategoryId(String brand, Integer categoryId) {
    return Optional.ofNullable(
            this.inplayStatsSortingRepository.findAllByBrandAndCategoryIdOrderBySortOrderAsc(
                brand, categoryId))
        .orElse(new ArrayList<>());
  }
}
