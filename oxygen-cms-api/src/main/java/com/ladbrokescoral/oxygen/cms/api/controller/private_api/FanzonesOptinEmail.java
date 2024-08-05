package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneOptinEmailDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import com.ladbrokescoral.oxygen.cms.api.mapping.FanzoneOptinEmailMapper;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class FanzonesOptinEmail extends AbstractCrudController<FanzoneOptinEmail> {
  private final FanzonesOptinEmailService fanzonesOptinEmailService;
  private final FanzoneOptinEmailMapper fanzoneOptinEmailMapper;

  @Autowired
  FanzonesOptinEmail(
      FanzonesOptinEmailService fanzonesOptinEmailService,
      FanzoneOptinEmailMapper fanzoneOptinEmailMapper) {
    super(fanzonesOptinEmailService);
    this.fanzonesOptinEmailService = fanzonesOptinEmailService;
    this.fanzoneOptinEmailMapper = fanzoneOptinEmailMapper;
  }

  /**
   * To create fanzone optin email
   *
   * @param entity represents requestBody
   * @param brand
   * @return created object in db
   */
  @PostMapping("{brand}/fanzones/fanzone-optin-email")
  public ResponseEntity<FanzoneOptinEmail> create(
      @RequestBody FanzoneOptinEmailDto entity, @PathVariable String brand) {
    FanzoneOptinEmail fanzoneOptinEmail = fanzoneOptinEmailMapper.toEntity(entity);
    fanzoneOptinEmail = fanzonesOptinEmailService.getFanzoneOptinEmail(fanzoneOptinEmail, brand);
    fanzoneOptinEmail =
        fanzonesOptinEmailService.setSeasonStartAndEndDateFromFanzoneSyc(fanzoneOptinEmail, brand);
    return super.create(fanzoneOptinEmail);
  }

  /**
   * To fetch fanzoneOptinEmail from db
   *
   * @param brand
   * @return fanzoneOptinEmail from db
   */
  @GetMapping("{brand}/fanzones/fanzone-optin-email")
  public List<FanzoneOptinEmail> findByPagenameAndColumn(@PathVariable String brand) {
    return super.readAll();
  }

  /**
   * To update fanzoneOptinEmail
   *
   * @param brand
   * @param value represents object Id
   * @param entity represents requestbody
   * @return updated entity in db
   */
  @PutMapping("{brand}/fanzones/fanzone-optin-email/{value}")
  public FanzoneOptinEmail updatePageNameAndColumn(
      @PathVariable String brand,
      @PathVariable String value,
      @RequestBody FanzoneOptinEmailDto entity) {
    FanzoneOptinEmail fanzoneOptinEmail = fanzoneOptinEmailMapper.toEntity(entity);
    fanzoneOptinEmail =
        fanzonesOptinEmailService.setSeasonStartAndEndDateFromFanzoneSyc(fanzoneOptinEmail, brand);
    return super.update(value, fanzoneOptinEmail);
  }

  /**
   * @param brand
   * @param value represents object Id
   */
  @DeleteMapping("{brand}/fanzones/fanzone-optin-email/{value}")
  public void deleteAllByBrandAndPageName(@PathVariable String brand, @PathVariable String value) {
    super.delete(value);
  }
}
