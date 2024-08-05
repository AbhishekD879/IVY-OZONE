package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.ContestPrizeService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/** Contest Prizes Controller */
@RestController
public class ContestPrizeController extends AbstractCrudController<ContestPrize> {

  private final ContestPrizeService contestPrizesService;

  @Autowired
  ContestPrizeController(ContestPrizeService crudService) {
    super(crudService);
    this.contestPrizesService = crudService;
  }

  /**
   * List All Contest Prizes based on Contest Id
   *
   * @param contestId - Contest Id
   */
  @GetMapping("contestprize/{contestId}")
  public List<ContestPrize> getByContestId(@PathVariable String contestId) {
    return contestPrizesService.getByContestId(contestId);
  }

  @Override
  @PostMapping("contestprize")
  public ResponseEntity<ContestPrize> create(@RequestBody @Valid ContestPrize entity) {
    return super.create(entity);
  }

  /**
   * Update Contest Prizes
   *
   * @param entity - Contest Prizes Object
   * @param id - Id of the Contest Prizes record which has to be Updated
   */
  @PutMapping("contestprize/{id}")
  @Override
  public ContestPrize update(@PathVariable String id, @RequestBody ContestPrize entity) {
    return super.update(id, entity);
  }

  /**
   * List Contest Prizes based on prize id
   *
   * @param entity - Contest Prizes Object
   * @param id - Id of the Contest Prizes
   */
  @GetMapping("contestprize/prizeid/{id}")
  @Override
  public ContestPrize read(@PathVariable String id) {
    return super.read(id);
  }

  /**
   * Delete Contest Prizes
   *
   * @param id - Id of the Contest Prizes record which has to be Deleted
   */
  @DeleteMapping("contestprize/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    ContestPrize contestPrizes =
        contestPrizesService.findOne(id).orElseThrow(NotFoundException::new);
    return super.delete(Optional.of(contestPrizes));
  }

  /**
   * Upload images of Contest Prizes
   *
   * @param id - Id of the Contest Prizes record which has to be Uploaded
   */
  @PostMapping(value = "contestprize/{id}/file")
  public ContestPrize uploadImage(
      @PathVariable String id,
      @RequestParam(value = "iconFile", required = false) MultipartFile contestprizesIcon,
      @RequestParam(value = "signPostingFile", required = false)
          MultipartFile contestprizesSignPosting) {
    return contestPrizesService.handleFileUploading(
        id, contestprizesIcon, contestprizesSignPosting);
  }

  /**
   * Delete images of Contest Prizes
   *
   * @param id - Id of the Contest Prizes record which has to be Deleted
   */
  @DeleteMapping("contestprize/{id}/file")
  public ContestPrize deleteImage(
      @PathVariable String id, @RequestParam(value = "imageType") String imageType) {
    return contestPrizesService.handleFileDelete(id, imageType);
  }
}
