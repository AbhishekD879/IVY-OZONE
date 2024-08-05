package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Gallery;
import com.ladbrokescoral.oxygen.cms.api.repository.GalleryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class GalleryService extends AbstractService<Gallery> {

  @Autowired
  public GalleryService(GalleryRepository repository) {
    super(repository);
  }
}
