package com.egalacoral.spark.timeform.api.services;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormContext;
import com.egalacoral.spark.timeform.api.services.endpoints.DataEndpoint;
import com.egalacoral.spark.timeform.api.services.endpoints.params.DataParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.InlineCountParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.SkipParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.TopParam;
import com.egalacoral.spark.timeform.model.greyhound.*;
import com.egalacoral.spark.timeform.model.horseracing.*;
import com.egalacoral.spark.timeform.model.internal.DataResponse;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;
import java.util.stream.Collectors;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.logging.HttpLoggingInterceptor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class DataService extends AbstractTimeFormService {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(DataService.class);
  public static final int CONNECT_TIMEOUT = 30;
  public static final int READ_TIMEOUT = 30;
  public static final int WRITE_TIMEOUT = 30;

  private final DataEndpoint dataEndpoint;

  private int pageSize;
  private String grUrlSuffix;
  private String hrUrlSuffix;

  public DataService(TimeFormContext context) {
    super(context);
    this.pageSize = 200;
    this.grUrlSuffix = context.getGrUrlSuffix();
    this.hrUrlSuffix = context.getHrUrlSuffix();

    HttpLoggingInterceptor logging = new HttpLoggingInterceptor(message -> LOGGER.debug(message));
    logging.setLevel(HttpLoggingInterceptor.Level.BODY);

    OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
    httpClient.addInterceptor(logging); // <-- this is the important line!
    httpClient.connectTimeout(CONNECT_TIMEOUT, TimeUnit.SECONDS);
    httpClient.readTimeout(READ_TIMEOUT, TimeUnit.SECONDS);
    httpClient.writeTimeout(WRITE_TIMEOUT, TimeUnit.SECONDS);
    httpClient.addInterceptor(
        chain -> {
          Request original = chain.request();

          Request request =
              original
                  .newBuilder()
                  .header("Authorization", "Bearer " + getContext().getTokenData().getAccessToken())
                  .method(original.method(), original.body())
                  .build();

          return chain.proceed(request);
        });
    if (context.getInterceptor() != null) {
      httpClient.addInterceptor(context.getInterceptor());
    }
    Gson gson = new GsonBuilder().setDateFormat("yyyy-MM-dd'T'HH:mm:ss").create();

    httpClient.followRedirects(false);
    httpClient.followSslRedirects(false);

    dataEndpoint =
        new Retrofit.Builder() //
            .baseUrl(context.getDataUrl()) //
            .addConverterFactory(GsonConverterFactory.create(gson)) //
            .client(httpClient.build()) //
            .build() //
            .create(DataEndpoint.class);
  }

  public void requestMeetings(DataCallback<List<Meeting>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getMeetings(grUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestEntries(DataCallback<List<Entry>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getEntries(grUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestGreyhounds(DataCallback<List<Greyhound>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getGreyhounds(grUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestPerformances(DataCallback<List<Performance>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getPerformances(grUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestPerformancesWithoutPagination(
      DataCallback<DataResponse<Performance>> callback, DataParam... params) {
    Map<String, String> paramMap = prepareParamsMap(Arrays.asList(params));
    getContext()
        .getRequestPerformer()
        .invokeAsync(dataEndpoint.getPerformances(grUrlSuffix, paramMap), callback);
  }

  public void requestRaces(DataCallback<List<Race>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getRaces(grUrlSuffix, map), Arrays.asList(params), callback, pageSize);
  }

  public void requestTracks(DataCallback<List<Track>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getTracks(grUrlSuffix, map), Arrays.asList(params), callback, pageSize);
  }

  public void requestHRMeetings(DataCallback<List<HRMeeting>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getHRMeetings(hrUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestHRRaces(DataCallback<List<HRRace>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getHRRaces(hrUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestHREntries(DataCallback<List<HREntry>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getHREntries(hrUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestHRPerformances(
      DataCallback<List<HRPerformance>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getHRPerformances(hrUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestHRCourses(DataCallback<List<HRCourse>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getHRCourses(hrUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public void requestHRCountries(DataCallback<List<HRCountry>> callback, DataParam... params) {
    pagination(
        map -> dataEndpoint.getHRCountries(hrUrlSuffix, map),
        Arrays.asList(params),
        callback,
        pageSize);
  }

  public <T> void pagination(
      Function<Map<String, String>, Call<DataResponse<T>>> function,
      List<DataParam> params,
      DataCallback<List<T>> callback,
      int pageSize) {
    new Paginator<T>(function, params, callback, pageSize).call();
  }

  private Map<String, String> prepareParamsMap(Collection<DataParam> params) {
    Map<String, String> paramsMap = new HashMap<>();
    if (params != null) {
      for (DataParam param : params) {
        String old = paramsMap.put(param.getName(), param.getValue().build());
        if (old != null) {
          throw new IllegalArgumentException("Duplicate param name: " + param.getName());
        }
      }
    }
    return paramsMap;
  }

  private class Paginator<T> implements DataCallback<DataResponse<T>> {

    private final DataCallback<List<T>> dataCallback;

    private final List<T> collector;

    private final Function<Map<String, String>, Call<DataResponse<T>>> function;

    private final Map<String, DataParam> params;

    private int pageSize;

    public Paginator(
        Function<Map<String, String>, Call<DataResponse<T>>> function,
        Collection<DataParam> params,
        DataCallback<List<T>> dataCallback,
        int pageSize) {
      this.function = function;
      this.params = params.stream().collect(Collectors.toMap(DataParam::getName, p -> p));
      this.dataCallback = dataCallback;
      this.pageSize = pageSize;
      this.collector = new ArrayList<T>();
    }

    public void call() {
      callNextPage();
    }

    private void setParam(DataParam param) {
      params.put(param.getName(), param);
    }

    private void callNextPage() {
      setParam(InlineCountParam.ALL_PAGES);
      setParam(TopParam.valueOf(pageSize));
      setParam(SkipParam.valueOf(collector.size()));
      getContext()
          .getRequestPerformer()
          .invokeAsync(function.apply(prepareParamsMap(params.values())), this);
    }

    @Override
    public void onResponse(DataResponse<T> data) {
      if (data.getEntities() != null) {
        collector.addAll(data.getEntities());
      }
      if (data.getTotalCount() > collector.size()) {
        callNextPage();
      } else {
        dataCallback.onResponse(collector);
      }
    }

    @Override
    public void onError(Exception throwable) {
      // TODO: decrease page size
      dataCallback.onError(throwable);
    }
  }

  public int getPageSize() {
    return pageSize;
  }

  public void setPageSize(int pageSize) {
    this.pageSize = pageSize;
  }
}
