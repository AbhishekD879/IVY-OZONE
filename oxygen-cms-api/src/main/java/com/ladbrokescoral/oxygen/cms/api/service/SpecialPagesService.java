package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.SpecialPagesRepository;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Slf4j
@Component
@Validated
public class SpecialPagesService<T extends SpecialPage> extends AbstractService<T> {

  private SpecialPagesRepository<T> specialPagesRepository;

  @Autowired
  public SpecialPagesService(SpecialPagesRepository specialPagesRepository) {
    super(specialPagesRepository);
    this.specialPagesRepository = specialPagesRepository;
  }

  public SpecialPage findByPageName(String pageName) {
    Optional<SpecialPage> specialPage = specialPagesRepository.findByPageName(pageName);
    return specialPage.isPresent() ? specialPage.get() : new SpecialPage();
  }

  @Override
  public void delete(String pageName) {
    SpecialPage specialPage =
        specialPagesRepository.findByPageName(pageName).orElseThrow(NotFoundException::new);
    specialPagesRepository.delete(specialPage);
  }
}
