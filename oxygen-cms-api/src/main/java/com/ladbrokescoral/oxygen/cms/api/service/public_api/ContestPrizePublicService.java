package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.service.ContestPrizeService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

/** ContestPrizes Service */
@Service
public class ContestPrizePublicService {

  private final ContestPrizeService service;

  public ContestPrizePublicService(ContestPrizeService service) {
    this.service = service;
  }

  /**
   * List All ContestPrizes based on contestId
   *
   * @param contestId - ContestId
   */
  public List<ContestPrize> findByContestId(String contestId) {
    List<ContestPrize> contestPrizes = service.getByContestId(contestId);
    return contestPrizes.stream().collect(Collectors.toList());
  }

  public List<ContestPrize> find(String brand, String contestId) {
    return service.getByContestIdAndBrand(contestId, brand);
  }

  /**
   * List All ContestPrizes based on Brand
   *
   * @param brand - Brand
   */
  public List<ContestPrize> findByBrand(String brand) {
    return service.findAllByBrandSorted(brand);
  }
}
