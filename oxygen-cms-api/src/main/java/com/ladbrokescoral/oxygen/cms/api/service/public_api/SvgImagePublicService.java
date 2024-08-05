package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.repository.SvgImageRepository;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SvgImagePublicService {

  private final SvgImageRepository svgRepository;

  private static final String SPRITE_TMPL = "<svg style=\"display:none;\">%s</svg>";

  public SvgSpriteDto getSvgSprite(String brand, String sprite) {
    List<SvgImage> svgImages = svgRepository.findAllByBrandAndSprite(brand, sprite);
    return toSvgSpriteDto(sprite, svgImages);
  }

  public SvgSpriteDto getSvgSprites(String brand, List<String> sprites) {
    List<SvgImage> svgImages = new ArrayList<>();
    sprites.forEach(
        sprite -> svgImages.addAll(svgRepository.findAllByBrandAndSprite(brand, sprite)));
    return toSvgSpriteDto(String.join("-", sprites), svgImages);
  }

  public List<SvgSpriteDto> getAllSvgSprites(String brand) {
    Map<String, List<SvgImage>> svgBySprite =
        svgRepository.findByBrand(brand).stream()
            .filter(svg -> Objects.nonNull(svg.getSprite()))
            .collect(Collectors.groupingBy(SvgImage::getSprite));
    return svgBySprite.entrySet().stream()
        .map(e -> toSvgSpriteDto(e.getKey(), e.getValue()))
        .collect(Collectors.toList());
  }

  private SvgSpriteDto toSvgSpriteDto(String sprite, List<SvgImage> svgImages) {
    List<String> svgContent =
        svgImages.stream()
            .filter(SvgImage::isActive)
            .map(SvgImage::getSvg)
            .filter(StringUtils::isNotBlank)
            .collect(Collectors.toList());
    return new SvgSpriteDto(sprite, createSvgSpriteByTmpl(svgContent));
  }

  private String createSvgSpriteByTmpl(List<String> svgContents) {
    return String.format(SPRITE_TMPL, String.join("", svgContents));
  }
}
