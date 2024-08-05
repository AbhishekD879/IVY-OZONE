package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SignPostingDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.service.SignPostingService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class SignPostingController extends AbstractSortableController<SignPosting> {
  @Autowired
  SignPostingController(SignPostingService crudService) {
    super(crudService);
  }

  @GetMapping("signposting")
  @Override
  public List<SignPosting> readAll() {
    return super.readAll();
  }

  @GetMapping("signposting/{id}")
  @Override
  public SignPosting read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("signposting/brand/{brand}")
  @Override
  public List<SignPosting> readByBrand(@PathVariable String brand) {

    return super.readByBrand(brand);
  }

  @PostMapping("signposting")
  public ResponseEntity<SignPosting> create(@RequestBody @Valid SignPostingDTO signPostingDTO) {
    SignPosting entity = (Util.objectMapper().convertValue(signPostingDTO, SignPosting.class));
    return super.create(entity);
  }

  @PutMapping("signposting/{id}")
  public SignPosting update(
      @PathVariable String id, @RequestBody @Valid SignPostingDTO signPostingDTO) {
    SignPosting entity = (Util.objectMapper().convertValue(signPostingDTO, SignPosting.class));
    return super.update(id, entity);
  }

  @DeleteMapping("signposting/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {

    return super.delete(id);
  }
}
