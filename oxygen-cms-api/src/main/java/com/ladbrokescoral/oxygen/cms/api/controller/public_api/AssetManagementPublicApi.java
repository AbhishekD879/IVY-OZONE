package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.AssetManagementDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.AssetManagementPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class AssetManagementPublicApi implements Public {

  private final AssetManagementPublicService service;

  @GetMapping("{brand}/asset-management")
  public List<AssetManagementDto> findByBrandAndNamesAndSportId(
      @PathVariable("brand") String brand,
      @RequestParam String teamNames,
      @RequestParam Integer sportId) {
    List<String> names = Arrays.asList(teamNames.split(","));
    return service.findByBrandAndNamesAndSportId(brand, names, sportId);
  }

  @GetMapping("{brand}/asset-management/brand")
  public List<AssetManagementDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand);
  }
}
