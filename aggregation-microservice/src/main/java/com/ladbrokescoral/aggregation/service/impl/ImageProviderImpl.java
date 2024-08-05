package com.ladbrokescoral.aggregation.service.impl;

import com.ladbrokescoral.aggregation.configuration.ApiProperties;
import com.ladbrokescoral.aggregation.model.ImageData;
import com.ladbrokescoral.aggregation.model.SilkUrl;
import com.ladbrokescoral.aggregation.repository.impl.CacheImageRepository;
import com.ladbrokescoral.aggregation.service.ImageProviderService;
import com.ladbrokescoral.aggregation.utils.ImageUtils;
import com.ladbrokescoral.aggregation.utils.SpriteGenerator;
import java.awt.image.BufferedImage;
import java.net.URI;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;
import reactor.core.publisher.Mono;

@Slf4j
@Service
public class ImageProviderImpl implements ImageProviderService {

  private final WebClient providerWebClientForImages;
  private final CacheImageRepository cacheImageRepository;
  private final int numberOfRetries;
  private final SpriteGenerator<BufferedImage> verticalSpriteGenerator;

  @Autowired
  public ImageProviderImpl(
      @Qualifier("providerWebClientForImages") WebClient providerWebClientForImages,
      CacheImageRepository cacheImageRepository,
      ApiProperties properties,
      SpriteGenerator<BufferedImage> verticalSpriteGenerator) {
    this.providerWebClientForImages = providerWebClientForImages;
    this.cacheImageRepository = cacheImageRepository;
    this.numberOfRetries = properties.getImage().getNumberOfRetries();
    this.verticalSpriteGenerator = verticalSpriteGenerator;
  }

  @Override
  public Mono<ImageData> getImage(SilkUrl silkUrl) {
    URI uri = UriComponentsBuilder.fromHttpUrl(silkUrl.getEndpoint()).build().toUri();
    String id = silkUrl.getSilkId();
    String key = silkUrl.getEndpoint();
    return cacheImageRepository
        .get(key)
        .flatMap(bytes -> Mono.just(makeImageData(id, bytes)))
        .switchIfEmpty(getExternalImage(uri, id, key));
  }

  private Mono<ImageData> getExternalImage(URI uri, String id, String key) {
    return providerWebClientForImages
        .get()
        .uri(uri)
        .retrieve()
        .bodyToMono(ByteArrayResource.class)
        .flatMap(
            array ->
                createResponseData(
                    id, Optional.of(ImageUtils.toBufferedImage(array.getByteArray())), null))
        .flatMap(imageData -> cacheImageData(id, key, imageData))
        .retry(numberOfRetries)
        .onErrorResume(res -> createResponseData(id, Optional.empty(), res));
  }

  private Mono<ImageData> cacheImageData(String id, String key, ImageData imageData) {
    log.debug("Save single silk to cache. Silk key = {}", key);
    return imageData
        .getImageContent()
        .filter(verticalSpriteGenerator::isImageWithExpectedSize)
        .map(
            image ->
                cacheImageRepository
                    .save(key, ImageUtils.toByteArray(image))
                    .map(bytes -> makeImageData(id, bytes)))
        .orElse(defaultSilkResponse(id, imageData));
  }

  private ImageData makeImageData(String id, byte[] bytes) {
    log.debug("Get single silk from cache. Silk Id = {}", id);
    return ImageData.builder()
        .imageId(id)
        .imageContent(Optional.ofNullable(ImageUtils.toBufferedImage(bytes)))
        .build();
  }

  private Mono<ImageData> defaultSilkResponse(String id, ImageData imageData) {
    imageData
        .getImageContent()
        .ifPresent(
            img ->
                log.warn(
                    "Image size imageId - {}, width - {}, height - {}",
                    imageData.getImageId(),
                    img.getWidth(),
                    img.getHeight()));
    return createResponseData(id, Optional.empty(), null);
  }

  private Mono<ImageData> createResponseData(
      String id, Optional<BufferedImage> image, Throwable throwable) {

    Mono<ImageData> imageDataMono =
        Mono.just(ImageData.builder().imageId(id).imageContent(image).throwable(throwable).build());
    return imageDataMono;
  }
}
