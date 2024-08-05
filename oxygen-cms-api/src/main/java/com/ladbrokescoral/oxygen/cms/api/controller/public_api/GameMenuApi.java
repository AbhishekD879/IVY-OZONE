package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.GameMenuDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.GameMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.GameMenuService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GameMenuApi implements Public {

  private final GameMenuService service;

  public GameMenuApi(GameMenuService service) {
    this.service = service;
  }

  @GetMapping("{brand}/game-menu")
  public List<GameMenuDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand).stream()
        .map(GameMenuMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
