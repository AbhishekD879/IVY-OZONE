package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SpecialPage;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidPageNameException;
import com.ladbrokescoral.oxygen.cms.api.service.SpecialPagesService;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.specialPages.SpecialPageDTO;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.specialPages.SpecialPagesMaintenance;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class SpecialPages<T extends SpecialPage> extends AbstractCrudController<T> {

  private final SpecialPagesService specialPagesService;
  private final SpecialPagesMaintenance specialPagesMaintenance;

  @Autowired
  public SpecialPages(
      SpecialPagesService specialPagesService, SpecialPagesMaintenance specialPagesMaintenance) {
    super(specialPagesService);
    this.specialPagesService = specialPagesService;
    this.specialPagesMaintenance = specialPagesMaintenance;
  }

  @PostMapping("special-pages/{pageName}")
  public ResponseEntity create(@RequestBody @Valid Object entity, @PathVariable String pageName) {
    ResponseEntity responseEntity = null;
    try {
      Class t = Class.forName("com.ladbrokescoral.oxygen.cms.api.entity." + pageName);
      responseEntity = super.create((T) (objectMapper().convertValue(entity, t)));
    } catch (ClassNotFoundException e) {
      throw new InvalidPageNameException();
    }
    specialPagesMaintenance.saveOrUpdateSpecialPage(
        objectMapper().convertValue(entity, SpecialPageDTO.class));
    return responseEntity;
  }

  @GetMapping("special-pages/{pageName}")
  public SpecialPage findByPageName(@PathVariable String pageName) {
    return specialPagesService.findByPageName(pageName);
  }

  @PutMapping("special-pages/{pageName}")
  public SpecialPage update(@PathVariable String pageName, @RequestBody @Valid Object entity) {
    SpecialPage responseSpecialPage = null;
    try {
      SpecialPage specialPage = specialPagesService.findByPageName(pageName);
      Class t = Class.forName("com.ladbrokescoral.oxygen.cms.api.entity." + pageName);
      responseSpecialPage =
          super.update(specialPage.getId(), (T) (objectMapper().convertValue(entity, t)));
    } catch (ClassNotFoundException e) {
      throw new InvalidPageNameException();
    }
    specialPagesMaintenance.saveOrUpdateSpecialPage(
        objectMapper().convertValue(entity, SpecialPageDTO.class));
    return responseSpecialPage;
  }

  @DeleteMapping("special-pages/{pageName}")
  public void deleteByPageName(@PathVariable String pageName) {
    specialPagesService.delete(pageName);
  }

  private ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new JavaTimeModule())
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }
}
