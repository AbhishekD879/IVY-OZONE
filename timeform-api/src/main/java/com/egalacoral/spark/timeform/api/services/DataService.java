package com.egalacoral.spark.timeform.api.services;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

import com.egalacoral.spark.timeform.model.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormContext;
import com.egalacoral.spark.timeform.api.services.endpoints.DataEndpoint;
import com.egalacoral.spark.timeform.api.services.endpoints.params.DataParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.InlineCountParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.SkipParam;
import com.egalacoral.spark.timeform.api.services.endpoints.params.TopParam;
import com.egalacoral.spark.timeform.model.internal.DataResponse;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class DataService extends AbstractTimeFormService {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(DataService.class);

  private final DataEndpoint dataEndpoint;

  private final InlineCountParam inlineCountParam = InlineCountParam.ALL_PAGES;
  private int pageSize;

  public DataService(TimeFormContext context) {
    super(context);
    this.pageSize = 200;

    HttpLoggingInterceptor logging = new HttpLoggingInterceptor(new HttpLoggingInterceptor.Logger() {
      @Override
      public void log(String message) {
        LOGGER.debug(message);
      }
    });
    logging.setLevel(HttpLoggingInterceptor.Level.BODY);

    OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
    httpClient.addInterceptor(logging); // <-- this is the important line!
    httpClient.addInterceptor(chain -> {
      Request original = chain.request();

      Request request =
          original.newBuilder().header("Authorization", "Bearer " + getContext().getTokenData().getAccessToken())
              .method(original.method(), original.body()).build();

      return chain.proceed(request);
    });

    Gson gson = new GsonBuilder().setDateFormat("yyyy-MM-dd'T'HH:mm:ss").create();

    httpClient.followRedirects(false);
    httpClient.followSslRedirects(false);

    dataEndpoint = new Retrofit.Builder() //
        .baseUrl(context.getDataUrl()) //
        .addConverterFactory(GsonConverterFactory.create(gson)) //
        .client(httpClient.build()) //
        .build() //
        .create(DataEndpoint.class);
  }

  public void requestMeetings(DataCallback<List<Meeting>> callback, DataParam... params) {
    pagination(map -> dataEndpoint.getMeetings(map), Arrays.asList(params), callback, pageSize);
  }

  public void requestEntries(DataCallback<List<Entry>> callback, DataParam... params) {
    pagination(map -> dataEndpoint.getEntries(map), Arrays.asList(params), callback, pageSize);
  }

  public void requestGreyhounds(DataCallback<List<Greyhound>> callback, DataParam... params) {
    pagination(map -> dataEndpoint.getGreyhounds(map), Arrays.asList(params), callback, pageSize);
  }

  public void requestPerformances(DataCallback<List<Performance>> callback, DataParam... params) {
    pagination(map -> dataEndpoint.getPerformances(map), Arrays.asList(params), callback, pageSize);
  }

  public void requestRaces(DataCallback<List<Race>> callback, DataParam... params) {
    pagination(map -> dataEndpoint.getRaces(map), Arrays.asList(params), callback, pageSize);
  }

  public void requestTracks(DataCallback<List<Track>> callback, DataParam... params) {
    pagination(map -> dataEndpoint.getTracks(map), Arrays.asList(params), callback, pageSize);
  }

  public <T> void pagination(Function<Map<String, String>, Call<DataResponse<T>>> function, List<DataParam> params,
      DataCallback<List<T>> callback, int pageSize) {
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

    public Paginator(Function<Map<String, String>, Call<DataResponse<T>>> function, Collection<DataParam> params,
        DataCallback<List<T>> dataCallback, int pageSize) {
      this.function = function;
      this.params = params.stream().collect(Collectors.toMap(DataParam::getName, Function.identity()));
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
      getContext().getRequestPerformer().invokeAsync(function.apply(prepareParamsMap(params.values())), this);
    }

    @Override
    public void onResponse(DataResponse<T> data) {
      collector.addAll(data.getEntities());
      if (data.getTotalCount() > collector.size()) {
        callNextPage();
      } else {
        dataCallback.onResponse(collector);
      }
    }

    @Override
    public void onError(Throwable throwable) {
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
