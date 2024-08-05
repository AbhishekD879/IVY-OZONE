package com.oxygen.publisher.sportsfeatured.relation;

import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.SportsVersionResponse;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface FeaturedApi {

  /**
   * Retrieves the current featured version.
   *
   * @return a retrofit {@link Call} with the wrapped response
   */
  @GET("/api/featured/generation")
  Call<SportsVersionResponse> getVersion();

  /**
   * Retrieves featured model structure for the given version.
   *
   * @param version model version
   * @return retrofit {@link Call} with an object with all the modules of the version specified as
   *     response
   */
  @GET("/api/featured/structure/{version}")
  Call<FeaturedModel> getModelStructure(@Path("version") String version);

  /**
   * Retrieves module data by the given id and version.
   *
   * @param id module id
   * @param version model version
   * @return retrofit {@link Call} with an up-to-date featured module object as response
   */
  @GET("/api/featured/module/{id}/{version}")
  Call<AbstractFeaturedModule> getModule(@Path("id") String id, @Path("version") String version);

  /**
   * Retrieve list of available topics for the given module id and version.
   *
   * @param id module id
   * @param version model version
   * @return retrofit {@link Call} with list of topics as response
   */
  @GET("/api/featured/topics/{id}/{version}")
  Call<List<String>> getTopics(@Path("id") String id, @Path("version") String version);

  /**
   * Retrieves PageIds of active sport pages
   *
   * @return a retrofit {@link Call} with list of topics as response
   */
  @GET("/api/featured/sport-pages")
  Call<List<String>> getSportPages();
}
