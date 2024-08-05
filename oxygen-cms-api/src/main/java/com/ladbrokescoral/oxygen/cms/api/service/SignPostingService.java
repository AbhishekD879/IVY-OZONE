package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.repository.SignPostingRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class SignPostingService extends SortableService<SignPosting> {
  private final SignPostingRepository signPostingRepository;

  @Autowired
  public SignPostingService(SignPostingRepository signPostingRepository) {
    super(signPostingRepository);
    this.signPostingRepository = signPostingRepository;
  }

  @Override
  public List<SignPosting> findAll() {
    return signPostingRepository.findAll(SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public List<SignPosting> findAllByBrand(String brand) {
    return signPostingRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
