package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.AliasModuleTypes;
import com.ladbrokescoral.oxygen.cms.api.service.AliasModuleNamesService;
import java.util.List;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * this controller responsible for providing the titles of all active QuickLinks, SuperButtons and
 * SpecialSuperButtons to the client (CMS-UI) so that they can view them in the Dropdown at alias
 * modules names section of RGY Modules under BonusSupression tab ....the Linked JIRA is OZONE-10188
 */
@RestController
@RequiredArgsConstructor
public class AliasModuleNames implements Abstract {

  private final AliasModuleNamesService aliasModuleNamesService;

  @GetMapping(value = "/alias-module-names/brand/{brand}")
  public ResponseEntity<Map<AliasModuleTypes, List<AliasModuleNamesDto>>>
      readQuickLinksAndSuperButtons(@PathVariable String brand) {
    return new ResponseEntity<>(this.aliasModuleNamesService.readQLAndSB(brand), HttpStatus.OK);
  }
}
