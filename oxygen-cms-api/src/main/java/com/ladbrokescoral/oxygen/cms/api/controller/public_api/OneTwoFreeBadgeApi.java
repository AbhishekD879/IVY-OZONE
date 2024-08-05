package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BadgeDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BadgePublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class OneTwoFreeBadgeApi implements Public {
  private final BadgePublicService badgePublicService;

  @GetMapping("{brand}/one-two-free/badge")
  public List<BadgeDto> findAllByBrand(@PathVariable String brand) {
    return badgePublicService.findAllByBrand(brand);
  }
}
