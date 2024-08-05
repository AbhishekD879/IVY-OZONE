package com.ladbrokescoral.aggregation.service.impl;

import com.ladbrokescoral.aggregation.configuration.ApiProperties;
import com.ladbrokescoral.aggregation.configuration.ApiProperties.Image;
import com.ladbrokescoral.aggregation.model.ImageData;
import com.ladbrokescoral.aggregation.model.SilkUrl;
import com.ladbrokescoral.aggregation.repository.impl.CacheImageRepository;
import com.ladbrokescoral.aggregation.utils.SpriteGenerator;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.net.URI;
import java.util.Optional;
import javax.imageio.ImageIO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClient.RequestHeadersSpec;
import org.springframework.web.reactive.function.client.WebClient.RequestHeadersUriSpec;
import org.springframework.web.reactive.function.client.WebClient.ResponseSpec;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

// FIXME: need rework. use mockserver.
@ExtendWith(MockitoExtension.class)
public class ImageProviderServiceImplTest extends BDDMockito {

  private static final BufferedImage fakeImage =
      new BufferedImage(100, 100, BufferedImage.TYPE_INT_RGB);

  @Mock private WebClient webClientMock;
  @Mock private RequestHeadersUriSpec requestHeadersUriSpecMock;
  @Mock private RequestHeadersSpec requestHeadersSpecMock;
  @Spy private ResponseSpec clientResponseMock;
  @Mock private CacheImageRepository cacheImageRepository;
  @Mock SpriteGenerator<BufferedImage> verticalSpriteGenerator;

  private ImageProviderImpl imageProvider;
  private ApiProperties properties;

  private ImageData emptyImageData;

  @BeforeEach
  public void setUp() {

    properties = getProperties();
    imageProvider =
        new ImageProviderImpl(
            webClientMock, cacheImageRepository, properties, verticalSpriteGenerator);

    emptyImageData = ImageData.builder().imageId("1").imageContent(Optional.empty()).build();

    // given
    given(cacheImageRepository.get(any())).willReturn(Mono.empty());

    given(webClientMock.get()).willReturn(requestHeadersUriSpecMock);
    given(requestHeadersUriSpecMock.uri(any(URI.class))).willReturn(requestHeadersSpecMock);
    given(requestHeadersSpecMock.retrieve()).willReturn(clientResponseMock);
  }

  @Test
  public void shouldGetImage() throws Exception {

    // given
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    ImageIO.write(fakeImage, "jpg", baos);

    given(clientResponseMock.bodyToMono(ByteArrayResource.class))
        .willReturn(Mono.just(new ByteArrayResource(baos.toByteArray())));

    // when
    Mono<ImageData> imageDataMono =
        imageProvider.getImage(
            SilkUrl.builder().endpoint("https://test/1.gif").silkId("1").build());

    // then
    StepVerifier.create(imageDataMono).expectNext(emptyImageData).expectComplete().verify();
  }

  private ApiProperties getProperties() {
    ApiProperties properties = new ApiProperties();
    Image image = new Image();
    image.setNumberOfRetries(3);
    properties.setImage(image);
    return properties;
  }
}
