package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.BankingMenuDto;
import com.ladbrokescoral.oxygen.cms.api.controller.mapping.BankingMenuControllerMapper;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.BankingMenuService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
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
public class BankingMenus extends AbstractSortableController<BankingMenu> {

  private final BankingMenuService service;

  @Autowired
  BankingMenus(BankingMenuService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @GetMapping("banking-menu")
  @Override
  public List<BankingMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("banking-menu/{id}")
  @Override
  public BankingMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("banking-menu/brand/{brand}")
  @Override
  public List<BankingMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("banking-menu")
  public ResponseEntity create(@Valid @RequestBody BankingMenuDto dto) {
    return super.create(BankingMenuControllerMapper.INSTANCE.toEntity(dto));
  }

  @PutMapping("banking-menu/{id}")
  public BankingMenu update(@PathVariable String id, @Valid @RequestBody BankingMenuDto dto) {
    return super.update(id, BankingMenuControllerMapper.INSTANCE.toEntity(dto));
  }

  @DeleteMapping("banking-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    BankingMenu menu = service.findOne(id).orElseThrow(NotFoundException::new);

    service.removeImage(menu);
    service.removeSvgImage(menu);

    return delete(Optional.of(menu));
  }

  @PostMapping("banking-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("banking-menu/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<BankingMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<BankingMenu> bankingMenu = Optional.empty();
    if (fileType.equals(FileType.IMAGE)
        && !file.getOriginalFilename().toLowerCase().contains(".svg")) {
      bankingMenu = service.attachImage(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.SVG)
        || file.getOriginalFilename().toLowerCase().contains(".svg")) {
      bankingMenu = service.attachSvgImage(maybeEntity.get(), file);
    }

    return bankingMenu.map(service::save).map(ResponseEntity::ok).orElseGet(failedToUpdateImage());
  }

  @DeleteMapping("banking-menu/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<BankingMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<BankingMenu> removeResult = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      removeResult = service.removeImage(maybeEntity.get());
    }
    if (fileType.equals(FileType.SVG)) {
      removeResult = service.removeSvgImage(maybeEntity.get());
    }

    return removeResult.map(service::save).map(ResponseEntity::ok).orElseGet(failedToRemoveImage());
  }
}
