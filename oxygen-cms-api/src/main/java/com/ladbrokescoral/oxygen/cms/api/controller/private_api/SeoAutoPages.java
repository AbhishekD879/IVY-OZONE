package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoAutoPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import com.ladbrokescoral.oxygen.cms.api.mapping.SeoAutoPageMapper;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class SeoAutoPages extends AbstractCrudController<SeoAutoPage> {

  protected SeoAutoPages(CrudService<SeoAutoPage> crudService) {
    super(crudService);
  }

  @GetMapping("seo-auto-page/brand/{brand}")
  @Override
  public List<SeoAutoPage> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("seo-auto-page")
  public ResponseEntity<SeoAutoPage> create(@RequestBody @Validated SeoAutoPageDto seoAutoPageDto) {
    SeoAutoPage entity = SeoAutoPageMapper.INSTANCE.toEntity(seoAutoPageDto);
    return super.create(entity);
  }

  @PutMapping("seo-auto-page/{id}")
  public SeoAutoPage update(
      @PathVariable String id, @RequestBody @Validated SeoAutoPageDto seoAutoPageDto) {
    SeoAutoPage entity = SeoAutoPageMapper.INSTANCE.toEntity(seoAutoPageDto);
    return super.update(id, entity);
  }

  @DeleteMapping("seo-auto-page/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
