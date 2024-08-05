package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.abstractions.WysiwygControllerTraits;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticBlock;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.StaticBlockService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import java.util.List;
import javax.validation.constraints.NotBlank;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
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
public class StaticBlocks extends AbstractCrudController<StaticBlock>
    implements WysiwygControllerTraits<StaticBlock> {

  private final StaticBlockService staticBlockService;
  private final WysiwygService wysiwygService;

  @Autowired
  StaticBlocks(StaticBlockService crudService, WysiwygService wysiwygService) {
    super(crudService);
    this.staticBlockService = crudService;
    this.wysiwygService = wysiwygService;
  }

  @GetMapping("static-block")
  @Override
  public List<StaticBlock> readAll() {
    return super.readAll();
  }

  @GetMapping("static-block/{id}")
  @Override
  public StaticBlock read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("static-block/brand/{brand}")
  @Override
  public List<StaticBlock> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("static-block")
  @Override
  public ResponseEntity create(@RequestBody @Validated StaticBlock entity) {
    return super.create(entity);
  }

  @PutMapping("static-block/{id}")
  @Override
  public StaticBlock update(@PathVariable String id, @RequestBody @Validated StaticBlock entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("static-block/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("static-block/{id}/wysiwyg-image")
  public ResponseEntity uploadWysiwygImage(
      @RequestParam("file") MultipartFile file, @PathVariable("id") @NotBlank String id) {
    StaticBlock staticBlock = staticBlockService.findOne(id).orElseThrow(NotFoundException::new);
    return uploadWysiwygImage(staticBlock.getBrand(), file, StaticBlock.COLLECTION_NAME, id);
  }

  @DeleteMapping("static-block/{id}/wysiwyg-image/{imageName}")
  public ResponseEntity removeWysiwygImage(
      @PathVariable("id") @NotBlank String id, @PathVariable("imageName") String imageName) {
    StaticBlock staticBlock = staticBlockService.findOne(id).orElseThrow(NotFoundException::new);
    return removeWysiwygImage(staticBlock.getBrand(), id, StaticBlock.COLLECTION_NAME, imageName);
  }

  @Override
  public CrudService<StaticBlock> getCRUDService() {
    return this.staticBlockService;
  }

  @Override
  public WysiwygService getWysiwygService() {
    return this.wysiwygService;
  }
}
