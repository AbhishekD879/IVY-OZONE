package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SvgImagePublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class SvgImageApi implements Public {

  private final SvgImagePublicService service;

  @Cacheable(value = "svg-sprite", key = "#brand + '-' + #sprite")
  @GetMapping("{brand}/svg-images/sprite/{sprite}")
  public ResponseEntity<SvgSpriteDto> getSvgImageSprite(
      @PathVariable String brand, @PathVariable String sprite) {
    return ResponseEntity.ok(service.getSvgSprite(brand, sprite));
  }

  @Cacheable(value = "svg-sprite", key = "#brand")
  @GetMapping("{brand}/svg-images/sprite")
  public ResponseEntity<List<SvgSpriteDto>> getAllSvgSprites(@PathVariable String brand) {
    return ResponseEntity.ok(service.getAllSvgSprites(brand));
  }
}
