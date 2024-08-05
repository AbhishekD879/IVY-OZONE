package com.coral.oxygen.middleware.featured.aem;

import static org.junit.Assert.assertTrue;

import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.featured.aem.model.OfferObject;
import com.coral.oxygen.middleware.featured.configuration.AemMetaConsumerConfig;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.stream.Collectors;
import lombok.Builder;
import lombok.Data;
import okhttp3.OkHttpClient;
import org.apache.commons.lang3.StringUtils;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;

public class AemMetaConsumerTest {

  private static final String AEM_OFFER_ENDPOINT = "https://35.176.108.76/";

  private static final String BRAND_NAME = "coral";

  private OkHttpClient okHttpClient;

  @Before
  public void init() throws NoSuchAlgorithmException, KeyManagementException {
    AemMetaConsumerConfig config = new AemMetaConsumerConfig();
    okHttpClient = config.cmsOkHttpClient(2, 2, "HEADERS", new OkHttpClientCreator(), null, null);
  }

  @Ignore
  @Test
  public void getBanners() {
    AemMetaConsumer consumer = new AemMetaConsumer(AEM_OFFER_ENDPOINT, BRAND_NAME, okHttpClient);
    List<OfferObject> offerObjectStream = consumer.getBanners();
    assertTrue(offerObjectStream.size() > 0);
  }

  @Data
  public static class SportsCategories {

    String categoryId;
    String ssCategoryCode;
    String targetUri;
  }

  @Data
  @Builder
  public static class SportsCategoriesLookup {

    String categoryId;
    Set<String> synonyms;
  }

  @Ignore
  @Test
  public void sportsCategoriesRead_ok() {
    String eventJson = TestUtils.getResourse("for-tests-only-sports-categories.json");
    Type listType = new TypeToken<List<SportsCategories>>() {}.getType();
    List<SportsCategories> categories = ModuleAdapter.FEATURED_GSON.fromJson(eventJson, listType);
    // List<SportsCategories> categories =
    // TestUtils.deserializeListWithGson("sports-categories.json", SportsCategories.class);
    assertTrue(categories.size() > 0);

    List<SportsCategoriesLookup> lookup =
        categories.stream().map(AemMetaConsumerTest::mapTo).collect(Collectors.toList());

    Gson gson = new GsonBuilder().create();
    String output = gson.toJson(lookup);
    assertTrue(output.length() > 0);
  }

  public static SportsCategoriesLookup mapTo(SportsCategories source) {
    String syn;
    Set<String> synonyms = new HashSet<>();
    if (!StringUtils.isBlank(source.ssCategoryCode)) {
      syn = source.ssCategoryCode.trim().toLowerCase();
      synonyms.add(syn);
      if (syn.contains("_")) {
        synonyms.add(syn.replace('_', '-'));
      }
    }
    if (!StringUtils.isBlank(source.targetUri)) {
      syn = source.targetUri.toLowerCase();
      StringTokenizer toc = new StringTokenizer(syn, "/");
      while (toc.hasMoreTokens()) {
        syn = toc.nextToken();
      }
      synonyms.add(syn);
    }
    return SportsCategoriesLookup.builder()
        .categoryId(source.getCategoryId())
        .synonyms(synonyms)
        .build();
  }
}
