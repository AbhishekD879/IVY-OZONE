package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.BetSharingRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class BetSharingService extends AbstractService<BetSharingEntity> {
  private final BetSharingRepository betSharingrepository;

  public BetSharingService(BetSharingRepository betSharingRepository) {
    super(betSharingRepository);
    this.betSharingrepository = betSharingRepository;
  }

  public Optional<BetSharingEntity> getBetSharingByBrand(String brand) {
    List<BetSharingEntity> betSharingEntities = betSharingrepository.findByBrand(brand);
    if (CollectionUtils.isEmpty(betSharingEntities)) return Optional.empty();
    return Optional.ofNullable(betSharingEntities.get(0));
  }
}
