package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Offer;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.IdNamePair;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class OfferService extends SortableService<Offer> {

  private final OfferRepository offerRepository;
  private final OfferExtendedRepository extendedRepository;
  private final OfferModuleService offerModuleService;
  private final ImageService imageService;
  private final String imgPathMedium;
  private final String imgSize;

  @Autowired
  public OfferService(
      OfferRepository offerRepository,
      OfferExtendedRepository extendedRepository,
      OfferModuleService offerModuleService,
      ImageService imageService,
      @Value("${images.offers.medium}") String imgPathMedium,
      @Value("${images.offers.size}") String imgSize) {
    super(offerRepository);
    this.offerRepository = offerRepository;
    this.extendedRepository = extendedRepository;
    this.offerModuleService = offerModuleService;
    this.imageService = imageService;
    this.imgPathMedium = imgPathMedium;
    this.imgSize = imgSize;
  }

  @Override
  public Offer save(Offer entity) {
    Offer savedOffer = offerRepository.save(entity);
    populateWithModuleName(Optional.ofNullable(savedOffer));
    return savedOffer;
  }

  @Override
  public Offer update(Offer existingEntity, Offer updateEntity) {
    prepareModelBeforeSave(updateEntity);
    updateEntity.setImage(existingEntity.getImage());
    updateEntity.setImageUri(existingEntity.getImageUri());
    return save(updateEntity);
  }

  @FortifyXSSValidate("return")
  @Override
  public Optional<Offer> findOne(String id) {
    Optional<Offer> offer = offerRepository.findById(id);
    populateWithModuleName(offer);
    return offer;
  }

  @Override
  public List<Offer> findAll() {
    List<Offer> offers = offerRepository.findAll(SortableService.SORT_BY_SORT_ORDER_ASC);
    populateWithModuleName(offers);
    return offers;
  }

  private void populateWithModuleName(Optional<Offer> offer) {
    offer
        .filter(o -> Objects.nonNull(o.getModule()))
        .filter(o -> Util.isValidObjectIdString(o.getModule().toString()))
        .ifPresent(this::setModuleName);
  }

  private void populateWithModuleName(List<Offer> offers) {
    offers.stream()
        .filter(offer -> Objects.nonNull(offer.getModule()))
        .filter(offer -> Util.isValidObjectIdString(offer.getModule().toString()))
        .forEach(this::setModuleName);
  }

  @Override
  public List<Offer> findByBrand(String brand) {
    List<Offer> offers = offerRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
    populateWithModuleName(offers);
    return offers;
  }

  public List<Offer> findOffers(String brand, String deviceType, List<ObjectId> moduleIds) {
    List<Offer> offers = extendedRepository.findOffers(brand, deviceType, moduleIds);
    populateWithModuleName(offers);
    return offers;
  }

  @Override
  public List<Offer> save(Iterable<Offer> entites) {
    List<Offer> offers = offerRepository.saveAll(entites);
    populateWithModuleName(offers);
    return offers;
  }

  public Optional<Offer> attachImage(
      Offer offer, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image) {

    ImageServiceImpl.Size size = new ImageServiceImpl.Size(imgSize);
    Optional<Filename> uploaded = imageService.upload(offer.getBrand(), image, imgPathMedium, size);
    Optional<Offer> maybeOffer =
        uploaded.map(
            uploadedImage -> {
              offer.setImageUri(
                  PathUtil.normalizedPath(imgPathMedium, uploadedImage.getFilename()));
              uploadedImage.setFilename(image.getOriginalFilename());
              uploadedImage.setPath(imgPathMedium);
              offer.setImage(uploadedImage);
              return offer;
            });
    populateWithModuleName(maybeOffer);
    return maybeOffer;
  }

  public Optional<Offer> removeImage(Offer offer) {
    Optional<Offer> maybeOffer =
        Optional.ofNullable(offer.getImageUri())
            .map(
                uriMedium -> {
                  Boolean isDeleted = imageService.removeImage(offer.getBrand(), uriMedium);
                  log.info("File {} removal status : {}", uriMedium, isDeleted);
                  offer.setImageUri(null);
                  offer.setImage(null);
                  return offer;
                });
    populateWithModuleName(maybeOffer);
    return maybeOffer;
  }

  @Override
  public Offer prepareModelBeforeSave(Offer offer) {
    offer.setVipLevels(generateVipLevels(offer));
    return offer;
  }

  private List<Integer> generateVipLevels(Offer offer) {
    if (!StringUtils.isBlank(offer.getVipLevelsInput())) {
      return Util.hyphenatedAndCommaSeparatedNumbersToList(offer.getVipLevelsInput());
    }
    return null;
  }

  private void setModuleName(Offer offer) {
    IdNamePair idNamePairById = offerModuleService.findIdNamePairById(offer.getModule().toString());
    if (idNamePairById != null) {
      offer.setModuleName(idNamePairById.getName());
    }
  }
}
