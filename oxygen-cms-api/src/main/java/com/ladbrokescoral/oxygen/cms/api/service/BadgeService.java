package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Badge;
import com.ladbrokescoral.oxygen.cms.api.repository.BadgeRepository;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class BadgeService extends AbstractService<Badge> {

  private final BadgeRepository badgeRepository;

  public BadgeService(BadgeRepository badgeRepository) {
    super(badgeRepository);
    this.badgeRepository = badgeRepository;
  }

  @Override
  public List<Badge> findByBrand(String brand) {
    return badgeRepository.findByBrand(brand);
  }
}
