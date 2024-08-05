package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsDisplay;
import com.ladbrokescoral.oxygen.cms.api.repository.InplayStatsDisplayRepository;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class InplayStatsDisplayService extends SortableService<InplayStatsDisplay> {

  private final InplayStatsDisplayRepository inplayStatsDisplayRepository;

  public InplayStatsDisplayService(InplayStatsDisplayRepository inplayStatsDisplayRepository) {
    super(inplayStatsDisplayRepository);
    this.inplayStatsDisplayRepository = inplayStatsDisplayRepository;
  }

  public List<InplayStatsDisplay> findByBrandAndCategoryId(String brand, Integer categoryId) {
    return Optional.ofNullable(
            this.inplayStatsDisplayRepository.findAllByBrandAndCategoryIdOrderBySortOrderAsc(
                brand, categoryId))
        .orElse(new ArrayList<>());
  }
}
