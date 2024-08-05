package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.abstractions.WysiwygControllerTraits;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallStaticBlock;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import com.ladbrokescoral.oxygen.cms.api.service.YourCallStaticBlockService;
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
public class YourCallStaticBlocks extends AbstractCrudController<YourCallStaticBlock>
    implements WysiwygControllerTraits<YourCallStaticBlock> {

  private final YourCallStaticBlockService yourCallStaticBlockService;
  private final WysiwygService wysiwygService;

  @Autowired
  YourCallStaticBlocks(YourCallStaticBlockService crudService, WysiwygService wysiwygService) {
    super(crudService);
    this.yourCallStaticBlockService = crudService;
    this.wysiwygService = wysiwygService;
  }

  @GetMapping("your-call-static-block")
  @Override
  public List<YourCallStaticBlock> readAll() {
    return super.readAll();
  }

  @GetMapping("your-call-static-block/{id}")
  @Override
  public YourCallStaticBlock read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("your-call-static-block/brand/{brand}")
  @Override
  public List<YourCallStaticBlock> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("your-call-static-block")
  @Override
  public ResponseEntity create(@RequestBody @Validated YourCallStaticBlock entity) {
    return super.create(entity);
  }

  @PutMapping("your-call-static-block/{id}")
  @Override
  public YourCallStaticBlock update(
      @PathVariable String id, @Validated @RequestBody YourCallStaticBlock entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("your-call-static-block/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("your-call-static-block/{id}/wysiwyg-image")
  public ResponseEntity uploadWysiwygImage(
      @RequestParam("file") MultipartFile file, @PathVariable("id") @NotBlank String id) {
    YourCallStaticBlock yourCallStaticBlock =
        yourCallStaticBlockService.findOne(id).orElseThrow(NotFoundException::new);
    return uploadWysiwygImage(
        yourCallStaticBlock.getBrand(), file, YourCallStaticBlock.COLLECTION_NAME, id);
  }

  @DeleteMapping("your-call-static-block/{id}/wysiwyg-image/{imageName}")
  public ResponseEntity removeWysiwygImage(
      @PathVariable("id") @NotBlank String id, @PathVariable("imageName") String imageName) {
    YourCallStaticBlock yourCallStaticBlock =
        yourCallStaticBlockService.findOne(id).orElseThrow(NotFoundException::new);
    return removeWysiwygImage(
        yourCallStaticBlock.getBrand(), id, YourCallStaticBlock.COLLECTION_NAME, imageName);
  }

  @Override
  public CrudService<YourCallStaticBlock> getCRUDService() {
    return this.yourCallStaticBlockService;
  }

  @Override
  public WysiwygService getWysiwygService() {
    return this.wysiwygService;
  }
}
