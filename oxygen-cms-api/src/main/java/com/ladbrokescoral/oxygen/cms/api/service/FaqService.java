package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import com.ladbrokescoral.oxygen.cms.api.repository.FaqRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class FaqService extends SortableService<Faq> {
  private final FaqRepository faqRepository;

  @Autowired
  public FaqService(FaqRepository faqRepository) {
    super(faqRepository);
    this.faqRepository = faqRepository;
  }

  public List<Faq> findAllByBrandSorted(String brand) {
    return faqRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }
}
