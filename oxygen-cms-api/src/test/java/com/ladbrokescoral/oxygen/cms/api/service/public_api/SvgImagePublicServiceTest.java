package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.ADDITIONAL;
import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.FEATURED;
import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.INITIAL;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.mockito.BDDMockito.given;
import static org.mockito.Matchers.anyString;

import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.repository.SvgImageRepository;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SvgImagePublicServiceTest {

  @Mock private SvgImage svgImage;

  @Mock private SvgImageRepository repository;

  private SvgImagePublicService service;

  @Before
  public void setUp() {
    service = new SvgImagePublicService(repository);
    given(svgImage.getSvg()).willReturn("<SVG-CONTENT>");
    given(svgImage.isActive()).willReturn(true);
  }

  @Test
  public void createEmptySpriteTest() {
    given(repository.findAllByBrandAndSprite(anyString(), anyString()))
        .willReturn(Collections.emptyList());

    SvgSpriteDto sprite = service.getSvgSprite("bma", INITIAL.getSpriteName());
    assertEquals(INITIAL.getSpriteName(), sprite.getName());
    assertEquals("<svg style=\"display:none;\"></svg>", sprite.getContent());
  }

  @Test
  public void createSpriteWithOneSVG() {
    given(repository.findAllByBrandAndSprite(anyString(), anyString()))
        .willReturn(Collections.singletonList(svgImage));

    SvgSpriteDto sprite = service.getSvgSprite("bma", INITIAL.getSpriteName());
    assertEquals(INITIAL.getSpriteName(), sprite.getName());
    assertEquals("<svg style=\"display:none;\"><SVG-CONTENT></svg>", sprite.getContent());
  }

  @Test
  public void createSpriteWithTwoSVGs() {
    given(repository.findAllByBrandAndSprite(anyString(), anyString()))
        .willReturn(Arrays.asList(svgImage, svgImage));

    SvgSpriteDto sprite = service.getSvgSprite("bma", INITIAL.getSpriteName());
    assertEquals(INITIAL.getSpriteName(), sprite.getName());
    assertEquals(
        "<svg style=\"display:none;\"><SVG-CONTENT><SVG-CONTENT></svg>", sprite.getContent());
  }

  @Test
  public void createSpriteFromDiffSprites() {
    given(repository.findAllByBrandAndSprite(anyString(), anyString()))
        .willReturn(Collections.singletonList(svgImage));

    SvgSpriteDto sprite =
        service.getSvgSprites(
            "bma",
            Arrays.asList(
                INITIAL.getSpriteName(), FEATURED.getSpriteName(), ADDITIONAL.getSpriteName()));
    assertEquals("initial-featured-additional", sprite.getName());
    assertEquals(
        "<svg style=\"display:none;\"><SVG-CONTENT><SVG-CONTENT><SVG-CONTENT></svg>",
        sprite.getContent());
  }

  @Test
  public void getAllBrandSvgs() {
    given(repository.findByBrand(anyString())).willReturn(Arrays.asList(svgImage, svgImage));
    given(svgImage.getSprite()).willReturn(FEATURED.getSpriteName());

    List<SvgSpriteDto> sprites = service.getAllSvgSprites("bma");

    assertEquals(1, sprites.size());
    SvgSpriteDto sprite = sprites.get(0);
    assertEquals(FEATURED.getSpriteName(), sprite.getName());
    assertEquals(
        "<svg style=\"display:none;\"><SVG-CONTENT><SVG-CONTENT></svg>", sprite.getContent());
  }

  @Test
  public void getAllBrandSvgsSkipEmptySprite() {
    SvgImage noSpriteImage = new SvgImage();
    noSpriteImage.setSvg("<symbol>no sprite</symbol>");
    given(repository.findByBrand(anyString()))
        .willReturn(Arrays.asList(this.svgImage, this.svgImage, noSpriteImage));
    given(this.svgImage.getSprite()).willReturn(FEATURED.getSpriteName());

    List<SvgSpriteDto> sprites = service.getAllSvgSprites("bma");

    assertEquals(1, sprites.size());
    SvgSpriteDto sprite = sprites.get(0);
    assertEquals(FEATURED.getSpriteName(), sprite.getName());
    assertEquals(
        "<svg style=\"display:none;\"><SVG-CONTENT><SVG-CONTENT></svg>", sprite.getContent());
    assertFalse(sprite.getContent().contains(noSpriteImage.getSvg()));
  }
}
