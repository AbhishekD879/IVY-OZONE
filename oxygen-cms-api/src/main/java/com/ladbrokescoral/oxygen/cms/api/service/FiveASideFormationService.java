package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.FiveASideFormation;
import com.ladbrokescoral.oxygen.cms.api.repository.FiveASideFormationRepository;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class FiveASideFormationService extends SortableService<FiveASideFormation> {
  private final FiveASideFormationRepository repository;

  public FiveASideFormationService(FiveASideFormationRepository repository) {
    super(repository);
    this.repository = repository;
  }

  public List<FiveASideFormation> findAllByBrandSorted(String brand) {
    return repository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
