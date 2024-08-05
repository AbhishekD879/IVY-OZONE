package com.oxygen.publisher.sportsfeatured.configuration;

import static org.mockito.Mockito.when;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.oxygen.publisher.configuration.JsonSupportConfig;
import com.oxygen.publisher.model.RacingFormEvent;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.SegmentedFeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import com.oxygen.publisher.sportsfeatured.model.module.EventsModule;
import com.oxygen.publisher.sportsfeatured.model.module.HighlightCarouselModule;
import com.oxygen.publisher.sportsfeatured.model.module.SegmentView;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.sportsfeatured.util.SegmentedFeaturedModelHelper;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import okhttp3.MediaType;
import okhttp3.mock.MockInterceptor;
import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mockito;
import org.springframework.test.util.ReflectionTestUtils;
import retrofit2.Call;
import retrofit2.Response;

public class FeaturedApiProviderTest {

  private MockInterceptor interceptor;

  @Test
  public void featuredApi() throws IOException {
    ObjectMapper mapper = new JsonSupportConfig().objectMapper();

    interceptor = new MockInterceptor();
    interceptor
        .addRule()
        .get("http://test.com/api/featured/structure/1")
        .respond(
            ClassLoader.getSystemResourceAsStream("FeaturedModel.json"),
            MediaType.parse("application/json"));

    FeaturedApiProvider provider =
        new FeaturedApiProvider(mapper, Collections.singletonList(interceptor));

    ReflectionTestUtils.setField(provider, "featuredConsumerHost", "test.com");
    ReflectionTestUtils.setField(provider, "featuredConsumerPort", 80);
    provider.start();

    Call<FeaturedModel> featuredModelCall = provider.featuredApi().getModelStructure("1");
    Response<FeaturedModel> modelResponse = featuredModelCall.execute();
    FeaturedModel featuredModel = modelResponse.body();
    Assert.assertNotNull(featuredModel);
    Assert.assertEquals(7, featuredModel.getModules().size());

    EventsModule eventsModule = (EventsModule) featuredModel.getModules().get(1);
    EventsModuleData eventsModuleData = eventsModule.getData().get(0);
    RacingFormEvent racingFormEvent = eventsModuleData.getRacingFormEvent();
    Assert.assertNotNull(racingFormEvent);
    Assert.assertEquals("100m", racingFormEvent.getDistance());
  }

  @Test
  public void shouldNotPrepareTheSFMWithSameUniqueIDsReturnedFromConsumer() throws IOException {
    ObjectMapper mapper = new JsonSupportConfig().objectMapper();

    interceptor = new MockInterceptor();
    interceptor
        .addRule()
        .get("http://test.com/api/featured/structure/1")
        .respond(
            ClassLoader.getSystemResourceAsStream("FeaturedModelCSP.json"),
            MediaType.parse("application/json"));

    FeaturedApiProvider provider =
        new FeaturedApiProvider(mapper, Collections.singletonList(interceptor));

    ReflectionTestUtils.setField(provider, "featuredConsumerHost", "test.com");
    ReflectionTestUtils.setField(provider, "featuredConsumerPort", 80);
    provider.start();

    Call<FeaturedModel> featuredModelCall = provider.featuredApi().getModelStructure("1");
    Response<FeaturedModel> modelResponse = featuredModelCall.execute();
    FeaturedModel featuredModel = modelResponse.body();
    Assert.assertNotNull(featuredModel);
    Set<String> deserializedUniqueIds = new HashSet<>();
    featuredModel.getModules().stream()
        .filter(module -> module instanceof HighlightCarouselModule)
        .forEach(
            hc -> {
              deserializedUniqueIds.addAll(
                  hc.getData().stream()
                      .map(emd -> ((EventsModuleData) emd).getUniqueId())
                      .collect(Collectors.toSet()));
            });

    SegmentView segmentView = featuredModel.getSegmentWiseModules().get("Universal");
    List<AbstractFeaturedModule<?>> nonSegmentedModules = new ArrayList<>();
    SegmentedFeaturedModelHelper.fillNonSegmentedModules(featuredModel, nonSegmentedModules);
    SegmentedFeaturedModel segmentedFeaturedModel =
        SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(featuredModel);
    SegmentedFeaturedModelHelper.populateSegmentedFeaturedModel(
        featuredModel, segmentedFeaturedModel, segmentView);
    segmentedFeaturedModel.addModules(nonSegmentedModules);

    Set<String> serializedUniqueIds = new HashSet<>();
    segmentedFeaturedModel.getModules().stream()
        .filter(module -> module instanceof HighlightCarouselModule)
        .forEach(
            hc -> {
              serializedUniqueIds.addAll(
                  hc.getData().stream()
                      .map(emd -> ((EventsModuleData) emd).getUniqueId())
                      .collect(Collectors.toSet()));
            });

    Assert.assertFalse(serializedUniqueIds.containsAll(deserializedUniqueIds));
  }

  @Test(expected = CloneNotSupportedException.class)
  public void testcloneWithNewUniqueId() throws CloneNotSupportedException {

    EventsModuleData data = Mockito.spy(EventsModuleData.class);
    when(data.cloneEventModuleData()).thenThrow(new CloneNotSupportedException());
    data.cloneWithNewUniqueId();
  }
}
