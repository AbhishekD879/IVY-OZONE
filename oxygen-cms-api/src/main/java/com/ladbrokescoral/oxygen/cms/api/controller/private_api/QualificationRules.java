package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.QualificationRule;
import com.ladbrokescoral.oxygen.cms.api.service.QualificationRuleService;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class QualificationRules extends AbstractCrudController<QualificationRule> {
  private final QualificationRuleService qualificationRuleService;

  QualificationRules(QualificationRuleService qualificationRuleService) {
    super(qualificationRuleService);
    this.qualificationRuleService = qualificationRuleService;
  }

  @Override
  @PostMapping("/qualification-rule")
  public ResponseEntity<QualificationRule> create(@RequestBody @Valid QualificationRule entity) {
    return super.create(entity);
  }

  @Override
  @PutMapping("/qualification-rule/{id}")
  public QualificationRule update(
      @PathVariable String id, @RequestBody @Valid QualificationRule entity) {
    return super.update(id, entity);
  }

  @GetMapping("/qualification-rule/brand/{brand}")
  public QualificationRule readOneByBrand(@PathVariable String brand) {
    return qualificationRuleService.findOneByBrand(brand);
  }

  @PostMapping("/qualification-rule/{brand}/blacklist")
  public QualificationRule blacklistUsers(
      @PathVariable String brand, @RequestParam("file") MultipartFile file) {
    return qualificationRuleService.uploadEncryptedBlacklistedUsers(brand, file);
  }
}
