package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.ExternalLink;
import com.ladbrokescoral.oxygen.cms.api.exception.ElementAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.repository.ExternalLinkRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ExternalLinkService extends AbstractService<ExternalLink> {

  private final ExternalLinkRepository externalLinkRepository;

  @Autowired
  public ExternalLinkService(ExternalLinkRepository externalLinkRepository) {
    super(externalLinkRepository);
    this.externalLinkRepository = externalLinkRepository;
  }

  @Override
  public ExternalLink prepareModelBeforeSave(ExternalLink model) {
    externalLinkRepository.findAllByUrlAndBrand(model.getUrl(), model.getBrand()).stream()
        .filter(entity -> !entity.getId().equals(model.getId()))
        .findAny()
        .ifPresent(
            element -> {
              throw new ElementAlreadyExistException();
            });
    return model;
  }
}
