package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Homepage;
import com.ladbrokescoral.oxygen.cms.api.repository.HomepagesRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HomepageService extends SortableService<Homepage> {
  private final HomepagesRepository homepagesRepository;

  @Autowired
  public HomepageService(HomepagesRepository repository) {
    super(repository);
    this.homepagesRepository = repository;
  }

  public List<Homepage> readAll() {
    return homepagesRepository.findAllByOrderBySortOrderAsc();
  }
}
