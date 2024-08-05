package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ContestRequest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import com.ladbrokescoral.oxygen.cms.api.service.ContestService;
import java.util.List;
import java.util.Objects;
import javax.validation.Valid;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
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

/** Contest Controller - BMA-58712 */
@RestController
public class ContestController extends AbstractSortableController<Contest> {

  private final ContestService service;

  @Autowired
  ContestController(ContestService crudService) {
    super(crudService);
    this.service = crudService;
  }

  /** Create Contests */
  @PostMapping("contest")
  public ResponseEntity<Contest> create(@RequestBody @Valid ContestRequest request) {
    Contest contest = new Contest();
    request.setContestURL(null);
    BeanUtils.copyProperties(request, contest);
    service.setContestWithOfferIds(contest);
    Contest newContest = super.create(contest).getBody();
    if (Objects.nonNull(request.getIntialContestId())) {
      service.populateContestPrizes(request, newContest);
    }
    return new ResponseEntity<>(newContest, HttpStatus.CREATED);
  }

  /** Create cloned Contests */
  @PostMapping("cloneContest")
  public ResponseEntity<Contest> createClonedContest(@RequestBody @Valid ContestRequest request) {
    Contest clonedContest = new Contest();
    request.setContestURL(null);
    BeanUtils.copyProperties(request, clonedContest);
    service.setContestWithOfferIds(clonedContest);
    Contest newClonedContest = super.create(clonedContest).getBody();
    service.populateContestPrizes(request, newClonedContest);
    return new ResponseEntity<>(newClonedContest, HttpStatus.CREATED);
  }

  /** List All Contests */
  @GetMapping("contest")
  @Override
  public List<Contest> readAll() {
    return super.readAll();
  }

  /**
   * List All Contests based on Id
   *
   * @param id - Contests Id
   */
  @GetMapping("contest/{id}")
  @Override
  public Contest read(@PathVariable String id) {
    return service.checkForEventCompleted(id);
  }

  /**
   * Update Contests based on Id
   *
   * @param id - Contests Id
   */
  @PutMapping("contest/{id}")
  @Override
  public Contest update(@PathVariable String id, @RequestBody Contest entity) {
    if (entity.isInvitationalContest() && entity.getContestURL() == null)
      return super.update(id, service.generateURL(entity));
    return super.update(id, entity);
  }

  /**
   * Delete Contests based on Id
   *
   * @param id - Contests Id
   */
  @DeleteMapping("contest/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  /**
   * List All Contests based on Brand
   *
   * @param brand - Brand
   */
  @GetMapping("contest/brand/{brand}")
  @Override
  public List<Contest> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  /**
   * Upload images of Contests based on Id
   *
   * @param id - Id of the Contests record which has to be Uploaded
   */
  @PostMapping(value = "contest/{id}/file")
  public Contest uploadImage(
      @PathVariable String id,
      @RequestParam(value = "contestLogo", required = false) MultipartFile contestLogo,
      @RequestParam(value = "contestIcon", required = false) MultipartFile contestIcon) {
    return service.handleFileUploading(id, contestLogo, contestIcon);
  }

  /**
   * Delete images of Contests based on Id
   *
   * @param id - Id of the Contests record which has to be Deleted
   */
  @DeleteMapping("contest/{id}/file")
  public Contest deleteImage(
      @PathVariable String id, @RequestParam(value = "imageType") String imageType) {
    return service.handleFileDelete(id, imageType);
  }

  /** Create Order for Contests */
  @PostMapping("contest/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
