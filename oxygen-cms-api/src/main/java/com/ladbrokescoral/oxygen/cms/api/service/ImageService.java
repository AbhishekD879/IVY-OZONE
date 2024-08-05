package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import java.util.Optional;
import org.springframework.web.multipart.MultipartFile;

public interface ImageService {

  Optional<Filename> upload(
      String brand, MultipartFile image, String path, String fileName, ImageServiceImpl.Size size);

  Optional<Filename> upload(
      String brand, MultipartFile image, String path, ImageServiceImpl.Size size);

  Optional<Filename> upload(String brand, MultipartFile image, String path);

  boolean removeImage(String brand, String path);
}
