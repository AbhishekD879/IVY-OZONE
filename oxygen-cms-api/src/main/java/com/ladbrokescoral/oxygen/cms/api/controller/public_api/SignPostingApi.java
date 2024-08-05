package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.service.SignPostingService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SignPostingApi implements Public {

  private final SignPostingService service;

  @Autowired
  public SignPostingApi(SignPostingService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/signposting")
  public List<SignPosting> findByBrand(@PathVariable("brand") String brand) {
    return service.findAllByBrand(brand);
  }
}
