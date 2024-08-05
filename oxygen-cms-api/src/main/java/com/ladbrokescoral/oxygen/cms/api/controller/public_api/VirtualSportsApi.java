package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.VirtualSportPublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class VirtualSportsApi implements Public {
  private final VirtualSportPublicService virtualSportPublicService;

  @GetMapping("/{brand}/virtual-sports")
  public List<VirtualSportDto> findVirtualSportsConfigs(@PathVariable("brand") String brand) {
    return virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand);
  }
}
