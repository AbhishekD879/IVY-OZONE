package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.CreatePotsResponseVO;
import com.ladbrokescoral.oxygen.cms.api.dto.FreeRideCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePotsDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.exception.CampaignAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideCampaignService;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRidePotsService;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@SuppressWarnings("java:S4684")
public class FreeRideCampaignController extends AbstractCrudController<FreeRideCampaign> {

  private final FreeRideCampaignService freeRideCampaignService;

  private final FreeRidePotsService freeRidePotsService;

  private enum Action {
    CREATE("Create"),
    UPDATE("Update");

    private String value;

    Action(String value) {
      this.value = value;
    }

    public String getValue() {
      return this.value;
    }
  }

  public FreeRideCampaignController(
      FreeRideCampaignService freeRideCampaignService, FreeRidePotsService freeRidePotsService) {
    super(freeRideCampaignService);
    this.freeRideCampaignService = freeRideCampaignService;
    this.freeRidePotsService = freeRidePotsService;
  }

  @PostMapping("/freeride/campaign")
  @Override
  public ResponseEntity<FreeRideCampaign> create(@RequestBody @Valid FreeRideCampaign entity) {
    validateCampaignAlreadyExists(entity);
    return super.create(
        populateCreatorAndUpdater(
            prepareModelBeforeSaveOrUpdate(entity, Action.CREATE.getValue())));
  }

  @PutMapping("/freeride/campaign/{id}/{isCampaignDateChanged}")
  public FreeRideCampaign update(
      @PathVariable("id") String campaingId,
      @PathVariable("isCampaignDateChanged") boolean isCampaignDateChanged,
      @RequestBody @Valid FreeRideCampaign entity) {
    if (isCampaignDateChanged) {
      validateCampaignAlreadyExists(entity);
    }
    freeRideCampaignService.mapProxyChoice(entity);
    return super.update(
        campaingId,
        populateCreatorAndUpdater(
            prepareModelBeforeSaveOrUpdate(entity, Action.UPDATE.getValue())));
  }

  @GetMapping("/freeride/campaign/{id}")
  public FreeRideCampaign readById(@PathVariable("id") String campaignId) {
    return super.read(campaignId);
  }

  @GetMapping("/freeride/campaign/brand/{brand}")
  public List<FreeRideCampaignDto> getAllByBrand(@PathVariable("brand") String brand, Sort sort) {
    return freeRideCampaignService.findAllByBrand(brand, sort);
  }

  @DeleteMapping("/freeride/campaign/brand/{brand}/{id}")
  public ResponseEntity<FreeRideCampaign> delete(
      @PathVariable("id") String campaignId, @PathVariable("brand") String brand) {
    freeRideCampaignService.deleteFreeRideMsCampaign(campaignId, brand);
    return super.delete(campaignId);
  }

  @GetMapping("/freeride/campaign/createpots/{id}")
  public ResponseEntity<CreatePotsResponseVO> createPot(@PathVariable("id") String campaingId) {
    FreeRideCampaign updatedFreeRideCampaign = freeRidePotsService.createPots(campaingId);
    return ResponseEntity.ok(
        new CreatePotsResponseVO(
            updatedFreeRideCampaign.getIsPotsCreated(), "Pots created successfully"));
  }

  @GetMapping("/freeride/campaign/viewpots/brand/{brand}/{id}")
  public ResponseEntity<Collection<FreeRidePotsDetailsDto>> viewPots(
      @PathVariable("id") String campaingId, @PathVariable("brand") String brand) {
    return ResponseEntity.ok(freeRidePotsService.getPotsDetails(campaingId, brand));
  }

  private void validateCampaignAlreadyExists(FreeRideCampaign freeRideCampaign) {
    List<FreeRideCampaign> campaignList =
        freeRideCampaignService.findAllByBrandAndDisplayFromBetween(
            freeRideCampaign.getBrand(), freeRideCampaign.getDisplayFrom());
    if (!campaignList.isEmpty()) {
      throw new CampaignAlreadyExistException("Another campaign is already saved with same date");
    }
  }

  private final FreeRideCampaign prepareModelBeforeSaveOrUpdate(
      FreeRideCampaign freeRideCampaign, String actionType) {
    freeRideCampaign.setId(null);
    String loggedUserId =
        Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
            .filter(Authentication::isAuthenticated)
            .map(Authentication::getPrincipal)
            .map(User.class::cast)
            .map(User::getId)
            .orElse(null);
    if (actionType.equalsIgnoreCase(Action.CREATE.getValue())) {
      freeRideCampaign.setCreatedBy(loggedUserId);
    }
    freeRideCampaign.setUpdatedBy(loggedUserId);
    return freeRideCampaign;
  }
}
