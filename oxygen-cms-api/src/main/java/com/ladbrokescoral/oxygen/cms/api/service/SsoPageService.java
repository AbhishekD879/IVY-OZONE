package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SsoPageExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SsoPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class SsoPageService extends ImageOperationsService<SsoPage> {

  private final SsoPageExtendedRepository extendedRepository;
  private final ImageService imageService;
  private final String imgPathMedium;
  private final String imgPathOriginal;
  private final String imgSize;

  @Autowired
  public SsoPageService(
      SsoPageRepository ssoPageRepository,
      SsoPageExtendedRepository extendedRepository,
      ImageService imageService,
      @Value("${images.ssopage.medium}") String imgPathMedium,
      @Value("${images.ssopage.original}") String imgPathOriginal,
      @Value("${images.ssopage.size}") String imgSize) {
    super(ssoPageRepository);
    this.extendedRepository = extendedRepository;
    this.imageService = imageService;
    this.imgPathMedium = imgPathMedium;
    this.imgPathOriginal = imgPathOriginal;
    this.imgSize = imgSize;
  }

  public List<SsoPage> findSsoPages(String brand, String osType) {
    return extendedRepository.findSsoPages(brand, osType);
  }

  @Override
  public SsoPage prepareModelBeforeSave(SsoPage model) {
    model.setTitleBrand(generateTitleBrand(model));
    return model;
  }

  private String generateTitleBrand(SsoPage model) {
    return new StringBuilder(model.getTitle())
        .append("-")
        .append(model.getBrand())
        .toString()
        .toLowerCase()
        .replace(" ", "-");
  }

  public Optional<SsoPage> attachImage(
      SsoPage ssoPage, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image) {
    // upload original image
    imageService
        .upload(ssoPage.getBrand(), image, imgPathOriginal, null)
        .ifPresent(
            uploadedImage -> {
              ssoPage.setUriOriginal(
                  PathUtil.normalizedPath(imgPathOriginal, uploadedImage.getFilename()));
              uploadedImage.setFilename(uploadedImage.getFilename());
              uploadedImage.setPath(imgPathOriginal);
              ssoPage.setFilename(uploadedImage);
            });
    // upload resized image
    ImageServiceImpl.Size size = new ImageServiceImpl.Size(imgSize);
    return imageService
        .upload(ssoPage.getBrand(), image, imgPathMedium, size)
        .map(
            uploadedImage -> {
              ssoPage.setUriMedium(
                  PathUtil.normalizedPath(imgPathMedium, uploadedImage.getFilename()));
              ssoPage.setWidthMedium(size.getWidth());
              ssoPage.setHeightMedium(size.getHeight());
              return ssoPage;
            });
  }

  @Override
  public Optional<SsoPage> removeImages(SsoPage ssoPage) {
    return Optional.ofNullable(ssoPage)
        .map(
            sso -> {
              if (Objects.nonNull(sso.getUriMedium())) {
                Boolean isDeletedMedium =
                    imageService.removeImage(ssoPage.getBrand(), sso.getUriMedium());
                log.info(
                    "SSO medium file {} removal status : {}", sso.getUriMedium(), isDeletedMedium);
              }
              if (Objects.nonNull(sso.getUriOriginal())) {
                Boolean isDeletedOriginal =
                    imageService.removeImage(ssoPage.getBrand(), sso.getUriOriginal());
                log.info(
                    "SSO original file {} removal status : {}",
                    sso.getUriOriginal(),
                    isDeletedOriginal);
              }
              ssoPage.setUriMedium(null);
              ssoPage.setUriOriginal(null);
              ssoPage.setFilename(null);
              return ssoPage;
            });
  }
}
