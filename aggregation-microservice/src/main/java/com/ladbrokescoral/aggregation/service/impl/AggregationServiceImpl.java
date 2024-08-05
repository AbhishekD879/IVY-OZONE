package com.ladbrokescoral.aggregation.service.impl;

import com.ladbrokescoral.aggregation.configuration.SilksProperties;
import com.ladbrokescoral.aggregation.configuration.SilksProperties.ImageProvider;
import com.ladbrokescoral.aggregation.exception.BadRequestException;
import com.ladbrokescoral.aggregation.model.ImageData;
import com.ladbrokescoral.aggregation.model.SilkUrl;
import com.ladbrokescoral.aggregation.service.AggregationService;
import com.ladbrokescoral.aggregation.service.ImageProviderService;
import com.ladbrokescoral.aggregation.service.SilkUrlProviderService;
import com.ladbrokescoral.aggregation.utils.ImageUtils;
import com.ladbrokescoral.aggregation.utils.SpriteGenerator;
import com.newrelic.api.agent.NewRelic;
import java.awt.image.BufferedImage;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@Slf4j
@RequiredArgsConstructor
public class AggregationServiceImpl implements AggregationService {

  private final SpriteGenerator<BufferedImage> spriteGenerator;
  private final SilksProperties silksProperties;
  private final ImageProviderService provider;
  private final SilkUrlProviderService silkUrlProvider;

  @Override
  public Mono<byte[]> imageAggregationByProvider(
      List<String> silkIds, String imageProvider, String requestId) {
    List<String> silks = cleanSilkIds(silkIds);
    return aggregate(
        convertToSilk(imageProvider, new HashSet<>(silks)), imageProvider, silks, requestId);
  }

  @Override
  public Mono<byte[]> imageAggregationByBrand(
      List<String> eventIds, String brand, String requestId) {
    List<String> silks = cleanSilkIds(eventIds);
    return fetchSilks(brand, silks)
        .flatMap(
            silk -> {
              List<String> silkIds =
                  silk.stream().map(SilkUrl::getSilkId).collect(Collectors.toList());
              return aggregate(Flux.fromIterable(silk), brand, silkIds, requestId);
            });
  }

  private List<String> cleanSilkIds(List<String> silkIds) {
    return silkIds.stream().map(silkId -> silkId.split("[.]")[0]).collect(Collectors.toList());
  }

  private Flux<SilkUrl> convertToSilk(String imageProvider, Set<String> silkIds) {
    return Flux.fromIterable(silkIds)
        .map(
            id ->
                SilkUrl.builder()
                    .endpoint(
                        getImageProvider(imageProvider).getEndpoint(),
                        id,
                        silksProperties.getExpectedExtension())
                    .silkId(id)
                    .build());
  }

  private Mono<List<SilkUrl>> fetchSilks(String brand, List<String> eventIds) {
    return silkUrlProvider.getSilksUrlsByEventIds(brand, eventIds);
  }

  /**
   * Method aggregates silks to sprite
   *
   * @param silkFlux silks to process
   * @param imageProvider silks provider
   * @param silkIds need to keep order of requested silks
   * @param requestId for log purposes
   */
  private Mono<byte[]> aggregate(
      Flux<SilkUrl> silkFlux, String imageProvider, List<String> silkIds, String requestId) {
    return silkFlux
        .flatMap(this::fetchImage)
        .collectList()
        .map(images -> reorderImagesBasedOnInputIds(silkIds, images))
        .doOnNext(imageDataList -> logImages(imageDataList, requestId))
        .map(images -> images.stream().map(ImageData::getImageContent).collect(Collectors.toList()))
        .map(
            images ->
                spriteGenerator.generate(images, getImageProvider(imageProvider).getDefaultSilk()))
        .map(opt -> opt.map(Mono::just).orElseGet(Mono::empty))
        .log(requestId)
        .onErrorReturn(
            Mono.just(
                defaultSilksSprite(
                    getImageProvider(imageProvider).getDefaultSilk(), silkIds.size())))
        .flatMap(ImageUtils::toByteArray);
  }

  private Mono<ImageData> fetchImage(SilkUrl silkUrl) {
    return provider.getImage(silkUrl);
  }

  private List<ImageData> reorderImagesBasedOnInputIds(
      List<String> silkIds, List<ImageData> images) {
    List<ImageData> reorderedImages = new ArrayList<>();
    Map<String, List<ImageData>> imagesBySilkId =
        images.stream().collect(Collectors.groupingBy(ImageData::getImageId));
    for (String silkId : silkIds) {
      List<ImageData> identicalImages = imagesBySilkId.get(silkId);
      if (identicalImages.size() > 1) {
        log.error("Multiple images fetched for the same silkId: {}", silkId);
      }
      reorderedImages.add(identicalImages.get(0));
    }
    return reorderedImages;
  }

  private void logImages(List<ImageData> images, String requestId) {
    log.info(
        "{} Before generating sprite: {}",
        requestId,
        images.stream()
            .map(
                imageData -> {
                  Optional<BufferedImage> maybeImage = imageData.getImageContent();
                  String imageId = String.valueOf(imageData.getImageId());
                  if (maybeImage.isPresent()) {
                    BufferedImage image = maybeImage.get();

                    if (!spriteGenerator.isImageWithExpectedSize(image)) {
                      NewRelic.noticeError(
                          MessageFormat.format(
                              "Wrong size for image https://silks.coral.co.uk/RP/images/{0}.png, {1}x{2}",
                              imageId, image.getWidth(), image.getHeight()));
                    }

                    return imageId + ":" + image.getWidth() + "x" + image.getHeight();
                  } else {
                    return imageId + ":-";
                  }
                })
            .collect(Collectors.toList()));
  }

  private ImageProvider getImageProvider(String imageProviderName) {
    return silksProperties
        .getImageProvider(imageProviderName)
        .orElseThrow(() -> new BadRequestException("Invalid provider=" + imageProviderName));
  }

  private BufferedImage defaultSilksSprite(BufferedImage defaultSilk, int numberOfSilksInSprite) {
    return spriteGenerator
        .generate(Collections.nCopies(numberOfSilksInSprite, Optional.of(defaultSilk)))
        .orElseThrow(
            () -> new RuntimeException("Failed to generate sprite with all silks default"));
  }
}
