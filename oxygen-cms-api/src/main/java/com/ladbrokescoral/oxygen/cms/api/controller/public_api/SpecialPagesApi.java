package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.SpecialPage;
import com.ladbrokescoral.oxygen.cms.api.service.SpecialPagesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class SpecialPagesApi implements Public {

  private SpecialPagesService specialPagesService;

  @Autowired
  public SpecialPagesApi(SpecialPagesService specialPagesService) {
    this.specialPagesService = specialPagesService;
  }

  @GetMapping("special-pages/{pageName}")
  public SpecialPage findByPageName(@PathVariable String pageName) {
    return specialPagesService.findByPageName(pageName);
  }
}
