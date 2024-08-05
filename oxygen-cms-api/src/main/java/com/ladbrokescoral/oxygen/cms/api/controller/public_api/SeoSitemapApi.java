package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoSitemapDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeoPagePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SeoSitemapApi implements Public {

  private final SeoPagePublicService service;

  @Autowired
  public SeoSitemapApi(SeoPagePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/seo-sitemap")
  public ResponseEntity<Map<String, SeoSitemapDto>> findByBrand(
      @Brand @PathVariable("brand") String brand) {
    Map<String, SeoSitemapDto> seoPagesMap = service.findSeoSitemap(brand);

    return CollectionUtils.isEmpty(seoPagesMap)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(seoPagesMap, HttpStatus.OK);
  }
}
