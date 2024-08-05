package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.SecondaryNameToAssetManagement;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.AssetManagementRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SecondaryNameToAssetRepository;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class AssetManagementService extends AbstractService<AssetManagement> {

  private final AssetManagementRepository repository;
  private final SecondaryNameToAssetRepository secondaryNameToAssetRepository;
  private final ImageService imageService;
  private final SvgImageParser svgImageParser;
  private final String svgMenuPath;

  @Autowired
  public AssetManagementService(
      AssetManagementRepository repository,
      SecondaryNameToAssetRepository secondaryNameToAssetRepository,
      @Value("${images.svg.path}") String svgMenuPath,
      ImageService imageService,
      SvgImageParser svgImageParser) {
    super(repository);
    this.repository = repository;
    this.secondaryNameToAssetRepository = secondaryNameToAssetRepository;
    this.svgMenuPath = svgMenuPath;
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
  }

  public List<AssetManagement> findAllByBrand(String brand) {
    return repository.findAllByBrand(brand);
  }

  @Override
  public AssetManagement prepareModelBeforeSave(AssetManagement entity) {
    validateDuplication(entity);
    return entity;
  }

  @Override
  public void delete(String assetId) {
    secondaryNameToAssetRepository.deleteAllByAssetId(assetId);
    repository.deleteById(assetId);
  }

  @Override
  public AssetManagement save(AssetManagement entity) {
    entity = repository.save(entity);
    updateSecondaryNameToAssetRepository(entity);
    return entity;
  }

  public List<AssetManagement> findByBrandAndNamesAndSportId(
      String brand, List<String> teamNames, Integer sportId) {
    List<AssetManagement> resultList = new ArrayList<>();
    teamNames.forEach(
        name -> {
          Optional<AssetManagement> assetManagement =
              repository.findByTeamNameAndSportIdAndBrand(name, sportId, brand);
          if (assetManagement.isPresent()) {
            resultList.add(assetManagement.get());
          } else {
            secondaryNameToAssetRepository
                .findByTeamNameAndSportIdAndBrand(name, sportId, brand)
                .flatMap(secondary -> repository.findById(secondary.getAssetId()))
                .ifPresent(resultList::add);
          }
        });

    return resultList;
  }

  private void updateSecondaryNameToAssetRepository(AssetManagement assetManagement) {
    List<String> names = new ArrayList<>();
    if (assetManagement.getSecondaryNames() != null) {
      names.addAll(assetManagement.getSecondaryNames());
    }

    List<SecondaryNameToAssetManagement> existedItems =
        secondaryNameToAssetRepository.findAllByAssetId(assetManagement.getId());

    names.forEach(
        name -> {
          if (existedItems.stream().noneMatch(item -> Objects.equals(item.getTeamName(), name))) {
            SecondaryNameToAssetManagement newItem =
                new SecondaryNameToAssetManagement(
                    name,
                    assetManagement.getSportId(),
                    assetManagement.getBrand(),
                    assetManagement.getId());
            secondaryNameToAssetRepository.save(newItem);
          } else {
            existedItems.stream()
                .filter(item -> Objects.equals(item.getTeamName(), name))
                .findAny()
                .ifPresent(
                    secondaryNameItem -> {
                      secondaryNameItem.setSportId(assetManagement.getSportId());
                      secondaryNameToAssetRepository.save(secondaryNameItem);
                    });
          }
        });

    existedItems.stream()
        .filter(item -> !names.contains(item.getTeamName()))
        .forEach(secondaryNameToAssetRepository::delete);
  }

  private void validateDuplication(AssetManagement assetManagement) {
    List<String> names = new ArrayList<>();
    if (assetManagement.getSecondaryNames() != null) {
      names.addAll(assetManagement.getSecondaryNames());
    }
    names.add(assetManagement.getTeamName());

    names.forEach(
        name -> {
          repository
              .findByTeamNameAndSportIdAndBrand(
                  name, assetManagement.getSportId(), assetManagement.getBrand())
              .ifPresent(
                  asset -> {
                    if (!Objects.equals(assetManagement.getId(), asset.getId()))
                      throw new ValidationException(
                          String.format(
                              "Team (with name %s ) already exists with the above details",
                              asset.getTeamName()));
                  });
          secondaryNameToAssetRepository
              .findByTeamNameAndSportIdAndBrand(
                  name, assetManagement.getSportId(), assetManagement.getBrand())
              .ifPresent(
                  asset -> {
                    if (!Objects.equals(assetManagement.getId(), asset.getAssetId()))
                      throw new ValidationException(
                          String.format(
                              "Team (with name %s ) already exists with the above details",
                              asset.getTeamName()));
                  });
        });
  }

  /**
   * This Method is used for to upload Image in AssetManager
   *
   * @param id
   * @param uploadImage
   * @return
   */
  public AssetManagement uploadImageAssetManager(String id, MultipartFile uploadImage) {
    AssetManagement assetManagement = repository.findById(id).orElseThrow(NotFoundException::new);
    uploadImage(uploadImage, assetManagement);
    repository.save(assetManagement);
    return assetManagement;
  }

  /**
   * This Method is used for to upload Image in AssetManager
   *
   * @param uploadImage
   * @param assetManagement
   */
  private void uploadImage(MultipartFile uploadImage, AssetManagement assetManagement) {
    if (uploadImage != null) {
      Filename uploadFileName = getUploadedSvg(assetManagement.getBrand(), uploadImage);
      assetManagement.setTeamsImage(uploadFileName);
      assetManagement.setActive(true);
    }
  }

  /**
   * Handle Uploading SVG images of Contests
   *
   * @param brand - Brand
   * @param svg - uploadImage
   */
  private Filename getUploadedSvg(String brand, MultipartFile svg) {
    Optional<Svg> parsedSvg = svgImageParser.parse(svg);
    if (!parsedSvg.isPresent()) {
      throw new BadRequestException(
          "Svg parsing error for AssetManager image: " + svg.getOriginalFilename());
    }

    Filename fileName =
        imageService
            .upload(brand, svg, svgMenuPath)
            .orElseThrow(
                () ->
                    new FileUploadException(
                        "Image uploading error for AssetManager image: "
                            + svg.getOriginalFilename()));

    fileName.setSvg(parsedSvg.get().getSvg());
    return fileName;
  }

  /**
   * This Method is used for to Delete Image in AssetManager
   *
   * @param id
   * @return AssetManagement
   */
  public AssetManagement deleteImageAssetManager(String id) {
    AssetManagement assetManagement = repository.findById(id).orElseThrow(NotFoundException::new);
    if (null != assetManagement.getTeamsImage()) {
      String imagePath =
          PathUtil.normalizedPath(
              assetManagement.getTeamsImage().getPath(),
              assetManagement.getTeamsImage().getFilename());
      boolean isDeleted = imageService.removeImage(assetManagement.getBrand(), imagePath);
      if (isDeleted) {
        assetManagement.setTeamsImage(null);
        assetManagement.setActive(false);
        repository.save(assetManagement);
        return assetManagement;
      }
    }
    return assetManagement;
  }
}
