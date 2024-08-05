package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BetPackLabelDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceLabelService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.apache.commons.collections4.CollectionUtils;
import org.modelmapper.ModelMapper;
import org.springframework.beans.BeanUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class BetPackMarketPlaceLabelController extends AbstractSortableController<BetPackLabel> {

  private final BetPackMarketPlaceLabelService betPackMarketPlaceLabelService;
  private final ModelMapper modelMapper;

  public BetPackMarketPlaceLabelController(
      BetPackMarketPlaceLabelService betPackMarketPlaceLabelService, ModelMapper modelMapper) {
    super(betPackMarketPlaceLabelService);
    this.betPackMarketPlaceLabelService = betPackMarketPlaceLabelService;
    this.modelMapper = modelMapper;
  }

  @GetMapping("bet-pack/labels")
  public List<BetPackLabel> getAllBetPackLabels() {
    return super.readAll();
  }

  @GetMapping("bet-pack/label/brand/{brand}")
  public ResponseEntity<BetPackLabel> getBetPackLabelByBrand(@PathVariable String brand) {
    List<BetPackLabel> betPackLabels = betPackMarketPlaceLabelService.getBetPackLabelByBrand(brand);
    if (CollectionUtils.isNotEmpty(betPackLabels)) {
      BetPackLabel label = betPackLabels.get(0);
      return new ResponseEntity<>(label, HttpStatus.OK);
    }
    return new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }

  @PostMapping("bet-pack/label")
  public ResponseEntity<BetPackLabel> createLabel(
      @RequestBody @Valid BetPackLabelDto betPackLabelDto) {
    if ((betPackLabelDto.isAllFilterPillMessageActive()
            && (null != betPackLabelDto.getAllFilterPillMessage()))
        || (!betPackLabelDto.isAllFilterPillMessageActive())) {
      BetPackLabel betPackLabelEntity = modelMapper.map(betPackLabelDto, BetPackLabel.class);
      return super.create(betPackLabelEntity);
    }
    return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
  }

  @GetMapping("bet-pack/label/{id}")
  public ResponseEntity<BetPackLabel> getBetPackLabel(@PathVariable String id) {
    return new ResponseEntity<>(super.read(id), HttpStatus.OK);
  }

  @PutMapping("bet-pack/label/{id}")
  public BetPackLabel updateBetPackLabel(
      @PathVariable("id") String id, @Valid @RequestBody BetPackLabelDto updateEntity) {
    BetPackLabel betPackLabelEntity = new BetPackLabel();
    BeanUtils.copyProperties(updateEntity, betPackLabelEntity);
    return super.update(id, betPackLabelEntity);
  }

  @DeleteMapping("bet-pack/label/{id}")
  @Override
  public ResponseEntity<BetPackLabel> delete(@PathVariable("id") String id) {
    Optional<BetPackLabel> maybeEntity = betPackMarketPlaceLabelService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    betPackMarketPlaceLabelService.handleRemoveImage(maybeEntity.get());
    betPackMarketPlaceLabelService.delete(id);
    return new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }

  @PostMapping("bet-pack/label/uploadImage/{bannerId}")
  public ResponseEntity<BetPackLabel> handleFileUpload(
      @PathVariable("bannerId") String bannerId, @RequestParam("file") MultipartFile file) {
    BetPackLabel betPackLabel =
        betPackMarketPlaceLabelService.uploadBackgroundImage(bannerId, file);
    return new ResponseEntity<>(betPackLabel, HttpStatus.OK);
  }

  @DeleteMapping("bet-pack/label/remove-image/{bannerId}")
  public ResponseEntity<BetPackLabel> handleFileRemove(@PathVariable("bannerId") String bannerId) {
    Optional<BetPackLabel> maybeEntity = betPackMarketPlaceLabelService.findOne(bannerId);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    BetPackLabel betPackLabel = betPackMarketPlaceLabelService.handleRemoveImage(maybeEntity.get());
    return new ResponseEntity<>(betPackMarketPlaceLabelService.save(betPackLabel), HttpStatus.OK);
  }
}
