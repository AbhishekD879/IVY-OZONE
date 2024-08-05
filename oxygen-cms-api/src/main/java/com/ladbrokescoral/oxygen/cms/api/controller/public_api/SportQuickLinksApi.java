package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportQuickLinkPublicService;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SportQuickLinksApi implements Public {

  private final SportQuickLinkPublicService service;

  private final SportModuleService sportModuleService;

  @Autowired
  public SportQuickLinksApi(
      SportQuickLinkPublicService service, SportModuleService sportModuleService) {
    this.service = service;
    this.sportModuleService = sportModuleService;
  }

  @GetMapping(value = "{brand}/sport-quick-link")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<?> data =
        PageType.stream()
            .map(
                t ->
                    isEnabled(brand, t, AbstractSportEntity.SPORT_HOME_PAGE)
                        ? service.findAll(brand)
                        : Collections.emptyList())
            .flatMap(List::stream)
            .collect(Collectors.toList());
    return new ResponseEntity<>(data, HttpStatus.OK);
  }

  private boolean isEnabled(String brand, PageType pageType, String sportId) {
    Optional<SportModule> optional =
        sportModuleService.findOne(brand, pageType, sportId, SportModuleType.QUICK_LINK);
    return optional.map(val -> !val.isDisabled()).orElse(true);
  }

  @GetMapping(value = "{brand}/sport-quick-link/{sportId}")
  public ResponseEntity findByBrandAndSportId(
      @PathVariable("brand") String brand, @PathVariable("sportId") String sportId) {
    List<?> data =
        PageType.stream()
            .map(
                t ->
                    isEnabled(brand, t, sportId) ? service.findAll(brand) : Collections.emptyList())
            .flatMap(List::stream)
            .collect(Collectors.toList());
    return new ResponseEntity<>(data, HttpStatus.OK);
  }
}
