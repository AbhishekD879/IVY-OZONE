package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneClub;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesClubService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class FanzonesClubApi implements Public {

  private FanzonesClubService fanzonesClubService;

  @Autowired
  public FanzonesClubApi(FanzonesClubService fanzonesClubService) {
    this.fanzonesClubService = fanzonesClubService;
  }

  /**
   * This API call is used to get all the FanzoneClubs
   *
   * @param brand
   * @return it will return all the requested FanzoneClubs.
   */
  @GetMapping("{brand}/fanzone-club")
  public Optional<List<FanzoneClub>> findAllByPageName(@PathVariable String brand) {
    return fanzonesClubService.findAllFanzonesByBrand(brand);
  }
}
