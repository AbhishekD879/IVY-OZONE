package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Category;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTracks;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportTrackRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import java.util.*;
import java.util.function.Consumer;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.lang3.ObjectUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
@Slf4j
public class VirtualSportTrackService extends SortableService<VirtualSportTrack> {
  public static final Pattern SINGLE_OR_PATTERN = Pattern.compile("\\|");
  public static final Pattern NON_ALPHANUMERIC_PATTERN = Pattern.compile("[^A-Za-z0-9]");
  private final VirtualSportTrackRepository virtualSportTrackRepository;
  private final VirtualSportService virtualSportService;
  private final ImageService imageService;

  private final SiteServeApiProvider siteServeApiProvider;

  private final String virtualsSportTrackImageRootPath;

  public VirtualSportTrackService(
      @Value("${images.virtualSportTrack.path}") String virtualsSportTrackImageRootPath,
      VirtualSportTrackRepository virtualSportTrackRepository,
      VirtualSportService virtualSportService,
      SiteServeApiProvider siteServeApiProvider,
      ImageService imageService) {
    super(virtualSportTrackRepository);
    this.virtualsSportTrackImageRootPath = virtualsSportTrackImageRootPath;
    this.virtualSportTrackRepository = virtualSportTrackRepository;
    this.virtualSportService = virtualSportService;
    this.siteServeApiProvider = siteServeApiProvider;
    this.imageService = imageService;
  }

  @Override
  @SuppressWarnings("unchecked")
  public VirtualSportTrack save(VirtualSportTrack virtualSportTrack) {
    if (!virtualSportService.findOne(virtualSportTrack.getSportId()).isPresent()) {
      throw new ValidationException(
          String.format(
              "Virtual Sport with id '%s' doesn't exist", virtualSportTrack.getSportId()));
    }
    return super.save(virtualSportTrack);
  }

  @Override
  public VirtualSportTrack update(
      VirtualSportTrack existingEntity, VirtualSportTrack updateEntity) {
    prepareModelBeforeUpdate(existingEntity, updateEntity);
    return save(updateEntity);
  }

  @Override
  public VirtualSportTrack prepareModelBeforeSave(VirtualSportTrack virtualSportTrack) {
    setClassnameForClassId(virtualSportTrack);
    return virtualSportTrack;
  }

  public VirtualSportTrack prepareModelBeforeUpdate(
      VirtualSportTrack existingEntity, VirtualSportTrack updateEntity) {
    if (!existingEntity.getTitle().equals(updateEntity.getTitle())) {
      updateEntity.setRunnerImages(new ArrayList<>());
      updateEntity.setEventRunnerImages(new HashMap<>());
      updateEntity.setEventAliases(new HashMap<>());
      updateEntity.setShowRunnerImages(false);
    }

    if (!existingEntity.getClassId().equals(updateEntity.getClassId())) {
      setClassnameForClassId(updateEntity);
    }

    return updateEntity;
  }

  public List<VirtualSportTrack> findActiveTracksBySportId(String sportId) {
    return virtualSportTrackRepository.findBySportIdAndActiveIsTrueOrderBySortOrderAsc(sportId);
  }

  public List<VirtualSportTrack> findBySportId(String sportId) {
    return virtualSportTrackRepository.findBySportIdOrderBySortOrderAsc(sportId);
  }

  public VirtualSportTrack attachImage(
      String id, @ValidFileType({"png", "jpg", "jpeg"}) MultipartFile image, String eventName) {
    // construct filename to save under
    VirtualSportTrack virtualSportTrack = findOne(id).orElseThrow(NotFoundException::new);
    VirtualSport virtualSport =
        virtualSportService
            .findOne(virtualSportTrack.getSportId())
            .orElseThrow(NotFoundException::new);

    List<Filename> currentlyPresentImages;
    Consumer<List<Filename>> runnerImagesSetter;

    if (StringUtils.isNotBlank(eventName)) {
      currentlyPresentImages = virtualSportTrack.getEventRunnerImages().get(eventName);
      runnerImagesSetter =
          images -> virtualSportTrack.getEventRunnerImages().put(eventName, images);

      virtualSportTrack.getEventAliases().putIfAbsent(eventName, formatAsAlias(eventName));
    } else {
      currentlyPresentImages = virtualSportTrack.getRunnerImages();
      runnerImagesSetter = virtualSportTrack::setRunnerImages;
    }

    String uploadImagePath =
        formatUploadImageFilePathForVirtualSport(virtualSportTrack, virtualSport, eventName);
    String uploadImageName = formatUpoadImageNameForFile(image);
    String uploadImageNameWithExtension =
        uploadImageName + "." + ImageUtil.getImageExtension(image.getOriginalFilename());

    List<Filename> otherNameCurrentlyPresentImages = new ArrayList<>();

    if (ObjectUtils.isNotEmpty(currentlyPresentImages)) {
      // remove image with same name if present
      otherNameCurrentlyPresentImages =
          currentlyPresentImages.stream()
              .filter(filename -> !filename.getFilename().equals(uploadImageNameWithExtension))
              .collect(Collectors.toList());

      if (currentlyPresentImages.size() != otherNameCurrentlyPresentImages.size()) {
        removeSameNameImage(
            virtualSportTrack, currentlyPresentImages, otherNameCurrentlyPresentImages);
      }
    }

    // upload the image and save updated sportTrack
    Filename newlyUploadedImage =
        uploadImageForTrack(image, virtualSportTrack, uploadImagePath, uploadImageName);

    otherNameCurrentlyPresentImages.add(0, newlyUploadedImage);
    runnerImagesSetter.accept(otherNameCurrentlyPresentImages);

    return save(virtualSportTrack);
  }

  public void removeInCloudImagesForVirtualSportTrack(VirtualSportTrack virtualSportTrack) {
    List<String> brokenRemovesFullPaths = new ArrayList<>();
    Stream.concat(
            virtualSportTrack.getRunnerImages().stream(),
            virtualSportTrack.getEventRunnerImages().values().stream().flatMap(Collection::stream))
        .forEach(
            (Filename image) -> {
              log.info(
                  String.format(
                      "Removing image for virtualSportTrack[%s]: %s",
                      virtualSportTrack.getTitle(), image.getFullPath()));
              if (!imageService.removeImage(virtualSportTrack.getBrand(), image.getFullPath())) {
                brokenRemovesFullPaths.add(image.getFullPath());
              }
            });

    if (!brokenRemovesFullPaths.isEmpty()) {
      log.error(
          String.format(
              "Exception on removing image(s): %s for virtual sport track: %s",
              brokenRemovesFullPaths, virtualSportTrack.getTitle()));
    }
  }

  public VirtualSportTrack removeImageForVirtualSportTrack(
      String sportTrackId, VirtualSportTracks.RemoveImageRequest removeRequest) {
    VirtualSportTrack virtualSportTrack = findOne(sportTrackId).orElseThrow(NotFoundException::new);

    removeRequest
        .imagesToRemove(virtualSportTrack)
        .forEach(
            (Filename image) -> {
              if (!imageService.removeImage(virtualSportTrack.getBrand(), image.getFullPath())) {
                throw new FileUploadException(
                    String.format(
                        "Exception on removing image %s for virtual sport track: %s",
                        image.getFullPath(), virtualSportTrack.getTitle()));
              }
            });

    return save(virtualSportTrack);
  }

  public String formatAsAlias(String unformatted) {
    return NON_ALPHANUMERIC_PATTERN
        .matcher(SINGLE_OR_PATTERN.matcher(unformatted).replaceAll(""))
        .replaceAll("-")
        .toLowerCase();
  }

  private void setClassnameForClassId(VirtualSportTrack virtualSportTrack) {
    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation(
                    "class.id", BinaryOperation.equals, virtualSportTrack.getClassId())
                .build();
    List<Category> classes =
        this.siteServeApiProvider
            .api(virtualSportTrack.getBrand())
            .getClasses(simpleFilter, new ExistsFilter.ExistsFilterBuilder().build())
            .orElseGet(Collections::emptyList);
    if (!classes.isEmpty()) {
      virtualSportTrack.setClassName(classes.get(0).getName());
    } else {
      throw new ValidationException("Class not found for classId" + virtualSportTrack.getClassId());
    }
  }

  private String formatUploadImageFilePathForVirtualSport(
      VirtualSportTrack virtualSportTrack, VirtualSport virtualSport, String eventName) {
    return String.format(
        "%s/%s/%s/%s",
        virtualsSportTrackImageRootPath,
        formatAsAlias(virtualSport.getTitle()),
        formatAsAlias(virtualSportTrack.getTitle()),
        StringUtils.isNotBlank(eventName) ? formatAsAlias(eventName) : StringUtils.EMPTY);
  }

  private String formatUpoadImageNameForFile(MultipartFile file) {
    return formatAsAlias(FilenameUtils.removeExtension(file.getOriginalFilename()));
  }

  private void removeSameNameImage(
      VirtualSportTrack virtualSportTrack,
      List<Filename> currentlyPresentImages,
      List<Filename> otherNameCurrentlyPresentImages) {
    currentlyPresentImages.stream()
        .filter(filename -> !otherNameCurrentlyPresentImages.contains(filename))
        .forEach(
            (Filename filename) -> {
              if (!imageService.removeImage(virtualSportTrack.getBrand(), filename.getFullPath())) {
                String message =
                    "Exception on removing image "
                        + filename.getFullPath()
                        + " for virtual sport track: "
                        + virtualSportTrack.getTitle();
                throw new FileUploadException(message);
              }
            });
  }

  private Filename uploadImageForTrack(
      MultipartFile file,
      VirtualSportTrack virtualSportTrack,
      String pathForImageUploading,
      String nameToUploadWith) {
    String message = " for virtual sport track: " + virtualSportTrack.getTitle();

    return imageService
        .upload(virtualSportTrack.getBrand(), file, pathForImageUploading, nameToUploadWith, null)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + file.getOriginalFilename() + message));
  }
}
