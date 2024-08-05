package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FaqDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FaqPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FaqApi implements Public {
  private final FaqPublicService service;

  @Autowired
  public FaqApi(FaqPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/faq")
  public ResponseEntity<List<Faq>> findByBrand(@PathVariable("brand") String brand) {
    List<Faq> list = service.findByBrand(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }

  @GetMapping("faq/{id}")
  public FaqDto findById(@PathVariable("id") String id) {
    return service.findById(id);
  }
}
