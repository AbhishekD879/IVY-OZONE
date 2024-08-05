package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OnBoardPublicService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OnBoardPublicApi implements Public {

  private final OnBoardPublicService onboardPublicService;

  public OnBoardPublicApi(OnBoardPublicService onboardPublicService) {
    this.onboardPublicService = onboardPublicService;
  }

  @GetMapping("/{brand}/my-stable/onboardings")
  public OnBoardDto getOnBoardDto(@PathVariable String brand) {

    return onboardPublicService.getOnBoard(brand);
  }
}
