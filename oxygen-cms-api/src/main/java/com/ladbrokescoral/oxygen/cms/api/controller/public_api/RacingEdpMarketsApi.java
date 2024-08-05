package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.RacingEdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RacingEdpMarketPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RacingEdpMarketsApi implements Public {

  private final RacingEdpMarketPublicService service;

  @Autowired
  public RacingEdpMarketsApi(RacingEdpMarketPublicService service) {
    this.service = service;
  }

  @JsonView(Views.Public.class)
  @GetMapping(value = "{brand}/racing-edp-markets")
  public ResponseEntity<List<RacingEdpMarketDto>> findByBrand(@PathVariable("brand") String brand) {
    List<RacingEdpMarketDto> list = service.findByBrand(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
