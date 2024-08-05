package com.egalacoral.spark.timeform.api.services;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormContext;
import com.egalacoral.spark.timeform.api.connectivity.RequestPerformer;
import com.egalacoral.spark.timeform.api.services.endpoints.CourseMapEndpoint;
import com.egalacoral.spark.timeform.model.horseracing.HRCourseMap;
import java.io.IOException;
import okhttp3.OkHttpClient;
import okhttp3.ResponseBody;
import okhttp3.logging.HttpLoggingInterceptor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import retrofit2.Retrofit;

public class ImageService {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(ImageService.class);

  private final CourseMapEndpoint courseMapEndpoint;

  private final RequestPerformer requestPerformer;

  public ImageService(TimeFormContext context, RequestPerformer requestPerformer) {
    this.requestPerformer = requestPerformer;
    HttpLoggingInterceptor logging = new HttpLoggingInterceptor(message -> LOGGER.debug(message));
    logging.setLevel(HttpLoggingInterceptor.Level.HEADERS);

    OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
    httpClient.addInterceptor(logging);
    if (context.getInterceptor() != null) {
      httpClient.addInterceptor(context.getInterceptor());
    }

    httpClient.followRedirects(false);
    httpClient.followSslRedirects(false);

    courseMapEndpoint =
        new Retrofit.Builder() //
            .baseUrl(context.getImageUrl()) //
            .client(httpClient.build()) //
            .build() //
            .create(CourseMapEndpoint.class);
  }

  public void getCourseMap(
      String courseAbbrev,
      String raceTypeChar,
      String raceSurfaceChar,
      DataCallback<HRCourseMap> callback) {
    requestPerformer.invokeAsync(
        courseMapEndpoint.getCourseMap(courseAbbrev, raceTypeChar, raceSurfaceChar),
        new DataCallback<ResponseBody>() {
          @Override
          public void onResponse(ResponseBody response) {
            HRCourseMap result = new HRCourseMap();
            try {
              result.setBytes(response.bytes());
              if (response.contentType() != null) {
                result.setContentType(response.contentType().toString());
              }
              callback.onResponse(result);
            } catch (IOException e) {
              callback.onError(e);
            }
          }

          @Override
          public void onError(Exception throwable) {
            callback.onError(throwable);
          }
        });
  }
}
