package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BetPackBannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceBannerService;
import java.util.List;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.bson.types.ObjectId;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@Slf4j
public class BetPackMarketPlaceBannerController extends AbstractSortableController<BetPackBanner> {

  private final BetPackMarketPlaceBannerService betPackEnablerBannerService;
  private final ModelMapper modelMapper;

  public BetPackMarketPlaceBannerController(
      BetPackMarketPlaceBannerService betPackEnablerBannerService, ModelMapper modelMapper) {
    super(betPackEnablerBannerService);
    this.betPackEnablerBannerService = betPackEnablerBannerService;
    this.modelMapper = modelMapper;
  }

  @GetMapping("bet-pack/banner/brand/{brand}")
  public ResponseEntity<BetPackBanner> getBetPackBannerByBrand(@PathVariable String brand) {
    List<BetPackBanner> betPackBanner = betPackEnablerBannerService.getBetPackBannerByBrand(brand);

    if (CollectionUtils.isNotEmpty(betPackBanner)) {
      BetPackBanner betBanner = betPackBanner.get(0);
      return new ResponseEntity<>(betBanner, HttpStatus.OK);
    }
    return new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }

  @PostMapping("bet-pack/banner")
  public BetPackBanner createBanner(@ModelAttribute @Valid BetPackBannerDto betPackBannerDto) {
    String bannerId = null;
    try {
      BetPackBanner betPackBanner = modelMapper.map(betPackBannerDto, BetPackBanner.class);
      bannerId = ObjectId.get().toHexString();
      betPackBanner.setId(bannerId);
      return betPackEnablerBannerService.uploadBannerImage(
          betPackBannerDto.getBannerImg(), betPackBanner);
    } catch (FileUploadException ex) {
      throw new BetPackMarketPlaceException("File Upload Failed");
    } catch (Exception ex) {
      super.delete(bannerId);
      throw new BetPackMarketPlaceException("Error occurred while creating banner");
    }
  }

  @PutMapping("bet-pack/banner/{id}")
  public BetPackBanner update(
      @PathVariable("id") String id, @ModelAttribute @Valid BetPackBannerDto betPackBannerDto) {
    try {
      BetPackBanner betPackBanner = modelMapper.map(betPackBannerDto, BetPackBanner.class);
      BetPackBanner betPackBannerUpdatedEntity = super.update(id, betPackBanner);
      return betPackEnablerBannerService.uploadBannerImage(
          betPackBannerDto.getBannerImg(), betPackBannerUpdatedEntity);
    } catch (FileUploadException ex) {
      log.error("file upload failed for bannerId {}", id);
      throw new BetPackMarketPlaceException("File Upload Failed ");
    } catch (Exception ex) {
      log.error("Exception occurred while updating banner bannerId {}", id);
      throw new BetPackMarketPlaceException("Error occurred while updating banner");
    }
  }

  @DeleteMapping("bet-pack/banner/{id}")
  public ResponseEntity<BetPackBanner> deleteById(@PathVariable String id) {
    return super.delete(id);
  }
}
