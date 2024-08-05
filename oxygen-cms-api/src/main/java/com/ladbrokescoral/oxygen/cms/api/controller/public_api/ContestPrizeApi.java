package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ContestPrizePublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/** Contest Prizes Controller */
@RestController
public class ContestPrizeApi implements Public {

  private final ContestPrizePublicService contestPrizesPublicService;

  @Autowired
  ContestPrizeApi(ContestPrizePublicService contestPrizesPublicService) {
    this.contestPrizesPublicService = contestPrizesPublicService;
  }

  /**
   * List All Contest Prizes based on Contest Id
   *
   * @param contestId - Contest Id
   */
  @GetMapping("contestprize/{contestId}")
  public List<ContestPrize> getByContestId(@PathVariable String contestId) {
    return contestPrizesPublicService.findByContestId(contestId);
  }

  @GetMapping(value = "contestprize/{brand}/{contestId}")
  public List<ContestPrize> findByBrand(
      @PathVariable("brand") String brand, @PathVariable("contestId") String contestId) {
    return contestPrizesPublicService.find(brand, contestId);
  }
}
