package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.GameMenuDto;
import com.ladbrokescoral.oxygen.cms.api.controller.mapping.GameMenuControllerMapper;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.GameMenu;
import com.ladbrokescoral.oxygen.cms.api.service.GameMenuService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class GameMenus extends AbstractSortableController<GameMenu> {

  private final GameMenuService gameMenuService;

  GameMenus(GameMenuService gameMenuService) {
    super(gameMenuService);
    this.gameMenuService = gameMenuService;
  }

  @Override
  @GetMapping("/game-menu")
  public List<GameMenu> readAll() {
    return super.readAll();
  }

  @Override
  @GetMapping("game-menu/brand/{brand}")
  public List<GameMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @PostMapping("game-menu/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("/game-menu")
  public ResponseEntity<GameMenu> create(@Valid @RequestBody GameMenuDto entity) {
    return super.create(GameMenuControllerMapper.INSTANCE.toEntity(entity));
  }

  @Override
  @GetMapping("/game-menu/{id}")
  public GameMenu read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @PutMapping("/game-menu/{id}")
  public GameMenu update(
      @PathVariable("id") String id, @Valid @RequestBody GameMenuDto updateEntity) {
    return super.update(id, GameMenuControllerMapper.INSTANCE.toEntity(updateEntity));
  }

  @DeleteMapping("/game-menu/{id}")
  public void deleteWithImage(@PathVariable("id") String id) {
    gameMenuService.delete(id);
  }

  @PostMapping("/game-menu/{id}/image")
  public GameMenu uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile image,
      @RequestParam(value = "fileType", defaultValue = "svg", required = false) FileType fileType) {
    return gameMenuService.attachImage(id, image, fileType);
  }

  @DeleteMapping("/game-menu/{id}/image")
  public GameMenu removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "svg", required = false) FileType fileType) {
    return gameMenuService.removeImage(id, fileType);
  }
}
