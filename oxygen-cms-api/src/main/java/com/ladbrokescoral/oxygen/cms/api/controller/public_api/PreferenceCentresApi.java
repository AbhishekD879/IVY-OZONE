package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.PreferenceCentre;
import com.ladbrokescoral.oxygen.cms.api.service.PreferenceCentresService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class PreferenceCentresApi implements Public {

  private PreferenceCentresService preferenceCentresService;

  @Autowired
  public PreferenceCentresApi(PreferenceCentresService preferenceCentresService) {
    this.preferenceCentresService = preferenceCentresService;
  }

  @GetMapping("{brand}/fanzone-preference-center")
  public Optional<PreferenceCentre> findByBrand(@PathVariable String brand) {
    return preferenceCentresService.findAllPreferencesByBrand(brand);
  }
}
