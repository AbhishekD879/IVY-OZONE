package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.GameDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OtfIosAppToggleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QualificationRuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.StaticTextOtfDto;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.GamePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.GameState;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OtfIosAppTogglePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QualificationRulePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticTextOtfPublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class OneTwoFreeApi implements Public {
  private final GamePublicService gameService;
  private final StaticTextOtfPublicService staticTextService;
  private final QualificationRulePublicService qualificationRuleService;
  private final OtfIosAppTogglePublicService otfIosAppTogglePublicService;

  @GetMapping("{brand}/one-two-free/game")
  public GameDto findGameByBrand(
      @PathVariable String brand,
      @RequestParam(required = false) GameState gameState,
      @RequestParam(required = false) String gameId) {
    return gameService.getSingleByBrand(brand, gameState, gameId);
  }

  @GetMapping("{brand}/one-two-free/previous-current-future-game")
  public List<GameDto> findPreviousCurrentAndFutureGameByBrand(@PathVariable String brand) {
    return gameService.findPreviousCurrentAndFutureGameByBrand(brand);
  }

  @GetMapping("{brand}/one-two-free/current-future-game")
  public List<GameDto> findCurrentAndFutureGameByBrand(@PathVariable String brand) {
    return gameService.findCurrentAndFutureGameByBrand(brand);
  }

  @GetMapping("{brand}/one-two-free/static-texts")
  public List<StaticTextOtfDto> findByBrand(@PathVariable("brand") String brand) {
    return staticTextService.findEnabledByBrand(brand);
  }

  @GetMapping("{brand}/one-two-free/games")
  public List<GameDto> findGameByBrand(@PathVariable("brand") String brand) {
    return gameService.findByBrand(brand);
  }

  @GetMapping("{brand}/one-two-free/qualification-rule")
  public QualificationRuleDto findQualificationRuleByBrand(@PathVariable("brand") String brand) {
    return qualificationRuleService.findByBrand(brand).orElseThrow(NotFoundException::new);
  }

  @GetMapping("{brand}/one-two-free/otf-ios-app-toggle")
  public OtfIosAppToggleDto findOtfIosAppToggleByBrand(@PathVariable("brand") String brand) {
    return otfIosAppTogglePublicService.findByBrand(brand);
  }
}
