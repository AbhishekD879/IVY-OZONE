package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.TopGame;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.TopGameService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class TopGames extends AbstractSortableController<TopGame> {

  private final TopGameService service;

  @Autowired
  TopGames(TopGameService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @GetMapping("top-game")
  @Override
  public List<TopGame> readAll() {
    return super.readAll();
  }

  @GetMapping("top-game/{id}")
  @Override
  public TopGame read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("top-game/brand/{brand}")
  @Override
  public List<TopGame> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("top-game")
  @Override
  public ResponseEntity create(@RequestBody TopGame entity) {
    return super.create(entity);
  }

  @PutMapping("top-game/{id}")
  @Override
  public TopGame update(@PathVariable String id, @RequestBody TopGame entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("top-game/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    TopGame topGame = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeImage(topGame);
    service.removeIcon(topGame);

    return delete(Optional.of(topGame));
  }

  @PostMapping("top-game/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("top-game/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<TopGame> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<TopGame> topGame = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      topGame = service.attachImage(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.ICON)) {
      topGame = service.attachIcon(maybeEntity.get(), file);
    }

    return topGame
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("top-game/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<TopGame> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<TopGame> removeResult = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      removeResult = service.removeImage(maybeEntity.get());
    }
    if (fileType.equals(FileType.ICON)) {
      removeResult = service.removeIcon(maybeEntity.get());
    }

    return removeResult
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }
}
